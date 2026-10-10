"""A* pathfinding preserved from the original project and expanded with lab metrics."""

from __future__ import annotations

from dataclasses import dataclass, field
import heapq
from typing import Iterable, List, Set, Tuple

Cell = Tuple[int, int]
DIRECTIONS: tuple[Cell, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))


@dataclass(frozen=True)
class SearchReport:
    """Inspectable A* result used by the lab evaluation panel."""

    path: List[Cell]
    open_set_count: int
    closed_set_count: int
    nodes_explored: int
    current_node: Cell | None
    closed_preview: tuple[Cell, ...] = field(default_factory=tuple)
    open_preview: tuple[Cell, ...] = field(default_factory=tuple)


def manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_search(start: Cell, goal: Cell, blocked: Set[Cell], cols: int, rows: int) -> SearchReport:
    """Run A* using Manhattan distance and return path plus algorithm metrics."""

    if start == goal:
        return SearchReport([start], 1, 0, 0, start, (), (start,))

    frontier: list[tuple[int, int, Cell]] = []
    counter = 0
    heapq.heappush(frontier, (manhattan(start, goal), counter, start))
    came_from: dict[Cell, Cell] = {}
    cost_so_far: dict[Cell, int] = {start: 0}
    closed: list[Cell] = []
    current: Cell | None = None

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in closed:
            continue
        closed.append(current)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return SearchReport(
                path=path,
                open_set_count=len(frontier),
                closed_set_count=len(closed),
                nodes_explored=len(closed),
                current_node=path[-1],
                closed_preview=tuple(closed[-8:]),
                open_preview=tuple(item[2] for item in frontier[:8]),
            )

        for dx, dy in DIRECTIONS:
            nxt = (current[0] + dx, current[1] + dy)
            if not (0 <= nxt[0] < cols and 0 <= nxt[1] < rows):
                continue
            if nxt in blocked:
                continue
            new_cost = cost_so_far[current] + 1
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                came_from[nxt] = current
                counter += 1
                priority = new_cost + manhattan(nxt, goal)
                heapq.heappush(frontier, (priority, counter, nxt))

    return SearchReport(
        path=[],
        open_set_count=0,
        closed_set_count=len(closed),
        nodes_explored=len(closed),
        current_node=current,
        closed_preview=tuple(closed[-8:]),
        open_preview=(),
    )


def astar(start: Cell, goal: Cell, blocked: Set[Cell], cols: int, rows: int) -> List[Cell]:
    """Compatibility wrapper matching the original project API."""

    return astar_search(start, goal, blocked, cols, rows).path


def path_length(path: Iterable[Cell]) -> int:
    return max(0, len(list(path)) - 1)
