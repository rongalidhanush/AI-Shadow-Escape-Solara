"""Scoring and threat calculations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Metrics:
    elapsed_seconds: float = 0.0
    player_distance: int = 0
    route_recalculations: int = 0
    obstacle_collisions: int = 0
    capture_time: Optional[float] = None
    successful_escape: bool = False
    gates_changed: int = 0
    scans_used: int = 0
    enemy_steps: int = 0
    # New metrics
    lives_lost: int = 0
    cloak_used: int = 0
    undo_used: int = 0

    def final_score(self, optimal_length: int) -> int:
        if not self.successful_escape:
            return 0
        time_bonus = max(0, int(1500 - self.elapsed_seconds * 9))
        efficiency_bonus = max(0, 700 - max(0, self.player_distance - optimal_length) * 30)
        gate_bonus = self.gates_changed * 15
        lives_bonus = (3 - self.lives_lost) * 200    # +200 per life kept
        cloak_bonus = self.cloak_used * 50            # +50 per cloak used cleverly
        scan_penalty = self.scans_used * 8
        collision_penalty = self.obstacle_collisions * 15
        undo_penalty = self.undo_used * 5
        return max(
            0,
            time_bonus
            + efficiency_bonus
            + gate_bonus
            + lives_bonus
            + cloak_bonus
            - scan_penalty
            - collision_penalty
            - undo_penalty,
        )


def danger_label(nearest_distance: int) -> str:
    if nearest_distance <= 1:
        return "CRITICAL"
    if nearest_distance <= 3:
        return "HIGH"
    if nearest_distance <= 6:
        return "MEDIUM"
    return "LOW"


def danger_value(nearest_distance: int) -> int:
    return max(0, min(100, int((1.0 - nearest_distance / 10.0) * 100)))
