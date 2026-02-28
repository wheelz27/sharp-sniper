"""
EdgeIntel — Betting Intelligence Engine
Configuration & Settings
"""
import os
from dataclasses import dataclass, field
from typing import Dict

# ─────────────────────────────────────────────
# API KEYS (set these in your environment)
# ─────────────────────────────────────────────
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "")          # https://the-odds-api.com (free tier = 500 reqs/month)
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))

# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "db", "edge_intel.db")

# ─────────────────────────────────────────────
# TIME-WEIGHTED RATING MODEL
# Weights must sum to 1.0
# Tune these after backtesting — start conservative
# ─────────────────────────────────────────────
@dataclass
class RatingWeights:
    season: float = 0.55
    last_15: float = 0.25
    last_5: float = 0.15
    last_game: float = 0.05

    def validate(self):
        total = self.season + self.last_15 + self.last_5 + self.last_game
        assert abs(total - 1.0) < 0.001, f"Weights must sum to 1.0, got {total}"

NBA_WEIGHTS = RatingWeights(season=0.55, last_15=0.25, last_5=0.15, last_game=0.05)
NCAAB_WEIGHTS = RatingWeights(season=0.60, last_15=0.22, last_5=0.13, last_game=0.05)

# ─────────────────────────────────────────────
# HOME COURT ADVANTAGE (points)
# ─────────────────────────────────────────────
HOME_COURT = {
    "nba": 2.5,       # ~2-3 pts historically, declining
    "ncaab": 3.3,     # stronger in college, varies by venue
}

# ─────────────────────────────────────────────
# EDGE THRESHOLDS
# Only flag picks above these minimums
# ─────────────────────────────────────────────
@dataclass
class EdgeThresholds:
    min_edge_points: float = 1.5       # minimum spread edge to flag
    strong_edge_points: float = 3.0    # "strong" edge
    min_ev_pct: float = 3.0            # minimum EV% to flag
    max_plays_per_day: int = 5         # discipline cap

NBA_THRESHOLDS = EdgeThresholds(min_edge_points=1.5, strong_edge_points=3.0)
NCAAB_THRESHOLDS = EdgeThresholds(min_edge_points=2.0, strong_edge_points=4.0)  # softer market = higher bar

# ─────────────────────────────────────────────
# ODDS API SETTINGS
# ─────────────────────────────────────────────
ODDS_API_BASE = "https://api.the-odds-api.com/v4"
ODDS_REGIONS = "us"
ODDS_MARKETS = "spreads,totals,h2h"
ODDS_BOOKMAKERS = "fanduel,draftkings,betmgm,caesars"  # sharp-ish US books

# ─────────────────────────────────────────────
# NBA API SETTINGS
# ─────────────────────────────────────────────
NBA_STATS_BASE = "https://stats.nba.com/stats"
NBA_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nba.com/",
    "Accept": "application/json",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
}

# ─────────────────────────────────────────────
# BARTTORVIK (NCAAB) SETTINGS
# ─────────────────────────────────────────────
BARTTORVIK_BASE = "https://barttorvik.com"

# ─────────────────────────────────────────────
# CONFIDENCE TIERS
# Maps edge size to human-readable confidence
# ─────────────────────────────────────────────
def get_confidence_tier(edge_points: float, sport: str = "nba") -> str:
    thresholds = NBA_THRESHOLDS if sport == "nba" else NCAAB_THRESHOLDS
    if edge_points >= thresholds.strong_edge_points * 1.5:
        return "🔥 HIGH"
    elif edge_points >= thresholds.strong_edge_points:
        return "✅ STRONG"
    elif edge_points >= thresholds.min_edge_points:
        return "⚡ MODERATE"
    else:
        return "⚪ LOW"
