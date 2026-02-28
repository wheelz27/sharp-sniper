"""
NCAAB Stats Client
Pulls team-level efficiency data from Barttorvik (barttorvik.com)
Also supports manual CSV import from KenPom exports
"""
import requests
import csv
import io
import time
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import BARTTORVIK_BASE


@dataclass
class NCAABTeamMetrics:
    """Core efficiency metrics for a single NCAAB time window"""
    team_name: str
    conf: str
    games_played: int
    wins: int
    losses: int
    adj_off: float         # adjusted offensive efficiency
    adj_def: float         # adjusted defensive efficiency
    adj_net: float         # adj_off - adj_def (Barttorvik "Barthag" proxy)
    tempo: float           # adjusted tempo (possessions per 40 min)
    efg_pct: float         # effective FG%
    opp_efg_pct: float     # opponent eFG%
    tov_pct: float         # turnover %
    opp_tov_pct: float     # forced turnover %
    orb_pct: float         # offensive rebound %
    ft_rate: float         # FTA / FGA
    fg3_pct: float         # 3pt %
    fg3a_rate: float       # 3pt attempt rate
    window: str            # "season", "last_15", "last_5", "last_1"

    @property
    def record(self) -> str:
        return f"{self.wins}-{self.losses}"


@dataclass
class NCAABTeamProfile:
    """All time-window metrics for one NCAAB team"""
    team_name: str
    conf: str
    season: Optional[NCAABTeamMetrics] = None
    last_15: Optional[NCAABTeamMetrics] = None
    last_5: Optional[NCAABTeamMetrics] = None
    last_1: Optional[NCAABTeamMetrics] = None


class NCAABStatsClient:
    """
    Pulls NCAAB team efficiency data.

    Primary: Barttorvik API/CSV endpoints
    Fallback: Manual CSV import (KenPom export)

    Usage:
        client = NCAABStatsClient(season=2026)
        profiles = client.get_all_team_profiles()
        duke = profiles.get("Duke")
    """

    def __init__(self, season: int = 2026):
        self.season = season
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self._cache: Dict[str, any] = {}

    def _fetch_barttorvik_data(self, start_date: str = "", end_date: str = "") -> List[dict]:
        """
        Fetch team data from Barttorvik's getteamdata endpoint.
        Dates in YYYYMMDD format. Empty = full season.
        """
        cache_key = f"bart_{start_date}_{end_date}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        url = f"{BARTTORVIK_BASE}/team-tables-json"
        params = {
            "year": self.season,
            "conyes": "All",
            "type": "pointed",
        }
        if start_date:
            params["start"] = start_date
        if end_date:
            params["end"] = end_date

        try:
            resp = self.session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[NCAAB/Barttorvik] Error: {e}")
            return []

        self._cache[cache_key] = data
        time.sleep(0.5)
        return data

    def _parse_barttorvik_row(self, row: list, window: str) -> NCAABTeamMetrics:
        """
        Parse a Barttorvik JSON row into NCAABTeamMetrics.
        Row format varies — this handles the common 'pointed' type layout.
        Indices may shift with site updates; adjust as needed.
        """
        try:
            return NCAABTeamMetrics(
                team_name=str(row[0]) if len(row) > 0 else "",
                conf=str(row[1]) if len(row) > 1 else "",
                games_played=int(row[3]) if len(row) > 3 else 0,
                wins=int(row[3]) if len(row) > 3 else 0,  # approximate
                losses=0,
                adj_off=float(row[5]) if len(row) > 5 else 0.0,
                adj_def=float(row[7]) if len(row) > 7 else 0.0,
                adj_net=float(row[5]) - float(row[7]) if len(row) > 7 else 0.0,
                tempo=float(row[9]) if len(row) > 9 else 0.0,
                efg_pct=float(row[11]) if len(row) > 11 else 0.0,
                opp_efg_pct=float(row[12]) if len(row) > 12 else 0.0,
                tov_pct=float(row[13]) if len(row) > 13 else 0.0,
                opp_tov_pct=float(row[14]) if len(row) > 14 else 0.0,
                orb_pct=float(row[15]) if len(row) > 15 else 0.0,
                ft_rate=float(row[17]) if len(row) > 17 else 0.0,
                fg3_pct=float(row[18]) if len(row) > 18 else 0.0,
                fg3a_rate=float(row[19]) if len(row) > 19 else 0.0,
                window=window,
            )
        except (ValueError, IndexError) as e:
            print(f"[NCAAB] Parse error: {e}")
            return None

    def load_from_csv(self, filepath: str, window: str = "season") -> Dict[str, NCAABTeamMetrics]:
        """
        Load team metrics from a KenPom or Barttorvik CSV export.
        Expects headers: Team, Conf, AdjOE, AdjDE, AdjTempo, eFG%, OppeFG%, etc.

        Usage:
            metrics = client.load_from_csv("kenpom_export.csv", window="season")
        """
        metrics = {}
        try:
            with open(filepath, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get("Team", row.get("team", "")).strip()
                    if not name:
                        continue
                    adj_off = float(row.get("AdjOE", row.get("AdjO", 0)))
                    adj_def = float(row.get("AdjDE", row.get("AdjD", 0)))
                    metrics[name] = NCAABTeamMetrics(
                        team_name=name,
                        conf=row.get("Conf", row.get("conf", "")),
                        games_played=int(row.get("W", 0)) + int(row.get("L", 0)),
                        wins=int(row.get("W", 0)),
                        losses=int(row.get("L", 0)),
                        adj_off=adj_off,
                        adj_def=adj_def,
                        adj_net=adj_off - adj_def,
                        tempo=float(row.get("AdjTempo", row.get("Tempo", 0))),
                        efg_pct=float(row.get("eFG%", row.get("EFG", 0))),
                        opp_efg_pct=float(row.get("OppeFG%", row.get("OEFG", 0))),
                        tov_pct=float(row.get("TO%", row.get("TOV", 0))),
                        opp_tov_pct=float(row.get("OppTO%", row.get("OTOV", 0))),
                        orb_pct=float(row.get("OR%", row.get("ORB", 0))),
                        ft_rate=float(row.get("FTRate", row.get("FTR", 0))),
                        fg3_pct=float(row.get("3P%", row.get("FG3", 0))),
                        fg3a_rate=float(row.get("3PA%", row.get("FG3A", 0))),
                        window=window,
                    )
        except Exception as e:
            print(f"[NCAAB] CSV load error: {e}")
        return metrics

    def get_all_team_profiles(self) -> Dict[str, NCAABTeamProfile]:
        """
        Main method: returns NCAAB teams with metrics across time windows.
        Uses Barttorvik API. Falls back gracefully if data unavailable.
        """
        from datetime import datetime, timedelta

        today = datetime.now()
        season_start = f"{self.season - 1}1101"  # Nov 1 of prior year

        # Date ranges for windows
        dates = {
            "season": ("", ""),  # full season
            "last_15": ((today - timedelta(days=30)).strftime("%Y%m%d"), today.strftime("%Y%m%d")),
            "last_5": ((today - timedelta(days=12)).strftime("%Y%m%d"), today.strftime("%Y%m%d")),
        }

        profiles: Dict[str, NCAABTeamProfile] = {}

        for window, (start, end) in dates.items():
            print(f"[NCAAB] Pulling {window} stats...")
            rows = self._fetch_barttorvik_data(start_date=start, end_date=end)

            for row in rows:
                metrics = self._parse_barttorvik_row(row, window)
                if metrics is None:
                    continue

                name = metrics.team_name
                if name not in profiles:
                    profiles[name] = NCAABTeamProfile(
                        team_name=name,
                        conf=metrics.conf,
                    )

                setattr(profiles[name], window, metrics)

        print(f"[NCAAB] Loaded {len(profiles)} team profiles")
        return profiles


if __name__ == "__main__":
    client = NCAABStatsClient(season=2026)
    profiles = client.get_all_team_profiles()

    for name, p in list(profiles.items())[:5]:
        if p.season:
            print(f"{name:25s} | AdjO {p.season.adj_off:6.1f} | AdjD {p.season.adj_def:6.1f} | Net {p.season.adj_net:+6.1f}")
