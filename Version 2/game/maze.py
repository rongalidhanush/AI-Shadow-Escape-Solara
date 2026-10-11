"""Procedural solvable maze definitions — 3 levels with power-up candidates."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Optional, Set, Tuple

from .pathfinding import astar

Cell = Tuple[int, int]


@dataclass(frozen=True)
class LevelSpec:
    name: str
    cols: int
    rows: int
    start: Cell
    safe_zone: Cell
    pursuers: tuple[tuple[Cell, str], ...]
    wall_density: float
    gate_candidates: tuple[Cell, ...]
    power_up_candidates: tuple[Cell, ...]


# ── Level 1: Shadow District ─────────────────────────────────────────────────
# Classic 16×13 grid — the original level, retained exactly
_L1 = LevelSpec(
    name="Shadow District",
    cols=16,
    rows=13,
    start=(1, 1),
    safe_zone=(14, 11),
    pursuers=(
        ((14, 1), "Hunter"),
        ((1, 11), "Interceptor"),
        ((7, 6), "Flanker"),
    ),
    wall_density=0.20,
    gate_candidates=((6, 4), (9, 8), (12, 5), (4, 9), (10, 2), (7, 10)),
    power_up_candidates=((4, 4), (11, 3), (8, 8), (3, 9), (12, 9)),
)

# ── Level 2: Neon Labyrinth ───────────────────────────────────────────────────
# Larger 18×15 grid — more corridors, more gates, denser maze
_L2 = LevelSpec(
    name="Neon Labyrinth",
    cols=18,
    rows=15,
    start=(1, 1),
    safe_zone=(16, 13),
    pursuers=(
        ((16, 1), "Hunter"),
        ((1, 13), "Interceptor"),
        ((9, 7), "Flanker"),
    ),
    wall_density=0.23,
    gate_candidates=((5, 3), (12, 4), (8, 7), (4, 10), (13, 10), (7, 12), (10, 6), (15, 7)),
    power_up_candidates=((4, 3), (13, 3), (9, 5), (5, 11), (13, 12), (8, 9)),
)

# ── Level 3: Blacksite ────────────────────────────────────────────────────────
# Largest 20×16 grid — highest density, most hostile
_L3 = LevelSpec(
    name="Blacksite",
    cols=20,
    rows=16,
    start=(1, 1),
    safe_zone=(18, 14),
    pursuers=(
        ((18, 1), "Hunter"),
        ((1, 14), "Interceptor"),
        ((10, 8), "Flanker"),
    ),
    wall_density=0.26,
    gate_candidates=(
        (5, 3), (14, 3), (9, 5), (4, 8), (15, 8),
        (7, 11), (12, 11), (9, 13), (16, 6), (3, 12),
    ),
    power_up_candidates=((5, 5), (14, 5), (10, 8), (4, 12), (15, 11), (9, 3), (8, 13)),
)

LEVELS = (_L1, _L2, _L3)

# Keep module-level COLS/ROWS pointing at level 1 defaults for compatibility
COLS = _L1.cols
ROWS = _L1.rows


def generate_walls(
    spec: LevelSpec,
    seed: Optional[int] = None,
    density: Optional[float] = None,
) -> Set[Cell]:
    """Generate walls while preserving valid routes for the player and pursuers."""

    cols, rows = spec.cols, spec.rows
    rng = random.Random(seed)
    protected = {
        spec.start,
        spec.safe_zone,
        *(cell for cell, _ in spec.pursuers),
        *spec.gate_candidates,
        *spec.power_up_candidates,
    }
    walls: Set[Cell] = set()
    candidates = [
        (x, y) for y in range(rows) for x in range(cols) if (x, y) not in protected
    ]
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
        if any(
            not astar(pursuer_cell, spec.start, walls, cols, rows)
            for pursuer_cell, _ in spec.pursuers
        ):
            walls.remove(cell)
    return walls
