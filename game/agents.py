"""Player and A* controlled pursuer agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Set, Tuple

from .pathfinding import SearchReport, astar_search

Cell = Tuple[int, int]


@dataclass
class Player:
    cell: Cell
    start_cell: Cell
    moves: int = 0
    blocked_attempts: int = 0
    distance_travelled: int = 0
    last_direction: Cell = (0, 0)

    def try_move(self, dx: int, dy: int, walls: Set[Cell], cols: int, rows: int) -> bool:
        target = (self.cell[0] + dx, self.cell[1] + dy)
        if not (0 <= target[0] < cols and 0 <= target[1] < rows) or target in walls:
            self.blocked_attempts += 1
            return False
        self.cell = target
        self.last_direction = (dx, dy)
        self.moves += 1
        self.distance_travelled += 1
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
    last_target: Cell | None = None
    current_target: Cell | None = None
    last_report: SearchReport | None = None

    def recalculate(
        self,
        target: Cell,
        walls: Set[Cell],
        cols: int,
        rows: int,
        others: Set[Cell] | None = None,
    ) -> SearchReport:
        blocked = set(walls)
        if others:
            blocked.update(others - {self.cell, target})
        blocked.discard(target)
        report = astar_search(self.cell, target, blocked, cols, rows)
        self.path = report.path
        self.last_report = report
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
        others: Set[Cell] | None = None,
    ) -> bool:
        if self.last_target != target or len(self.path) < 2 or self.path[0] != self.cell:
            self.recalculate(target, walls, cols, rows, others)
        if len(self.path) < 2:
            return False
        next_cell = self.path[1]
        if next_cell in walls:
            self.recalculate(target, walls, cols, rows, others)
            if len(self.path) < 2:
                return False
            next_cell = self.path[1]
        self.cell = next_cell
        self.path = self.path[1:]
        self.cells_travelled += 1
        return True
