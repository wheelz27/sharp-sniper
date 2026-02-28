"""
Edge Calculator
Compares model projections to market lines.
Identifies mispricing and computes expected value.

Production guardrails:
  - Edge capping (anomalous edges → auto-PASS)
  - Input validation (NaN/None/absurd values caught)
  - Anomaly logging for debugging
"""
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
import math
import logging

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import NBA_THRESHOLDS, NCAAB_THRESHOLDS, get_confidence_tier, EdgeThresholds
from engine.ratings import PowerRating

logger = logging.getLogger("edgeintel.edge")

# ─────────────────────────────────────────────
# PRODUCTION GUARDRAILS
# ─────────────────────────────────────────────
MAX_EDGE_POINTS = 10.0          # Any edge > 10 pts = data error, not opportunity
MAX_SPREAD_ABS = 30.0           # No realistic spread exceeds ±30
MAX_TOTAL = 300.0               # No realistic total exceeds 300
MIN_TOTAL = 150.0               # No realistic total below 150
MAX_INJURY_IMPACT = 12.0        # Injury adjustment cap


@dataclass
class EdgeResult:
    """Complete edge analysis for a single game"""
    # Teams
    away_team: str
    home_team: str
    sport: str

    # Ratings
    away_rating: float
    home_rating: float
    away_trend: str
    home_trend: str

    # Model
    model_spread_home: float     # negative = home favored
    model_total: float

    # Market
    market_spread_home: float
    market_total: float
    home_implied_prob: float

    # Edge
    spread_edge: float           # model_spread - market_spread (positive = home undervalued)
    total_edge: float
    model_win_prob_home: float
    ev_pct: float                # expected value percentage

    # Injury context
    injury_impact: float
    injury_summary_away: str
    injury_summary_home: str

    # Meta
    confidence: str
    play_side: str               # "HOME", "AWAY", "OVER", "UNDER", or "NO PLAY"
    is_playable: bool

    # Regime shift flags
    away_regime_shift: float
    home_regime_shift: float

    @property
    def edge_abs(self) -> float:
        return abs(self.spread_edge)

    @property
    def headline(self) -> str:
        """One-line summary for quick scanning"""
        if not self.is_playable:
            return f"{self.away_team} @ {self.home_team} — NO EDGE"
        side = self.home_team if self.play_side == "HOME" else self.away_team
        return f"{self.confidence} {side} | Edge: {self.edge_abs:.1f} pts | EV: {self.ev_pct:+.1f}%"


class EdgeCalculator:
    """
    Takes model spreads + market lines and identifies edges.

    Usage:
        calc = EdgeCalculator(sport="nba")
        edge = calc.compute_edge(
            away_rating=ratings["LAL"],
            home_rating=ratings["SAS"],
            model_spread_home=-6.5,
            model_total=225.0,
            market_spread_home=-4.0,
            market_total=222.5,
            home_implied_prob=0.62,
            injury_impact=1.5,
            injury_summary_away="Davis doubtful (back) [-3.2 pts]",
            injury_summary_home="No significant injuries",
        )

        if edge.is_playable:
            print(edge.headline)
    """

    def __init__(self, sport: str = "nba"):
        self.sport = sport
        self.thresholds = NBA_THRESHOLDS if sport == "nba" else NCAAB_THRESHOLDS

    def _spread_to_win_prob(self, spread: float) -> float:
        """
        Convert point spread to implied win probability.
        Uses a logistic approximation calibrated to historical data.

        spread < 0 means the team is favored.
        Returns probability that the team with the spread covers/wins.
        """
        # Logistic function: P(win) ≈ 1 / (1 + 10^(spread / k))
        # k ≈ 8.0 for NBA (each point ≈ ~3% win probability shift)
        # k ≈ 9.5 for NCAAB (more variance)
        k = 8.0 if self.sport == "nba" else 9.5
        return 1.0 / (1.0 + math.pow(10, spread / k))

    def _compute_ev(self, model_prob: float, market_prob: float) -> float:
        """
        Expected value percentage.
        EV% = (model_prob / market_prob - 1) * 100

        Positive EV% = edge exists.
        """
        if market_prob <= 0:
            return 0.0
        return round((model_prob / market_prob - 1) * 100, 2)

    def compute_edge(
        self,
        away_rating: PowerRating,
        home_rating: PowerRating,
        model_spread_home: float,
        model_total: float,
        market_spread_home: float,
        market_total: float,
        home_implied_prob: float = 0.5,
        injury_impact: float = 0.0,
        injury_summary_away: str = "No significant injuries",
        injury_summary_home: str = "No significant injuries",
    ) -> EdgeResult:
        """Compute full edge analysis for a matchup"""

        # ── INPUT VALIDATION ──
        validation_error = self._validate_inputs(
            model_spread_home, model_total, market_spread_home,
            market_total, home_implied_prob, injury_impact,
            away_rating, home_rating
        )
        if validation_error:
            logger.warning(f"Input validation failed: {away_rating.team_abbr}@{home_rating.team_abbr} — {validation_error}")
            return self._quarantined_result(away_rating, home_rating, validation_error)

        # Spread edge (positive = home team undervalued by market)
        spread_edge = model_spread_home - market_spread_home

        # ── EDGE CAPPING (ANOMALY GUARD) ──
        if abs(spread_edge) > MAX_EDGE_POINTS:
            logger.warning(
                f"EDGE ANOMALY: {away_rating.team_abbr}@{home_rating.team_abbr} | "
                f"Model={model_spread_home:.1f} Market={market_spread_home:.1f} Edge={spread_edge:.1f} — QUARANTINED"
            )
            return self._quarantined_result(
                away_rating, home_rating,
                f"Edge {spread_edge:.1f} exceeds cap ({MAX_EDGE_POINTS}). Likely data error."
            )

        # Total edge
        total_edge = model_total - market_total

        # Win probabilities
        model_win_prob_home = self._spread_to_win_prob(model_spread_home)
        market_win_prob_home = max(home_implied_prob, 0.01)

        # EV (for spread bet side)
        if spread_edge < 0:
            # Edge favors home team
            ev_pct = self._compute_ev(model_win_prob_home, market_win_prob_home)
        else:
            # Edge favors away team
            model_away_prob = 1 - model_win_prob_home
            market_away_prob = 1 - market_win_prob_home
            ev_pct = self._compute_ev(model_away_prob, market_away_prob)

        # Determine play side
        edge_abs = abs(spread_edge)
        is_playable = edge_abs >= self.thresholds.min_edge_points

        if not is_playable:
            play_side = "NO PLAY"
        elif spread_edge < 0:
            # Model has home MORE favored than market → home undervalued
            play_side = "HOME"
        else:
            # Model has home LESS favored than market → away undervalued
            play_side = "AWAY"

        confidence = get_confidence_tier(edge_abs, self.sport)

        return EdgeResult(
            away_team=away_rating.team_abbr,
            home_team=home_rating.team_abbr,
            sport=self.sport,
            away_rating=away_rating.weighted_net,
            home_rating=home_rating.weighted_net,
            away_trend=away_rating.trend_label,
            home_trend=home_rating.trend_label,
            model_spread_home=model_spread_home,
            model_total=model_total,
            market_spread_home=market_spread_home,
            market_total=market_total,
            home_implied_prob=home_implied_prob,
            spread_edge=round(spread_edge, 1),
            total_edge=round(total_edge, 1),
            model_win_prob_home=round(model_win_prob_home, 3),
            ev_pct=ev_pct,
            injury_impact=injury_impact,
            injury_summary_away=injury_summary_away,
            injury_summary_home=injury_summary_home,
            confidence=confidence,
            play_side=play_side,
            is_playable=is_playable,
            away_regime_shift=away_rating.regime_shift,
            home_regime_shift=home_rating.regime_shift,
        )

    def _validate_inputs(self, model_spread, model_total, market_spread,
                         market_total, implied_prob, injury_impact,
                         away_rating, home_rating) -> Optional[str]:
        """
        Validate all inputs before computing edge.
        Returns error string if invalid, None if clean.
        """
        # NaN / None checks
        for name, val in [("model_spread", model_spread), ("market_spread", market_spread),
                          ("model_total", model_total), ("market_total", market_total)]:
            if val is None or (isinstance(val, float) and math.isnan(val)):
                return f"{name} is NaN/None"

        # Spread sanity
        if abs(model_spread) > MAX_SPREAD_ABS:
            return f"Model spread {model_spread} exceeds ±{MAX_SPREAD_ABS}"
        if abs(market_spread) > MAX_SPREAD_ABS:
            return f"Market spread {market_spread} exceeds ±{MAX_SPREAD_ABS}"

        # Total sanity
        if model_total > 0 and (model_total > MAX_TOTAL or model_total < MIN_TOTAL):
            return f"Model total {model_total} outside range [{MIN_TOTAL}, {MAX_TOTAL}]"

        # Implied probability sanity
        if implied_prob < 0.01 or implied_prob > 0.99:
            return f"Implied prob {implied_prob} outside [0.01, 0.99]"

        # Injury cap
        if abs(injury_impact) > MAX_INJURY_IMPACT:
            return f"Injury impact {injury_impact} exceeds ±{MAX_INJURY_IMPACT}"

        # Rating sanity
        if abs(away_rating.weighted_net) > 25 or abs(home_rating.weighted_net) > 25:
            return f"Weighted net rating outside ±25 range"

        return None

    def _quarantined_result(self, away_rating: PowerRating, home_rating: PowerRating,
                            reason: str = "Data anomaly") -> EdgeResult:
        """Return a safe PASS result when inputs are bad"""
        return EdgeResult(
            away_team=away_rating.team_abbr,
            home_team=home_rating.team_abbr,
            sport=self.sport,
            away_rating=away_rating.weighted_net,
            home_rating=home_rating.weighted_net,
            away_trend=away_rating.trend_label,
            home_trend=home_rating.trend_label,
            model_spread_home=0.0,
            model_total=0.0,
            market_spread_home=0.0,
            market_total=0.0,
            home_implied_prob=0.5,
            spread_edge=0.0,
            total_edge=0.0,
            model_win_prob_home=0.5,
            ev_pct=0.0,
            injury_impact=0.0,
            injury_summary_away="QUARANTINED",
            injury_summary_home=reason,
            confidence="⚪ LOW",
            play_side="NO PLAY",
            is_playable=False,
            away_regime_shift=0.0,
            home_regime_shift=0.0,
        )


def rank_edges(edges: List[EdgeResult], max_plays: int = 5) -> List[EdgeResult]:
    """
    Rank and filter edges by strength.
    Returns top N playable edges sorted by absolute edge size.
    """
    playable = [e for e in edges if e.is_playable]
    playable.sort(key=lambda e: e.edge_abs, reverse=True)
    return playable[:max_plays]
