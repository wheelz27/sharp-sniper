"""
Matchup Analyzer
Orchestrates all components:
  Data (stats + odds + injuries) → Ratings → Edge → Output

This is the main pipeline you run daily.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data.nba_stats import NBAStatsClient, TeamProfile
from data.ncaab_stats import NCAABStatsClient, NCAABTeamProfile
from data.odds import OddsClient, GameOdds
from data.injuries import InjuryTracker
from engine.ratings import RatingEngine, PowerRating
from engine.edge import EdgeCalculator, EdgeResult, rank_edges


# ─────────────────────────────────────────────
# TEAM NAME MAPPING
# The Odds API uses full names, NBA API uses abbreviations.
# This maps between them.
# ─────────────────────────────────────────────
NBA_NAME_TO_ABBR = {
    "Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN",
    "Charlotte Hornets": "CHA", "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN", "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA", "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP", "New York Knicks": "NYK", "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR", "Utah Jazz": "UTA", "Washington Wizards": "WAS",
}

ABBR_TO_NBA_NAME = {v: k for k, v in NBA_NAME_TO_ABBR.items()}


class MatchupAnalyzer:
    """
    Full pipeline: pull data → compute ratings → compare to market → output edges.

    Usage:
        analyzer = MatchupAnalyzer(sport="nba")
        edges = analyzer.run()

        for edge in edges:
            print(edge.headline)

    Or for manual matchup analysis:
        edge = analyzer.analyze_matchup("SAS", "LAL")
    """

    def __init__(self, sport: str = "nba", season: str = "2025-26"):
        self.sport = sport
        self.season = season

        # Initialize components
        self.rating_engine = RatingEngine()
        self.edge_calc = EdgeCalculator(sport=sport)
        self.odds_client = OddsClient()
        self.injury_tracker = InjuryTracker()

        # Sport-specific data client
        if sport == "nba":
            self.stats_client = NBAStatsClient(season=season)
        else:
            year = int(season.split("-")[0]) + 1 if "-" in season else int(season)
            self.stats_client = NCAABStatsClient(season=year)

        # Cached data
        self._ratings: Dict[str, PowerRating] = {}
        self._games: List[GameOdds] = []

    def load_injuries(self, injury_data: Dict[str, List[dict]]):
        """
        Load injury data before running analysis.

        Example:
            analyzer.load_injuries({
                "SAS": [{"player": "Wembanyama", "status": "out", "role": "star", "reason": "knee"}],
                "LAL": [{"player": "Davis", "status": "doubtful", "role": "star", "reason": "back"}],
            })
        """
        self.injury_tracker.load_from_dict(injury_data)

    def _resolve_team_abbr(self, full_name: str) -> str:
        """Convert full team name (from Odds API) to abbreviation"""
        if self.sport == "nba":
            return NBA_NAME_TO_ABBR.get(full_name, full_name[:3].upper())
        else:
            # NCAAB uses full names as keys
            return full_name

    def refresh_data(self):
        """Pull fresh stats and odds data"""
        print(f"\n{'='*60}")
        print(f"  EDGE INTEL — {self.sport.upper()} Pipeline")
        print(f"{'='*60}\n")

        # Pull team stats
        if self.sport == "nba":
            profiles = self.stats_client.get_all_team_profiles()
            self._ratings = self.rating_engine.compute_nba_ratings(profiles)
        else:
            profiles = self.stats_client.get_all_team_profiles()
            self._ratings = self.rating_engine.compute_ncaab_ratings(profiles)

        # Pull odds
        self._games = self.odds_client.get_odds(self.sport)

        print(f"\n[PIPELINE] {len(self._ratings)} teams rated, {len(self._games)} games on board\n")

    def run(self, max_plays: int = 5) -> List[EdgeResult]:
        """
        Full pipeline: refresh data → compute all edges → return ranked plays.

        Returns list of EdgeResult objects, sorted by edge size.
        """
        self.refresh_data()
        return self._compute_all_edges(max_plays)

    def _compute_all_edges(self, max_plays: int = 5) -> List[EdgeResult]:
        """Compute edge for every game on the board"""
        all_edges = []

        for game in self._games:
            away_abbr = self._resolve_team_abbr(game.away_team)
            home_abbr = self._resolve_team_abbr(game.home_team)

            away_rating = self._ratings.get(away_abbr)
            home_rating = self._ratings.get(home_abbr)

            if not away_rating or not home_rating:
                print(f"[SKIP] Missing rating: {game.away_team} ({away_abbr}) or {game.home_team} ({home_abbr})")
                continue

            # Market data
            market_spread = game.consensus_spread_home
            market_total = game.consensus_total
            home_impl_prob = game.home_implied_prob

            if market_spread == 0 and market_total == 0:
                continue  # no lines posted yet

            # Model projections
            injury_adj = self.injury_tracker.get_matchup_impact(home_abbr, away_abbr)
            model_spread = self.rating_engine.compute_model_spread(
                team_a_rating=home_rating,
                team_b_rating=away_rating,
                home_team=home_abbr,
                injury_adj=injury_adj,
            )
            model_total = self.rating_engine.compute_model_total(home_rating, away_rating)

            # Injury summaries
            inj_away = self.injury_tracker.get_summary(away_abbr)
            inj_home = self.injury_tracker.get_summary(home_abbr)

            # Compute edge
            edge = self.edge_calc.compute_edge(
                away_rating=away_rating,
                home_rating=home_rating,
                model_spread_home=model_spread,
                model_total=model_total,
                market_spread_home=market_spread,
                market_total=market_total,
                home_implied_prob=home_impl_prob,
                injury_impact=injury_adj,
                injury_summary_away=inj_away,
                injury_summary_home=inj_home,
            )

            all_edges.append(edge)

        # Rank and filter
        ranked = rank_edges(all_edges, max_plays)

        print(f"[PIPELINE] {len(all_edges)} games analyzed, {len(ranked)} plays flagged\n")
        return ranked

    def analyze_matchup(self, team_a: str, team_b: str,
                        market_spread: float = 0, market_total: float = 0) -> Optional[EdgeResult]:
        """
        Analyze a single matchup manually.
        Assumes team_a is home.

        Usage:
            edge = analyzer.analyze_matchup("SAS", "LAL", market_spread=-4.0, market_total=222.5)
        """
        if not self._ratings:
            print("[WARN] No ratings loaded. Call refresh_data() first.")
            return None

        home_rating = self._ratings.get(team_a.upper())
        away_rating = self._ratings.get(team_b.upper())

        if not home_rating or not away_rating:
            print(f"[ERROR] Missing rating for {team_a} or {team_b}")
            return None

        injury_adj = self.injury_tracker.get_matchup_impact(team_a, team_b)
        model_spread = self.rating_engine.compute_model_spread(
            team_a_rating=home_rating,
            team_b_rating=away_rating,
            home_team=team_a,
            injury_adj=injury_adj,
        )
        model_total = self.rating_engine.compute_model_total(home_rating, away_rating)

        return self.edge_calc.compute_edge(
            away_rating=away_rating,
            home_rating=home_rating,
            model_spread_home=model_spread,
            model_total=model_total,
            market_spread_home=market_spread,
            market_total=market_total,
            injury_impact=injury_adj,
            injury_summary_away=self.injury_tracker.get_summary(team_b),
            injury_summary_home=self.injury_tracker.get_summary(team_a),
        )

    def get_team_report(self, team: str) -> str:
        """
        Generate a team breakdown showing all time windows.
        This is the "season → month → week → last game" view you wanted.
        """
        rating = self._ratings.get(team.upper())
        if not rating:
            return f"No data for {team}"

        lines = [
            f"{'='*50}",
            f"  {rating.team_name} ({rating.team_abbr})",
            f"  Record: {rating.season_record}",
            f"{'='*50}",
            f"",
            f"  {'Window':<12} {'Net':>8} {'Off':>8} {'Def':>8}",
            f"  {'─'*40}",
            f"  {'Season':<12} {rating.season_net:>+8.1f}",
            f"  {'Last 15':<12} {rating.last_15_net:>+8.1f}",
            f"  {'Last 5':<12} {rating.last_5_net:>+8.1f}",
            f"  {'Last Game':<12} {rating.last_1_net:>+8.1f}",
            f"",
            f"  Weighted Net:  {rating.weighted_net:>+.1f}",
            f"  Weighted Off:  {rating.weighted_off:>.1f}",
            f"  Weighted Def:  {rating.weighted_def:>.1f}",
            f"  Pace:          {rating.weighted_pace:>.1f}",
            f"",
            f"  Trend:  {rating.trend_label}",
            f"  Regime: {rating.regime_shift_label}",
            f"",
            f"  Injuries:",
            f"  {self.injury_tracker.get_summary(team)}",
        ]
        return "\n".join(lines)
