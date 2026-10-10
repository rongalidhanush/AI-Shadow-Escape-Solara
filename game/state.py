"""Serializable game-state structures for the Solara UI."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple

Cell = Tuple[int, int]


class GameStatus(str, Enum):
    MENU = "READY"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    WON = "MISSION COMPLETE"
    LOST = "MISSION FAILED"


class Difficulty(str, Enum):
    EASY = "EASY"
    NORMAL = "NORMAL"
    HARD = "HARD"


@dataclass(frozen=True)
class AgentSnapshot:
    name: str
    role: str
    cell: Cell
    path: List[Cell]
    path_length: int
    distance_to_player: int
    target: Cell | None
    open_set_count: int = 0
    closed_set_count: int = 0
    current_node: Cell | None = None
    nodes_explored: int = 0
    recalculations: int = 0


@dataclass(frozen=True)
class ScanReport:
    active: bool
    agents: Dict[str, Dict[str, str | int]]


@dataclass(frozen=True)
class GameSnapshot:
    status: GameStatus
    difficulty: Difficulty
    cols: int
    rows: int
    level_name: str
    player: Cell
    exit_cell: Cell
    walls: set[Cell]
    gate_cells: set[Cell]
    closed_gates: set[Cell]
    agents: List[AgentSnapshot]
    score: int
    moves: int
    elapsed_seconds: float
    route_recalculations: int
    obstacle_collisions: int
    gates_changed: int
    scans_used: int
    nearest_distance: int
    danger_label: str
    danger_value: int
    message: str
    lab_mode: bool
    show_paths: bool
    scan: ScanReport = field(default_factory=lambda: ScanReport(False, {}))
