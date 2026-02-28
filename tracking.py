"""
Pick Tracker
SQLite-backed system for logging picks, results, and computing performance metrics.

Tracks:
  - Every pick with line taken, closing line, result
  - ROI over time
  - CLV (Closing Line Value) - the single best predictor of long-term edge
  - Win rate by confidence tier
  - Units gained/lost
"""
import sqlite3
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import DB_PATH


@dataclass
class PickRecord:
    id: int
    timestamp: str
    sport: str
    away_team: str
    home_team: str
    play_side: str          # "HOME", "AWAY"
    bet_type: str           # "spread", "total_over", "total_under", "ml"
    line_taken: float       # spread or total at time of pick
    odds_taken: int         # american odds
    closing_line: float     # line at game start
    model_spread: float
    market_spread: float
    edge_points: float
    confidence: str
    units: float
    result: str             # "win", "loss", "push", "pending"
    profit_units: float     # units won/lost
    clv: float              # closing line value (positive = beat close)
    notes: str


class PickTracker:
    """
    Tracks all picks with full transparency metrics.

    Usage:
        tracker = PickTracker()

        # Log a pick
        pick_id = tracker.log_pick(
            sport="nba",
            away_team="LAL",
            home_team="SAS",
            play_side="HOME",
            bet_type="spread",
            line_taken=-4.0,
            odds_taken=-110,
            model_spread=-6.5,
            market_spread=-4.0,
            edge_points=2.5,
            confidence="✅ STRONG",
            units=1.0,
            notes="Spurs 11-0 run, net rating structural shift"
        )

        # Update result after game
        tracker.update_result(pick_id, closing_line=-5.5, result="win")

        # Get performance report
        report = tracker.get_performance_report()
    """

    def __init__(self, db_path: str = None):
        self.db_path = db_path or DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS picks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                sport TEXT NOT NULL,
                away_team TEXT NOT NULL,
                home_team TEXT NOT NULL,
                play_side TEXT NOT NULL,
                bet_type TEXT NOT NULL DEFAULT 'spread',
                line_taken REAL NOT NULL,
                odds_taken INTEGER NOT NULL DEFAULT -110,
                closing_line REAL DEFAULT NULL,
                model_spread REAL NOT NULL,
                market_spread REAL NOT NULL,
                edge_points REAL NOT NULL,
                confidence TEXT NOT NULL,
                units REAL NOT NULL DEFAULT 1.0,
                result TEXT NOT NULL DEFAULT 'pending',
                profit_units REAL DEFAULT 0.0,
                clv REAL DEFAULT 0.0,
                notes TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_summary (
                date TEXT PRIMARY KEY,
                sport TEXT,
                total_picks INTEGER,
                wins INTEGER,
                losses INTEGER,
                pushes INTEGER,
                units_wagered REAL,
                units_profit REAL,
                roi_pct REAL,
                avg_clv REAL
            )
        """)
        conn.commit()
        conn.close()

    def log_pick(self, sport: str, away_team: str, home_team: str,
                 play_side: str, bet_type: str, line_taken: float,
                 odds_taken: int, model_spread: float, market_spread: float,
                 edge_points: float, confidence: str, units: float = 1.0,
                 notes: str = "") -> int:
        """Log a new pick. Returns pick ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            INSERT INTO picks (timestamp, sport, away_team, home_team, play_side,
                             bet_type, line_taken, odds_taken, model_spread,
                             market_spread, edge_points, confidence, units, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            sport, away_team, home_team, play_side, bet_type,
            line_taken, odds_taken, model_spread, market_spread,
            edge_points, confidence, units, notes,
        ))
        pick_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"[TRACKER] Logged pick #{pick_id}: {play_side} {home_team if play_side == 'HOME' else away_team} {line_taken}")
        return pick_id

    def update_result(self, pick_id: int, closing_line: float, result: str):
        """
        Update a pick with its result after the game.

        Args:
            pick_id: pick ID from log_pick()
            closing_line: the spread at game start (for CLV calculation)
            result: "win", "loss", or "push"
        """
        conn = sqlite3.connect(self.db_path)

        # Get the pick
        row = conn.execute("SELECT * FROM picks WHERE id = ?", (pick_id,)).fetchone()
        if not row:
            print(f"[TRACKER] Pick #{pick_id} not found")
            conn.close()
            return

        line_taken = row[7]   # line_taken
        odds_taken = row[8]   # odds_taken
        units = row[14]       # units

        # Calculate CLV (positive = we got a better line than close)
        clv = closing_line - line_taken  # if line moved our way, CLV is positive

        # Calculate profit
        if result == "win":
            if odds_taken > 0:
                profit = units * (odds_taken / 100)
            else:
                profit = units * (100 / abs(odds_taken))
        elif result == "loss":
            profit = -units
        else:  # push
            profit = 0.0

        conn.execute("""
            UPDATE picks SET closing_line = ?, result = ?, profit_units = ?, clv = ?
            WHERE id = ?
        """, (closing_line, result, round(profit, 2), round(clv, 2), pick_id))
        conn.commit()
        conn.close()
        print(f"[TRACKER] Updated pick #{pick_id}: {result} ({profit:+.2f}u, CLV: {clv:+.1f})")

    def get_pending_picks(self) -> List[PickRecord]:
        """Get all picks that haven't been graded yet"""
        return self._query_picks("WHERE result = 'pending'")

    def get_recent_picks(self, days: int = 7) -> List[PickRecord]:
        """Get picks from the last N days"""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        return self._query_picks(f"WHERE timestamp > '{cutoff}' ORDER BY timestamp DESC")

    def _query_picks(self, where_clause: str = "") -> List[PickRecord]:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(f"SELECT * FROM picks {where_clause}").fetchall()
        conn.close()
        return [PickRecord(
            id=r[0], timestamp=r[1], sport=r[2], away_team=r[3], home_team=r[4],
            play_side=r[5], bet_type=r[6], line_taken=r[7], odds_taken=r[8],
            closing_line=r[9] or 0, model_spread=r[10], market_spread=r[11],
            edge_points=r[12], confidence=r[13], units=r[14], result=r[15],
            profit_units=r[16] or 0, clv=r[17] or 0, notes=r[18] or "",
        ) for r in rows]

    def get_performance_report(self, sport: str = None, days: int = None) -> Dict:
        """
        Generate comprehensive performance report.

        Returns dict with:
            total_picks, wins, losses, pushes, win_rate,
            units_wagered, units_profit, roi_pct,
            avg_clv, clv_positive_rate,
            by_confidence (breakdown by tier),
            streak (current W/L streak)
        """
        where_parts = ["result != 'pending'"]
        if sport:
            where_parts.append(f"sport = '{sport}'")
        if days:
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            where_parts.append(f"timestamp > '{cutoff}'")

        where = "WHERE " + " AND ".join(where_parts)
        picks = self._query_picks(where + " ORDER BY timestamp ASC")

        if not picks:
            return {"total_picks": 0, "message": "No graded picks yet"}

        wins = sum(1 for p in picks if p.result == "win")
        losses = sum(1 for p in picks if p.result == "loss")
        pushes = sum(1 for p in picks if p.result == "push")
        total = wins + losses + pushes

        units_wagered = sum(p.units for p in picks)
        units_profit = sum(p.profit_units for p in picks)
        roi_pct = (units_profit / units_wagered * 100) if units_wagered > 0 else 0

        clv_values = [p.clv for p in picks if p.clv != 0]
        avg_clv = sum(clv_values) / len(clv_values) if clv_values else 0
        clv_positive = sum(1 for c in clv_values if c > 0)
        clv_rate = (clv_positive / len(clv_values) * 100) if clv_values else 0

        # By confidence tier
        by_confidence = {}
        for p in picks:
            tier = p.confidence
            if tier not in by_confidence:
                by_confidence[tier] = {"picks": 0, "wins": 0, "profit": 0.0}
            by_confidence[tier]["picks"] += 1
            if p.result == "win":
                by_confidence[tier]["wins"] += 1
            by_confidence[tier]["profit"] += p.profit_units

        # Current streak
        streak = 0
        streak_type = ""
        for p in reversed(picks):
            if p.result == "push":
                continue
            if not streak_type:
                streak_type = p.result
                streak = 1
            elif p.result == streak_type:
                streak += 1
            else:
                break

        return {
            "total_picks": total,
            "wins": wins,
            "losses": losses,
            "pushes": pushes,
            "win_rate": round(wins / (wins + losses) * 100, 1) if (wins + losses) > 0 else 0,
            "units_wagered": round(units_wagered, 1),
            "units_profit": round(units_profit, 2),
            "roi_pct": round(roi_pct, 2),
            "avg_clv": round(avg_clv, 2),
            "clv_positive_rate": round(clv_rate, 1),
            "by_confidence": by_confidence,
            "streak": f"{streak}{'W' if streak_type == 'win' else 'L'}" if streak > 0 else "0",
        }

    def format_performance_report(self, sport: str = None, days: int = None) -> str:
        """Human-readable performance report"""
        r = self.get_performance_report(sport, days)
        if r.get("total_picks", 0) == 0:
            return "No graded picks yet."

        period = f"Last {days} days" if days else "All Time"
        sport_label = sport.upper() if sport else "ALL SPORTS"

        lines = [
            f"{'='*50}",
            f"  PERFORMANCE REPORT — {sport_label} ({period})",
            f"{'='*50}",
            f"",
            f"  Record:    {r['wins']}-{r['losses']}-{r['pushes']} ({r['win_rate']}%)",
            f"  Units:     {r['units_profit']:+.2f}u on {r['units_wagered']:.1f}u wagered",
            f"  ROI:       {r['roi_pct']:+.2f}%",
            f"  Avg CLV:   {r['avg_clv']:+.2f} pts ({r['clv_positive_rate']:.0f}% positive)",
            f"  Streak:    {r['streak']}",
            f"",
        ]

        if r.get("by_confidence"):
            lines.append("  By Confidence:")
            for tier, stats in r["by_confidence"].items():
                wr = round(stats['wins'] / stats['picks'] * 100) if stats['picks'] > 0 else 0
                lines.append(f"    {tier}: {stats['picks']} picks, {wr}% win, {stats['profit']:+.1f}u")

        return "\n".join(lines)
