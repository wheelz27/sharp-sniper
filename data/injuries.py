"""
Injury Tracker
Fetches injury reports and estimates point impact on team performance.
Uses a simple tiered impact model based on player role.
"""
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class PlayerRole(Enum):
    STAR = "star"           # Top 1-2 players (~3-5 pt impact)
    STARTER = "starter"     # Starting 5 (~1-2.5 pt impact)
    ROTATION = "rotation"   # 6th-9th man (~0.5-1.5 pt impact)
    BENCH = "bench"         # End of bench (~0-0.5 pt impact)


class InjuryStatus(Enum):
    OUT = "out"
    DOUBTFUL = "doubtful"
    QUESTIONABLE = "questionable"
    PROBABLE = "probable"
    HEALTHY = "healthy"


# Probability multiplier: how likely they actually miss
STATUS_MISS_PROB = {
    InjuryStatus.OUT: 1.0,
    InjuryStatus.DOUBTFUL: 0.80,
    InjuryStatus.QUESTIONABLE: 0.45,
    InjuryStatus.PROBABLE: 0.15,
    InjuryStatus.HEALTHY: 0.0,
}

# Base point impact by role (spread adjustment in points)
ROLE_IMPACT = {
    PlayerRole.STAR: 4.0,
    PlayerRole.STARTER: 2.0,
    PlayerRole.ROTATION: 1.0,
    PlayerRole.BENCH: 0.3,
}


@dataclass
class InjuryEntry:
    player_name: str
    team: str
    status: InjuryStatus
    role: PlayerRole
    reason: str = ""

    @property
    def expected_impact(self) -> float:
        """Expected spread impact in points (negative = hurts team)"""
        miss_prob = STATUS_MISS_PROB[self.status]
        base = ROLE_IMPACT[self.role]
        return round(-1 * miss_prob * base, 2)


class InjuryTracker:
    """
    Tracks injuries and computes estimated spread impact per team.

    Since real-time injury APIs are limited/paid, this supports:
    1. Manual entry (recommended — you control the data)
    2. Basic web scrape (ESPN/Rotowire — may break)

    Usage:
        tracker = InjuryTracker()

        # Manual entry
        tracker.add_injury("Victor Wembanyama", "SAS", InjuryStatus.OUT, PlayerRole.STAR, "knee")
        tracker.add_injury("Some Bench Guy", "SAS", InjuryStatus.OUT, PlayerRole.BENCH)

        # Get total team impact
        impact = tracker.get_team_impact("SAS")
        # Returns: -4.3 (points of spread adjustment)

        # Or get impact differential for a matchup
        diff = tracker.get_matchup_impact("SAS", "LAL")
    """

    def __init__(self):
        self.injuries: Dict[str, List[InjuryEntry]] = {}  # keyed by team

    def add_injury(self, player: str, team: str, status: InjuryStatus,
                   role: PlayerRole, reason: str = ""):
        """Add an injury entry"""
        entry = InjuryEntry(
            player_name=player,
            team=team.upper(),
            status=status,
            role=role,
            reason=reason,
        )
        if team.upper() not in self.injuries:
            self.injuries[team.upper()] = []

        # Update existing or add new
        existing = [i for i in self.injuries[team.upper()] if i.player_name == player]
        if existing:
            self.injuries[team.upper()].remove(existing[0])
        self.injuries[team.upper()].append(entry)

    def remove_injury(self, player: str, team: str):
        """Remove a player from injury list (they're healthy)"""
        team = team.upper()
        if team in self.injuries:
            self.injuries[team] = [i for i in self.injuries[team] if i.player_name != player]

    def clear_team(self, team: str):
        """Clear all injuries for a team"""
        self.injuries[team.upper()] = []

    def clear_all(self):
        """Reset all injuries"""
        self.injuries = {}

    def get_team_impact(self, team: str) -> float:
        """
        Total expected spread impact for a team's injuries.
        Returns negative number (injuries hurt team).
        """
        team = team.upper()
        if team not in self.injuries:
            return 0.0
        return sum(entry.expected_impact for entry in self.injuries[team])

    def get_matchup_impact(self, team_a: str, team_b: str) -> float:
        """
        Net injury impact differential (from team_a perspective).
        Positive = team_a has injury advantage.
        Negative = team_a has injury disadvantage.
        """
        impact_a = self.get_team_impact(team_a)  # negative
        impact_b = self.get_team_impact(team_b)  # negative
        # If team B is more injured, that helps team A
        return round(impact_b - impact_a, 2)

    def get_team_injuries(self, team: str) -> List[InjuryEntry]:
        """Get all injury entries for a team"""
        return self.injuries.get(team.upper(), [])

    def get_summary(self, team: str) -> str:
        """Human-readable injury summary for a team"""
        entries = self.get_team_injuries(team)
        if not entries:
            return "No significant injuries"

        lines = []
        for e in sorted(entries, key=lambda x: ROLE_IMPACT[x.role], reverse=True):
            lines.append(f"  {e.player_name} ({e.role.value}) — {e.status.value}"
                        f" [{e.expected_impact:+.1f} pts]"
                        f"{' (' + e.reason + ')' if e.reason else ''}")
        total = self.get_team_impact(team)
        lines.append(f"  Total impact: {total:+.1f} pts")
        return "\n".join(lines)

    def load_from_dict(self, injury_data: Dict[str, List[dict]]):
        """
        Bulk load injuries from a dict structure.

        Example:
            tracker.load_from_dict({
                "SAS": [
                    {"player": "Wembanyama", "status": "out", "role": "star", "reason": "knee"},
                    {"player": "Vassell", "status": "questionable", "role": "starter"},
                ],
                "LAL": [
                    {"player": "Davis", "status": "doubtful", "role": "star", "reason": "back"},
                ],
            })
        """
        status_map = {s.value: s for s in InjuryStatus}
        role_map = {r.value: r for r in PlayerRole}

        for team, players in injury_data.items():
            for p in players:
                self.add_injury(
                    player=p["player"],
                    team=team,
                    status=status_map.get(p.get("status", "out"), InjuryStatus.OUT),
                    role=role_map.get(p.get("role", "rotation"), PlayerRole.ROTATION),
                    reason=p.get("reason", ""),
                )


if __name__ == "__main__":
    tracker = InjuryTracker()

    tracker.load_from_dict({
        "SAS": [
            {"player": "Wembanyama", "status": "out", "role": "star", "reason": "knee"},
        ],
        "LAL": [
            {"player": "Davis", "status": "doubtful", "role": "star", "reason": "back"},
            {"player": "Reaves", "status": "questionable", "role": "starter"},
        ],
    })

    print("=== SAS Injuries ===")
    print(tracker.get_summary("SAS"))
    print(f"\n=== LAL Injuries ===")
    print(tracker.get_summary("LAL"))
    print(f"\nMatchup impact (SAS perspective): {tracker.get_matchup_impact('SAS', 'LAL'):+.1f} pts")
