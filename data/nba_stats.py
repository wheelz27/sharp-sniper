"""
NBA Stats Client
Pulls team-level efficiency data from stats.nba.com
Handles Season / Last 15 / Last 5 / Last 1 game windows
"""
import requests
import time
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import NBA_STATS_BASE, NBA_HEADERS


@dataclass
class TeamMetrics:
    """Core efficiency metrics for a single time window"""
    team_id: int
    team_name: str
    team_abbr: str
    games_played: int
    wins: int
    losses: int
    off_rating: float      # points per 100 possessions (offense)
    def_rating: float      # points per 100 possessions (defense)
    net_rating: float      # off - def
    pace: float            # possessions per 48 min
    ts_pct: float          # true shooting %
    reb_pct: float         # rebound rate
    tov_pct: float         # turnover rate
    efg_pct: float         # effective FG%
    fg3_pct: float         # 3pt %
    fg3a_rate: float       # 3pt attempt rate
    ft_rate: float         # free throw rate
    opp_efg_pct: float     # opponent eFG%
    window: str            # "season", "last_15", "last_5", "last_1"

    @property
    def record(self) -> str:
        return f"{self.wins}-{self.losses}"


@dataclass
class TeamProfile:
    """All time-window metrics for one team"""
    team_id: int
    team_name: str
    team_abbr: str
    season: Optional[TeamMetrics] = None
    last_15: Optional[TeamMetrics] = None
    last_5: Optional[TeamMetrics] = None
    last_1: Optional[TeamMetrics] = None


class NBAStatsClient:
    """
    Pulls team advanced stats from stats.nba.com

    Usage:
        client = NBAStatsClient(season="2025-26")
        profiles = client.get_all_team_profiles()
        spurs = profiles["SAS"]
        print(spurs.season.off_rating)
        print(spurs.last_15.net_rating)
    """

    def __init__(self, season: str = "2025-26"):
        self.season = season
        self.session = requests.Session()
        self.session.headers.update(NBA_HEADERS)
        self._cache: Dict[str, any] = {}

    def _fetch_team_stats(self, last_n_games: int = 0, measure_type: str = "Advanced") -> List[dict]:
        """
        Pull team stats from leaguedashteamstats endpoint.
        last_n_games=0 means full season.
        """
        cache_key = f"team_stats_{measure_type}_{last_n_games}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        params = {
            "Conference": "",
            "DateFrom": "",
            "DateTo": "",
            "Division": "",
            "GameScope": "",
            "GameSegment": "",
            "Height": "",
            "LastNGames": last_n_games,
            "LeagueID": "00",
            "Location": "",
            "MeasureType": measure_type,
            "Month": 0,
            "OpponentTeamID": 0,
            "Outcome": "",
            "PORound": 0,
            "PaceAdjust": "N",
            "PerMode": "Per100Possessions" if measure_type == "Base" else "PerGame",
            "Period": 0,
            "PlayerExperience": "",
            "PlayerPosition": "",
            "PlusMinus": "N",
            "Rank": "N",
            "Season": self.season,
            "SeasonSegment": "",
            "SeasonType": "Regular Season",
            "ShotClockRange": "",
            "StarterBench": "",
            "TeamID": 0,
            "TwoWay": 0,
            "VsConference": "",
            "VsDivision": "",
        }

        url = f"{NBA_STATS_BASE}/leaguedashteamstats"

        try:
            resp = self.session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[NBA API] Error fetching {measure_type} (last {last_n_games}): {e}")
            return []

        headers = data["resultSets"][0]["headers"]
        rows = data["resultSets"][0]["rowSet"]
        result = [dict(zip(headers, row)) for row in rows]
        self._cache[cache_key] = result

        time.sleep(0.6)  # rate limit courtesy
        return result

    def _parse_team_metrics(self, adv_row: dict, base_row: dict, window: str) -> TeamMetrics:
        """Convert raw API rows into a TeamMetrics object"""
        return TeamMetrics(
            team_id=adv_row.get("TEAM_ID", 0),
            team_name=adv_row.get("TEAM_NAME", ""),
            team_abbr=adv_row.get("TEAM_ABBREVIATION", ""),
            games_played=adv_row.get("GP", 0),
            wins=adv_row.get("W", 0),
            losses=adv_row.get("L", 0),
            off_rating=adv_row.get("OFF_RATING", 0.0),
            def_rating=adv_row.get("DEF_RATING", 0.0),
            net_rating=adv_row.get("NET_RATING", 0.0),
            pace=adv_row.get("PACE", 0.0),
            ts_pct=adv_row.get("TS_PCT", 0.0),
            reb_pct=adv_row.get("REB_PCT", 0.0),
            tov_pct=adv_row.get("TM_TOV_PCT", 0.0),
            efg_pct=base_row.get("EFG_PCT", 0.0) if base_row else 0.0,
            fg3_pct=base_row.get("FG3_PCT", 0.0) if base_row else 0.0,
            fg3a_rate=base_row.get("FG3A_RANK", 0.0) if base_row else 0.0,
            ft_rate=base_row.get("FT_PCT", 0.0) if base_row else 0.0,
            opp_efg_pct=adv_row.get("OPP_EFG_PCT", 0.0),
            window=window,
        )

    def _build_profiles(self, adv_rows: List[dict], base_rows: List[dict], window: str) -> Dict[str, TeamMetrics]:
        """Build TeamMetrics dict keyed by team abbreviation"""
        base_lookup = {r.get("TEAM_ABBREVIATION", ""): r for r in base_rows}
        result = {}
        for row in adv_rows:
            abbr = row.get("TEAM_ABBREVIATION", "")
            base_row = base_lookup.get(abbr, {})
            result[abbr] = self._parse_team_metrics(row, base_row, window)
        return result

    def get_all_team_profiles(self) -> Dict[str, TeamProfile]:
        """
        Main method: returns all 30 NBA teams with metrics across 4 time windows.

        Returns:
            Dict[str, TeamProfile] keyed by team abbreviation (e.g. "SAS", "LAL")
        """
        print("[NBA] Pulling season stats...")
        season_adv = self._fetch_team_stats(last_n_games=0, measure_type="Advanced")
        season_base = self._fetch_team_stats(last_n_games=0, measure_type="Base")

        print("[NBA] Pulling last 15 games...")
        l15_adv = self._fetch_team_stats(last_n_games=15, measure_type="Advanced")
        l15_base = self._fetch_team_stats(last_n_games=15, measure_type="Base")

        print("[NBA] Pulling last 5 games...")
        l5_adv = self._fetch_team_stats(last_n_games=5, measure_type="Advanced")
        l5_base = self._fetch_team_stats(last_n_games=5, measure_type="Base")

        print("[NBA] Pulling last game...")
        l1_adv = self._fetch_team_stats(last_n_games=1, measure_type="Advanced")
        l1_base = self._fetch_team_stats(last_n_games=1, measure_type="Base")

        season_map = self._build_profiles(season_adv, season_base, "season")
        l15_map = self._build_profiles(l15_adv, l15_base, "last_15")
        l5_map = self._build_profiles(l5_adv, l5_base, "last_5")
        l1_map = self._build_profiles(l1_adv, l1_base, "last_1")

        profiles: Dict[str, TeamProfile] = {}
        for abbr in season_map:
            profiles[abbr] = TeamProfile(
                team_id=season_map[abbr].team_id,
                team_name=season_map[abbr].team_name,
                team_abbr=abbr,
                season=season_map.get(abbr),
                last_15=l15_map.get(abbr),
                last_5=l5_map.get(abbr),
                last_1=l1_map.get(abbr),
            )

        print(f"[NBA] Loaded {len(profiles)} team profiles")
        return profiles


# ─────────────────────────────────────────────
# QUICK TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    client = NBAStatsClient(season="2025-26")
    profiles = client.get_all_team_profiles()

    # Example: Spurs
    if "SAS" in profiles:
        sas = profiles["SAS"]
        print(f"\n{'='*50}")
        print(f"  {sas.team_name}")
        print(f"{'='*50}")
        for label, m in [("Season", sas.season), ("Last 15", sas.last_15),
                          ("Last 5", sas.last_5), ("Last Game", sas.last_1)]:
            if m:
                print(f"  {label:10s} | {m.record:6s} | ORtg {m.off_rating:6.1f} | DRtg {m.def_rating:6.1f} | Net {m.net_rating:+6.1f} | Pace {m.pace:5.1f}")
