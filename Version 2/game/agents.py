"""Player and A*-controlled pursuer agents (Hunter, Interceptor, Flanker)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple

from .pathfinding import BFSReport, SearchReport, astar_search, bfs_search

Cell = Tuple[int, int]


@dataclass
class Player:
    cell: Cell
    start_cell: Cell
    moves: int = 0
    blocked_attempts: int = 0
    distance_travelled: int = 0
    last_direction: Cell = (0, 0)
    prev_cell: Optional[Cell] = None  # for undo

    def try_move(self, dx: int, dy: int, walls: Set[Cell], cols: int, rows: int) -> bool:
        target = (self.cell[0] + dx, self.cell[1] + dy)
        if not (0 <= target[0] < cols and 0 <= target[1] < rows) or target in walls:
            self.blocked_attempts += 1
            return False
        self.prev_cell = self.cell
        self.cell = target
        self.last_direction = (dx, dy)
        self.moves += 1
        self.distance_travelled += 1
        return True

    def undo(self) -> bool:
        """Revert to previous cell. Returns True if successful."""
        if self.prev_cell is None:
            return False
        self.cell = self.prev_cell
        self.prev_cell = None
        self.moves = max(0, self.moves - 1)
        self.distance_travelled = max(0, self.distance_travelled - 1)
        return True


@dataclass
class Pursuer:
    name: str
    cell: Cell
    role: str
    color_variant: int = 0
    path: List[Cell] = field(default_factory=list)
    route_recalculations: int = 0
    cells_travelled: int = 0
    last_target: Optional[Cell] = None
    current_target: Optional[Cell] = None
    last_report: Optional[SearchReport] = None
    last_bfs_report: Optional[BFSReport] = None
    frozen: bool = False          # True while Cloak power-up is active
    frozen_moves_left: int = 0

    def recalculate(
        self,
        target: Cell,
        walls: Set[Cell],
        cols: int,
        rows: int,
        others: Optional[Set[Cell]] = None,
        heuristic: str = "Manhattan",
    ) -> SearchReport:
        blocked = set(walls)
        if others:
            blocked.update(others - {self.cell, target})
        blocked.discard(target)
        report = astar_search(self.cell, target, blocked, cols, rows, heuristic)
        bfs_report = bfs_search(self.cell, target, blocked, cols, rows)
        self.path = report.path
        self.last_report = report
        self.last_bfs_report = bfs_report
        self.last_target = target
        self.current_target = target
        self.route_recalculations += 1
        return report

    def move_one_step(
        self,
        target: Cell,
        walls: Set[Cell],
        cols: int,
        rows: int,
        others: Optional[Set[Cell]] = None,
        heuristic: str = "Manhattan",
    ) -> bool:
        if self.frozen:
            self.frozen_moves_left = max(0, self.frozen_moves_left - 1)
            if self.frozen_moves_left == 0:
                self.frozen = False
            return False

        if self.last_target != target or len(self.path) < 2 or self.path[0] != self.cell:
            self.recalculate(target, walls, cols, rows, others, heuristic)
        if len(self.path) < 2:
            return False
        next_cell = self.path[1]
        if next_cell in walls:
            self.recalculate(target, walls, cols, rows, others, heuristic)
            if len(self.path) < 2:
                return False
            next_cell = self.path[1]
        self.cell = next_cell
        self.path = self.path[1:]
        self.cells_travelled += 1
        return True

    def freeze(self, moves: int) -> None:
        """Freeze this pursuer for `moves` player moves (Cloak effect)."""
        self.frozen = True
        self.frozen_moves_left = moves
