"""Game board renderer — emoji icons, heatmap overlay, cloak shimmer, path dots."""

from __future__ import annotations

import html

import solara

from game.state import GameSnapshot

# Role → emoji label
ROLE_EMOJI = {
    "Hunter":      "👁",
    "Interceptor": "⚡",
    "Flanker":     "🔮",
}
ROLE_CLASS = {
    "Hunter":      "hunter",
    "Interceptor": "interceptor",
    "Flanker":     "flanker",
}
ROLE_FROZEN_CLASS = {
    "Hunter":      "hunter-frozen",
    "Interceptor": "interceptor-frozen",
    "Flanker":     "flanker-frozen",
}


def _cell_html(snapshot: GameSnapshot, x: int, y: int) -> str:
    cell = (x, y)
    classes = ["ase-cell", "floor-a" if (x + y) % 2 == 0 else "floor-b"]
    label = ""
    style = ""

    # Path overlays (only on floor cells — applied before entity override)
    if snapshot.show_paths:
        for i, agent in enumerate(snapshot.agents):
            agent_path = set(agent.path[1:])
            if cell in agent_path:
                path_cls = f"path-{agent.role.lower()}"
                classes.append(path_cls)

    # Walls
    if cell in snapshot.walls:
        # Remove floor class, add wall
        classes = [c for c in classes if not c.startswith("floor")]
        classes.append("wall")
        label = ""

    # Gates (override wall if also a gate)
    if cell in snapshot.gate_cells:
        classes = [c for c in classes if c not in ("wall", "floor-a", "floor-b")]
        if cell in snapshot.closed_gates:
            classes.append("gate-closed")
            label = "🔒"
        else:
            classes.append("gate-open")
            label = "🚪"

    # Power-up
    if snapshot.power_up_cell and cell == snapshot.power_up_cell:
        classes = [c for c in classes if not c.startswith("floor")]
        classes.append("power-up")
        label = "✨"

    # Exit
    if cell == snapshot.exit_cell:
        classes = [c for c in classes if c not in ("wall", "floor-a", "floor-b")]
        classes.append("exit")
        label = "🏁"

    # AI Agents
    for agent in snapshot.agents:
        if cell == agent.cell:
            frozen_css = ROLE_FROZEN_CLASS.get(agent.role, agent.role.lower() + "-frozen")
            active_css = ROLE_CLASS.get(agent.role, agent.role.lower())
            css = frozen_css if agent.frozen else active_css
            classes = [c for c in classes if c not in ("wall", "floor-a", "floor-b")]
            classes.append(css)
            label = ROLE_EMOJI.get(agent.role, "?")

    # Player (always on top)
    if cell == snapshot.player:
        classes = [c for c in classes if c not in ("wall", "floor-a", "floor-b")]
        classes.append("player-cloaked" if snapshot.cloak_active else "player")
        label = "🔵" if not snapshot.cloak_active else "👻"

    cls_str = html.escape(" ".join(classes))
    title = html.escape(f"({x},{y})")
    lbl = html.escape(label)
    return (
        f'<div class="{cls_str}" title="{title}" style="{style}">'
        f'<span class="ase-cell-label">{lbl}</span></div>'
    )


def board_html(snapshot: GameSnapshot) -> str:
    grid_cols = snapshot.cols
    cells = []
    for y in range(snapshot.rows):
        for x in range(snapshot.cols):
            cells.append(_cell_html(snapshot, x, y))

    legend_items = [
        ("🔵", "Player"),
        ("👻", "Cloaked"),
        ("👁", "Hunter"),
        ("⚡", "Interceptor"),
        ("🔮", "Flanker"),
        ("🏁", "Exit"),
        ("🔒", "Gate (closed)"),
        ("🚪", "Gate (open)"),
        ("✨", "Cloak token"),
    ]
    legend_html = "".join(
        f'<span class="ase-pill">{html.escape(em)} {html.escape(nm)}</span>'
        for em, nm in legend_items
    )

    level_tag = html.escape(f"{snapshot.level_name} | {snapshot.cols}×{snapshot.rows}")

    return (
        '<div class="ase-board-wrap">'
        '<div class="ase-board-title">'
        '<span>🗺 Tactical Grid</span>'
        f'<span>{level_tag}</span>'
        '</div>'
        f'<div class="ase-board" style="grid-template-columns: repeat({grid_cols}, minmax(18px,1fr));">'
        + "".join(cells)
        + "</div>"
        f'<div class="ase-legend">{legend_html}</div>'
        "</div>"
    )


@solara.component
def GameBoard(snapshot: GameSnapshot):
    solara.HTML(tag="div", unsafe_innerHTML=board_html(snapshot))
