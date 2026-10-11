"""Serializable game-state structures for the Solara UI."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

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
    EXPERT = "EXPERT"


class Heuristic(str, Enum):
    MANHATTAN = "Manhattan"
    CHEBYSHEV = "Chebyshev"


@dataclass(frozen=True)
class AgentSnapshot:
    name: str
    role: str
    cell: Cell
    path: List[Cell]
    path_length: int
    distance_to_player: int
    target: Optional[Cell]
    open_set_count: int = 0
    closed_set_count: int = 0
    current_node: Optional[Cell] = None
    nodes_explored: int = 0
    recalculations: int = 0
    frozen: bool = False
    # BFS comparison metrics
    bfs_nodes_explored: int = 0
    bfs_path_length: int = 0


@dataclass(frozen=True)
class ScanReport:
    active: bool
    agents: Dict[str, Dict[str, str | int]]


@dataclass(frozen=True)
class GameSnapshot:
    status: GameStatus
    difficulty: Difficulty
    heuristic: Heuristic
    cols: int
    rows: int
    level_index: int
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
    # New fields
    lives: int = 3
    cloak_active: bool = False
    cloak_moves_left: int = 0
    cloak_collected: bool = False
    undo_available: bool = False
    power_up_cell: Optional[Cell] = None
    scan: ScanReport = field(default_factory=lambda: ScanReport(False, {}))
