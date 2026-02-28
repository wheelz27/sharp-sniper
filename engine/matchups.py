"""
Matchup Analyzer 
Orchestrates all components: Data → Ratings → Edge → Output
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import sys, os

# This ensures the engine can see the 'data' and 'engine' folders
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# FOLDER-AWARE IMPORTS
from data.nba_stats import NBAStatsClient
from data.ncaab_stats import NCAABStatsClient
from data.odds import OddsClient, GameOdds
from data.injuries import InjuryTracker
from engine.ratings import RatingEngine, PowerRating
from engine.edge import EdgeCalculator, EdgeResult, rank_edges

# --- TEAM NAME MAPPING ---
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

class MatchupAnalyzer:
    def __init__(self, sport: str = "nba", season: str = "2025-26"):
        self.sport = sport
        self.season = season

        # Initialize components
        self.rating_engine = RatingEngine()
        self.edge_calc = EdgeCalculator(sport=sport)
        self.odds_client = OddsClient()
        self.injury_tracker = InjuryTracker()

        if sport == "nba":
            self.stats_client = NBAStatsClient(season=season)
        else:
            year = int(season.split("-")[0]) + 1 if "-" in season else int(season)
            self.stats_client = NCAABStatsClient(season=year)

        self._ratings: Dict[str, PowerRating] = {}
        self._games: List[GameOdds] = []

    def _resolve_team_abbr(self, full_name: str) -> str:
        if self.sport == "nba":
            return NBA_NAME_TO_ABBR.get(full_name, full_name[:3].upper())
        return full_name

    def refresh_data(self):
        """Pull fresh stats and odds data"""
        if self.sport == "nba":
            profiles = self.stats_client.get_all_team_profiles()
            self._ratings = self.rating_engine.compute_nba_ratings(profiles)
        else:
            profiles = self.stats_client.get_all_team_profiles()
            self._ratings = self.rating_engine.compute_ncaab_ratings(profiles)

        self._games = self.odds_client.get_odds(self.sport)

    def compute_all_edges(self, max_plays: int = 5) -> List[EdgeResult]:
        """The 'Handshake' function called by app.py"""
        self.refresh_data()
        all_edges = []

        for game in self._games:
            away_abbr = self._resolve_team_abbr(game.away_team)
            home_abbr = self._resolve_team_abbr(game.home_team)
            
            away_rating = self._ratings.get(away_abbr)
            home_rating = self._ratings.get(home_abbr)

            if not away_rating or not home_rating:
                continue

            # Model projections
            injury_adj = self.injury_tracker.get_matchup_impact(home_abbr, away_abbr)
            model_spread = self.rating_engine.compute_model_spread(
                team_a_rating=home_rating,
                team_b_rating=away_rating,
                home_team=home_abbr,
                injury_adj=injury_adj,
            )
            model_total = self.rating_engine.compute_model_total(home_rating, away_rating)

            # Compute the final edge
            edge = self.edge_calc.compute_edge(
                away_rating=away_rating,
                home_rating=home_rating,
                model_spread_home=model_spread,
                model_total=model_total,
                market_spread_home=game.consensus_spread_home,
                market_total=game.consensus_total,
                home_implied_prob=game.home_implied_prob,
                injury_impact=injury_adj,
                injury_summary_away=self.injury_tracker.get_summary(away_abbr),
                injury_summary_home=self.injury_tracker.get_summary(home_abbr),
            )
            all_edges.append(edge)

        return all_edges
