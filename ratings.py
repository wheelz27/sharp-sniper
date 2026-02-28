"""
Rating Engine
Computes time-weighted power ratings for NBA and NCAAB teams.

This is THE core of the system.
Everything else (edge, matchups, formatting) flows from these numbers.

The weighted rating formula:
    Weighted_Net = (W_season * Season_Net) + (W_15 * L15_Net) + (W_5 * L5_Net) + (W_1 * L1_Net)

Then model spread = (Team_A_Rating - Team_B_Rating) + home_court + injury_adjustment
"""
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import NBA_WEIGHTS, NCAAB_WEIGHTS, HOME_COURT, RatingWeights
from data.nba_stats import TeamProfile, TeamMetrics
from data.ncaab_stats import NCAABTeamProfile, NCAABTeamMetrics


@dataclass
class PowerRating:
    """Computed power rating for a team"""
    team_name: str
    team_abbr: str
    sport: str

    # Component ratings
    season_net: float
    last_15_net: float
    last_5_net: float
    last_1_net: float

    # Weighted composite
    weighted_net: float

    # Offensive / Defensive breakdown
    weighted_off: float
    weighted_def: float

    # Pace
    weighted_pace: float

    # Trend indicators
    trending_up: bool        # last_15 > season
    hot_streak: bool         # last_5 > last_15 > season
    cooling_off: bool        # last_5 < last_15 < season
    regime_shift: float      # last_15_net - season_net (magnitude of shift)

    # Raw data (for display)
    season_record: str = ""
    recent_record: str = ""

    @property
    def trend_label(self) -> str:
        if self.hot_streak:
            return "🔥 HOT"
        elif self.trending_up:
            return "📈 TRENDING UP"
        elif self.cooling_off:
            return "📉 COOLING"
        else:
            return "➡️ STABLE"

    @property
    def regime_shift_label(self) -> str:
        if abs(self.regime_shift) < 1.5:
            return "Stable"
        elif self.regime_shift > 3.0:
            return f"⚠️ MAJOR SHIFT UP (+{self.regime_shift:.1f})"
        elif self.regime_shift > 1.5:
            return f"Shift up (+{self.regime_shift:.1f})"
        elif self.regime_shift < -3.0:
            return f"⚠️ MAJOR SHIFT DOWN ({self.regime_shift:.1f})"
        else:
            return f"Shift down ({self.regime_shift:.1f})"


class RatingEngine:
    """
    Computes time-weighted power ratings.

    Usage:
        engine = RatingEngine()

        # NBA
        nba_profiles = nba_client.get_all_team_profiles()
        nba_ratings = engine.compute_nba_ratings(nba_profiles)
        spurs_rating = nba_ratings["SAS"]

        # NCAAB
        ncaab_profiles = ncaab_client.get_all_team_profiles()
        ncaab_ratings = engine.compute_ncaab_ratings(ncaab_profiles)

        # Model spread
        spread = engine.compute_model_spread(
            team_a_rating=nba_ratings["SAS"],
            team_b_rating=nba_ratings["LAL"],
            home_team="SAS",
            injury_adj=1.5
        )
    """

    def __init__(self, nba_weights: RatingWeights = None, ncaab_weights: RatingWeights = None):
        self.nba_weights = nba_weights or NBA_WEIGHTS
        self.ncaab_weights = ncaab_weights or NCAAB_WEIGHTS
        self.nba_weights.validate()
        self.ncaab_weights.validate()

    # ─────────────────────────────────────────
    # NBA RATINGS
    # ─────────────────────────────────────────

    def compute_nba_ratings(self, profiles: Dict[str, TeamProfile]) -> Dict[str, PowerRating]:
        """Compute weighted power ratings for all NBA teams"""
        ratings = {}
        w = self.nba_weights

        for abbr, prof in profiles.items():
            s = prof.season
            l15 = prof.last_15
            l5 = prof.last_5
            l1 = prof.last_1

            if not s:
                continue

            # Net ratings per window (fallback to season if missing)
            s_net = s.net_rating if s else 0
            l15_net = l15.net_rating if l15 else s_net
            l5_net = l5.net_rating if l5 else l15_net
            l1_net = l1.net_rating if l1 else l5_net

            # Offensive ratings
            s_off = s.off_rating if s else 0
            l15_off = l15.off_rating if l15 else s_off
            l5_off = l5.off_rating if l5 else l15_off
            l1_off = l1.off_rating if l1 else l5_off

            # Defensive ratings
            s_def = s.def_rating if s else 0
            l15_def = l15.def_rating if l15 else s_def
            l5_def = l5.def_rating if l5 else l15_def
            l1_def = l1.def_rating if l1 else l5_def

            # Pace
            s_pace = s.pace if s else 0
            l15_pace = l15.pace if l15 else s_pace
            l5_pace = l5.pace if l5 else l15_pace
            l1_pace = l1.pace if l1 else l5_pace

            # Weighted composites
            weighted_net = (w.season * s_net) + (w.last_15 * l15_net) + (w.last_5 * l5_net) + (w.last_game * l1_net)
            weighted_off = (w.season * s_off) + (w.last_15 * l15_off) + (w.last_5 * l5_off) + (w.last_game * l1_off)
            weighted_def = (w.season * s_def) + (w.last_15 * l15_def) + (w.last_5 * l5_def) + (w.last_game * l1_def)
            weighted_pace = (w.season * s_pace) + (w.last_15 * l15_pace) + (w.last_5 * l5_pace) + (w.last_game * l1_pace)

            # Trend detection
            trending_up = l15_net > s_net
            hot_streak = l5_net > l15_net > s_net
            cooling_off = l5_net < l15_net < s_net
            regime_shift = l15_net - s_net

            ratings[abbr] = PowerRating(
                team_name=prof.team_name,
                team_abbr=abbr,
                sport="nba",
                season_net=round(s_net, 2),
                last_15_net=round(l15_net, 2),
                last_5_net=round(l5_net, 2),
                last_1_net=round(l1_net, 2),
                weighted_net=round(weighted_net, 2),
                weighted_off=round(weighted_off, 2),
                weighted_def=round(weighted_def, 2),
                weighted_pace=round(weighted_pace, 2),
                trending_up=trending_up,
                hot_streak=hot_streak,
                cooling_off=cooling_off,
                regime_shift=round(regime_shift, 2),
                season_record=s.record if s else "",
                recent_record=l15.record if l15 else "",
            )

        return ratings

    # ─────────────────────────────────────────
    # NCAAB RATINGS
    # ─────────────────────────────────────────

    def compute_ncaab_ratings(self, profiles: Dict[str, NCAABTeamProfile]) -> Dict[str, PowerRating]:
        """Compute weighted power ratings for all NCAAB teams"""
        ratings = {}
        w = self.ncaab_weights

        for name, prof in profiles.items():
            s = prof.season
            l15 = prof.last_15
            l5 = prof.last_5
            l1 = prof.last_1

            if not s:
                continue

            # Net ratings
            s_net = s.adj_net if s else 0
            l15_net = l15.adj_net if l15 else s_net
            l5_net = l5.adj_net if l5 else l15_net
            l1_net = l1.adj_net if l1 else l5_net

            # Off/Def
            s_off = s.adj_off if s else 0
            l15_off = l15.adj_off if l15 else s_off
            l5_off = l5.adj_off if l5 else l15_off

            s_def = s.adj_def if s else 0
            l15_def = l15.adj_def if l15 else s_def
            l5_def = l5.adj_def if l5 else l15_def

            # Tempo
            s_tempo = s.tempo if s else 0
            l15_tempo = l15.tempo if l15 else s_tempo
            l5_tempo = l5.tempo if l5 else l15_tempo

            # Weighted
            # NCAAB doesn't always have last_1 granularity, so use 3 windows
            weighted_net = (w.season * s_net) + (w.last_15 * l15_net) + ((w.last_5 + w.last_game) * l5_net)
            weighted_off = (w.season * s_off) + (w.last_15 * l15_off) + ((w.last_5 + w.last_game) * l5_off)
            weighted_def = (w.season * s_def) + (w.last_15 * l15_def) + ((w.last_5 + w.last_game) * l5_def)
            weighted_pace = (w.season * s_tempo) + (w.last_15 * l15_tempo) + ((w.last_5 + w.last_game) * l5_tempo)

            trending_up = l15_net > s_net
            hot_streak = l5_net > l15_net > s_net
            cooling_off = l5_net < l15_net < s_net
            regime_shift = l15_net - s_net

            ratings[name] = PowerRating(
                team_name=name,
                team_abbr=name[:4].upper(),
                sport="ncaab",
                season_net=round(s_net, 2),
                last_15_net=round(l15_net, 2),
                last_5_net=round(l5_net, 2),
                last_1_net=round(l1_net if l1 else l5_net, 2),
                weighted_net=round(weighted_net, 2),
                weighted_off=round(weighted_off, 2),
                weighted_def=round(weighted_def, 2),
                weighted_pace=round(weighted_pace, 2),
                trending_up=trending_up,
                hot_streak=hot_streak,
                cooling_off=cooling_off,
                regime_shift=round(regime_shift, 2),
                season_record=s.record if s else "",
            )

        return ratings

    # ─────────────────────────────────────────
    # MODEL SPREAD COMPUTATION
    # ─────────────────────────────────────────

    def compute_model_spread(
        self,
        team_a_rating: PowerRating,
        team_b_rating: PowerRating,
        home_team: str,
        injury_adj: float = 0.0,
        rest_adj: float = 0.0,
    ) -> float:
        """
        Compute model-projected spread.

        Positive = team_a favored.
        Negative = team_b favored.

        Args:
            team_a_rating: PowerRating for team A
            team_b_rating: PowerRating for team B
            home_team: abbreviation of team playing at home ("A" side or "B" side)
            injury_adj: injury differential from InjuryTracker (from team_a perspective)
            rest_adj: rest advantage (positive = team_a rested more)
        """
        sport = team_a_rating.sport
        hca = HOME_COURT.get(sport, 2.5)

        # Base spread from rating difference
        raw_spread = team_a_rating.weighted_net - team_b_rating.weighted_net

        # Home court
        if home_team.upper() == team_a_rating.team_abbr.upper():
            raw_spread += hca
        elif home_team.upper() == team_b_rating.team_abbr.upper():
            raw_spread -= hca

        # Adjustments
        raw_spread += injury_adj
        raw_spread += rest_adj

        return round(raw_spread, 1)

    def compute_model_total(
        self,
        team_a_rating: PowerRating,
        team_b_rating: PowerRating,
    ) -> float:
        """
        Estimate total points based on pace and offensive/defensive efficiency.
        This is a simplified model — real totals models are more complex.
        """
        # Average pace determines possessions
        avg_pace = (team_a_rating.weighted_pace + team_b_rating.weighted_pace) / 2

        # Team A scores: their offense vs B's defense
        # Team B scores: their offense vs A's defense
        # Simplified: use weighted ratings as per-100-possession scores
        # Scale by actual expected possessions (pace / 100)
        pace_factor = avg_pace / 100.0

        a_scores = (team_a_rating.weighted_off + (200 - team_b_rating.weighted_def)) / 2 * pace_factor
        b_scores = (team_b_rating.weighted_off + (200 - team_a_rating.weighted_def)) / 2 * pace_factor

        return round(a_scores + b_scores, 1)
