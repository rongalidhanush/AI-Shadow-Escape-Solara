"""Dynamic gate handling."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set, Tuple

Cell = Tuple[int, int]


@dataclass
class GateSystem:
    candidates: Set[Cell] = field(default_factory=set)
    closed: Set[Cell] = field(default_factory=set)
    cursor: int = 0

    def active_count(self) -> int:
        return len(self.closed)

    def ordered_candidates(self) -> list[Cell]:
        return sorted(self.candidates, key=lambda cell: (cell[1], cell[0]))
