"""Game board renderer."""

from __future__ import annotations

import html

import solara

from game.state import GameSnapshot


def _cell_classes(snapshot: GameSnapshot, cell: tuple[int, int]) -> tuple[str, str]:
    classes = ["ase-cell", "floor-a" if (cell[0] + cell[1]) % 2 == 0 else "floor-b"]
    label = ""

    hunter_path = set(snapshot.agents[0].path[1:]) if snapshot.agents else set()
    interceptor_path = set(snapshot.agents[1].path[1:]) if len(snapshot.agents) > 1 else set()
    if snapshot.show_paths and cell in hunter_path:
        classes.append("path-hunter")
    if snapshot.show_paths and cell in interceptor_path:
        classes.append("path-interceptor")

    if cell in snapshot.walls:
        classes.append("wall")
        label = ""
    if cell in snapshot.gate_cells:
        if cell in snapshot.closed_gates:
            classes.append("gate-closed")
            label = "X"
        else:
            classes.append("gate-open")
            label = ""
    if cell == snapshot.exit_cell:
        classes.append("exit")
        label = "EXIT"
    for agent in snapshot.agents:
        if cell == agent.cell:
            if agent.role == "Hunter":
                classes.append("hunter")
                label = "H"
            else:
                classes.append("interceptor")
                label = "I"
    if cell == snapshot.player:
        classes.append("player")
        label = "P"

    return " ".join(classes), label


def board_html(snapshot: GameSnapshot) -> str:
    cells = []
    for y in range(snapshot.rows):
        for x in range(snapshot.cols):
            class_name, label = _cell_classes(snapshot, (x, y))
            title = f"Cell ({x}, {y})"
            cells.append(
                f'<div class="{html.escape(class_name)}" title="{html.escape(title)}">'
                f'<span class="ase-cell-label">{html.escape(label)}</span></div>'
            )
    return (
        '<div class="ase-board-wrap">'
        '<div class="ase-board-title"><span>Tactical Maze Grid</span>'
        f'<span>{html.escape(snapshot.level_name)} | {snapshot.cols} x {snapshot.rows}</span></div>'
        '<div class="ase-board">'
        + "".join(cells)
        + "</div>"
        '<div class="ase-legend">'
        '<span class="ase-pill">P Player</span>'
        '<span class="ase-pill">H Hunter</span>'
        '<span class="ase-pill">I Interceptor</span>'
        '<span class="ase-pill">EXIT Goal</span>'
        '<span class="ase-pill">LOCK Dynamic gate</span>'
        '<span class="ase-pill">Glowing dots A* paths</span>'
        "</div></div>"
    )


@solara.component
def GameBoard(snapshot: GameSnapshot):
    solara.HTML(tag="div", unsafe_innerHTML=board_html(snapshot))
