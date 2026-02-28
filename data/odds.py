"""
Odds Client
Pulls live spreads, totals, and moneylines from The Odds API
https://the-odds-api.com
Free tier: 500 requests/month
"""
import requests
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import ODDS_API_KEY, ODDS_API_BASE, ODDS_REGIONS, ODDS_MARKETS, ODDS_BOOKMAKERS


@dataclass
class BookLine:
    """A single bookmaker's line for a game"""
    bookmaker: str
    spread_home: float
    spread_away: float
    spread_home_price: int     # American odds
    spread_away_price: int
    total: float
    total_over_price: int
    total_under_price: int
    ml_home: int               # moneyline
    ml_away: int
    updated: str


@dataclass
class GameOdds:
    """All odds data for a single game"""
    game_id: str
    sport: str
    commence_time: str
    home_team: str
    away_team: str
    books: List[BookLine] = field(default_factory=list)

    @property
    def consensus_spread_home(self) -> float:
        """Average home spread across all books"""
        spreads = [b.spread_home for b in self.books if b.spread_home != 0]
        return sum(spreads) / len(spreads) if spreads else 0.0

    @property
    def consensus_total(self) -> float:
        """Average total across all books"""
        totals = [b.total for b in self.books if b.total != 0]
        return sum(totals) / len(totals) if totals else 0.0

    @property
    def sharpest_spread_home(self) -> float:
        """Use Pinnacle if available, else FanDuel, else consensus"""
        for preferred in ["pinnacle", "fanduel", "draftkings"]:
            for b in self.books:
                if b.bookmaker == preferred:
                    return b.spread_home
        return self.consensus_spread_home

    def implied_probability(self, american_odds: int) -> float:
        """Convert American odds to implied probability"""
        if american_odds > 0:
            return 100 / (american_odds + 100)
        else:
            return abs(american_odds) / (abs(american_odds) + 100)

    @property
    def home_implied_prob(self) -> float:
        """Implied win probability for home team from consensus ML"""
        mls = [b.ml_home for b in self.books if b.ml_home != 0]
        if not mls:
            return 0.5
        avg_ml = sum(mls) / len(mls)
        return self.implied_probability(int(avg_ml))


# Map sport keys from The Odds API to our internal names
SPORT_MAP = {
    "nba": "basketball_nba",
    "ncaab": "basketball_ncaab",
    "nfl": "americanfootball_nfl",
    "ncaaf": "americanfootball_ncaaf",
    "mlb": "baseball_mlb",
    "nhl": "icehockey_nhl",
}


class OddsClient:
    """
    Pulls odds from The Odds API.

    Usage:
        client = OddsClient()
        games = client.get_odds("nba")
        for g in games:
            print(f"{g.away_team} @ {g.home_team} | Spread: {g.consensus_spread_home}")
    """

    def __init__(self):
        if not ODDS_API_KEY:
            print("[ODDS] WARNING: No ODDS_API_KEY set. Set env var ODDS_API_KEY.")
        self.session = requests.Session()
        self._remaining_requests = None

    def get_odds(self, sport: str = "nba") -> List[GameOdds]:
        """
        Get current odds for all games in a sport.

        Args:
            sport: "nba", "ncaab", "nfl", "ncaaf", "mlb", "nhl"

        Returns:
            List of GameOdds objects
        """
        sport_key = SPORT_MAP.get(sport, sport)

        url = f"{ODDS_API_BASE}/sports/{sport_key}/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": ODDS_REGIONS,
            "markets": ODDS_MARKETS,
            "bookmakers": ODDS_BOOKMAKERS,
            "oddsFormat": "american",
        }

        try:
            resp = self.session.get(url, params=params, timeout=30)
            resp.raise_for_status()

            # Track remaining API calls
            self._remaining_requests = resp.headers.get("x-requests-remaining")
            if self._remaining_requests:
                print(f"[ODDS] Requests remaining: {self._remaining_requests}")

            data = resp.json()
        except Exception as e:
            print(f"[ODDS] Error fetching {sport}: {e}")
            return []

        return self._parse_odds(data, sport)

    def _parse_odds(self, data: list, sport: str) -> List[GameOdds]:
        """Parse raw API response into GameOdds objects"""
        games = []

        for event in data:
            game = GameOdds(
                game_id=event.get("id", ""),
                sport=sport,
                commence_time=event.get("commence_time", ""),
                home_team=event.get("home_team", ""),
                away_team=event.get("away_team", ""),
            )

            for bookmaker in event.get("bookmakers", []):
                book_name = bookmaker.get("key", "")
                book_line = BookLine(
                    bookmaker=book_name,
                    spread_home=0, spread_away=0,
                    spread_home_price=0, spread_away_price=0,
                    total=0, total_over_price=0, total_under_price=0,
                    ml_home=0, ml_away=0,
                    updated=bookmaker.get("last_update", ""),
                )

                for market in bookmaker.get("markets", []):
                    mkey = market.get("key", "")
                    outcomes = market.get("outcomes", [])

                    if mkey == "spreads":
                        for o in outcomes:
                            if o.get("name") == event.get("home_team"):
                                book_line.spread_home = o.get("point", 0)
                                book_line.spread_home_price = o.get("price", 0)
                            else:
                                book_line.spread_away = o.get("point", 0)
                                book_line.spread_away_price = o.get("price", 0)

                    elif mkey == "totals":
                        for o in outcomes:
                            if o.get("name") == "Over":
                                book_line.total = o.get("point", 0)
                                book_line.total_over_price = o.get("price", 0)
                            else:
                                book_line.total_under_price = o.get("price", 0)

                    elif mkey == "h2h":
                        for o in outcomes:
                            if o.get("name") == event.get("home_team"):
                                book_line.ml_home = o.get("price", 0)
                            else:
                                book_line.ml_away = o.get("price", 0)

                game.books.append(book_line)

            games.append(game)

        return games

    @property
    def requests_remaining(self) -> Optional[str]:
        return self._remaining_requests


if __name__ == "__main__":
    client = OddsClient()
    games = client.get_odds("nba")
    print(f"\n[ODDS] Found {len(games)} NBA games\n")
    for g in games:
        print(f"  {g.away_team:25s} @ {g.home_team:25s} | "
              f"Spread: {g.consensus_spread_home:+.1f} | "
              f"Total: {g.consensus_total:.1f} | "
              f"Home Impl: {g.home_implied_prob:.1%}")
