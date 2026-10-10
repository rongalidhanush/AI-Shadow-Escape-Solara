"""Procedural solvable maze definitions."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Set, Tuple

from .pathfinding import astar

Cell = Tuple[int, int]


@dataclass(frozen=True)
class LevelSpec:
    name: str
    start: Cell
    safe_zone: Cell
    pursuers: tuple[tuple[Cell, str], ...]
    wall_density: float
    gate_candidates: tuple[Cell, ...]


COLS = 16
ROWS = 13

LEVELS = (
    LevelSpec(
        name="Shadow District",
        start=(1, 1),
        safe_zone=(14, 11),
        pursuers=(((14, 1), "Hunter"), ((1, 11), "Interceptor")),
        wall_density=0.20,
        gate_candidates=((6, 4), (9, 8), (12, 5), (4, 9), (10, 2), (7, 10)),
    ),
)


def generate_walls(spec: LevelSpec, cols: int, rows: int, seed: int | None = None, density: float | None = None) -> Set[Cell]:
    """Generate walls while preserving valid routes for the player and pursuers."""

    rng = random.Random(seed)
    protected = {
        spec.start,
        spec.safe_zone,
        *(cell for cell, _ in spec.pursuers),
        *spec.gate_candidates,
    }
    walls: Set[Cell] = set()
    candidates = [(x, y) for y in range(rows) for x in range(cols) if (x, y) not in protected]
    rng.shuffle(candidates)
    wall_density = spec.wall_density if density is None else density
    target = int(cols * rows * wall_density)

    for cell in candidates:
        if len(walls) >= target:
            break
        walls.add(cell)
        if not astar(spec.start, spec.safe_zone, walls, cols, rows):
            walls.remove(cell)
            continue
        if any(not astar(pursuer_cell, spec.start, walls, cols, rows) for pursuer_cell, _ in spec.pursuers):
            walls.remove(cell)
    return walls
