"""Explanatory and lab evaluation panels."""

from __future__ import annotations

import html

import solara

from game.state import GameSnapshot


def _row(label: str, value: str | int) -> str:
    return f'<div class="ase-row"><span class="ase-muted">{html.escape(label)}</span><b>{html.escape(str(value))}</b></div>'


@solara.component
def LabPanel(snapshot: GameSnapshot):
    if not snapshot.lab_mode:
        return
    hunter = snapshot.agents[0]
    interceptor = snapshot.agents[1]
    html_text = (
        '<div class="ase-panel" style="margin-top:12px;">'
        '<div class="ase-panel-title">LAB EVALUATION MODE</div>'
        '<div class="ase-code">f(n) = g(n) + h(n)<br>'
        'g(n) = cost from start node<br>'
        'h(n) = estimated cost to goal<br>'
        'Manhattan: h(n) = |x1-x2| + |y1-y2|</div>'
        '<div style="display:grid; grid-template-columns: repeat(2, minmax(220px, 1fr)); gap:12px; margin-top:12px;">'
        '<div class="ase-readout">'
        '<div class="ase-panel-title">Hunter Search</div>'
        + _row("Open Set Count", hunter.open_set_count)
        + _row("Closed Set Count", hunter.closed_set_count)
        + _row("Current Node", hunter.current_node)
        + _row("Path Length", hunter.path_length)
        + _row("Nodes Explored", hunter.nodes_explored)
        + _row("Replanning Count", hunter.recalculations)
        + "</div>"
        '<div class="ase-readout">'
        '<div class="ase-panel-title">Interceptor Search</div>'
        + _row("Open Set Count", interceptor.open_set_count)
        + _row("Closed Set Count", interceptor.closed_set_count)
        + _row("Current Node", interceptor.current_node)
        + _row("Path Length", interceptor.path_length)
        + _row("Nodes Explored", interceptor.nodes_explored)
        + _row("Replanning Count", interceptor.recalculations)
        + "</div></div></div>"
    )
    solara.HTML(tag="div", unsafe_innerHTML=html_text)


@solara.component
def ScanPanel(snapshot: GameSnapshot):
    if not snapshot.scan.active:
        solara.HTML(
            tag="div",
            unsafe_innerHTML=(
                '<div class="ase-panel" style="margin-top:12px;">'
                '<div class="ase-panel-title">SHADOW SCAN</div>'
                '<div class="ase-muted">Press SCAN to inspect live enemy distance, threat and path length.</div>'
                "</div>"
            ),
        )
        return
    rows = []
    for role, info in snapshot.scan.agents.items():
        rows.append(
            '<div class="ase-panel" style="margin-top:8px;">'
            f'<div class="ase-panel-title">{html.escape(role)}</div>'
            '<div class="ase-readout">'
            + _row("Distance", f"{info['distance']} cells")
            + _row("Threat", info["threat"])
            + _row("Path Length", info["path_length"])
            + _row("Target", info["target"])
            + "</div></div>"
        )
    solara.HTML(
        tag="div",
        unsafe_innerHTML=(
            '<div class="ase-panel" style="margin-top:12px; border-color:rgba(49,216,255,.55);">'
            '<div class="ase-panel-title">SHADOW SCAN</div>'
            + "".join(rows)
            + "</div>"
        ),
    )


@solara.component
def ExplanationPanel():
    solara.Markdown(
        """
<details class="ase-panel" style="margin-top:12px;">
<summary class="ase-panel-title">HOW THE AI WORKS</summary>

1. The maze is represented as a grid.
2. The player occupies one grid cell.
3. AI agents detect the player's position.
4. A* searches for an efficient path.
5. Manhattan distance estimates the remaining cost.
6. AI agents move along the calculated path.
7. When the player moves or gates change, paths are recalculated.
8. The player must reach the exit before being intercepted.

</details>
""",
        unsafe_solara_execute=False,
    )


@solara.component
def CreditsPanel():
    solara.HTML(
        tag="div",
        unsafe_innerHTML=(
            '<div class="ase-panel ase-credit">'
            '<div class="ase-panel-title" style="color:#2ee889;">PROJECT CREDITS</div>'
            '<div class="ase-readout">'
            + _row("Name", "Dhanush Naidu")
            + _row("Registration Number", "BL.S.U4AIE25241")
            + _row("Course", "Fundamentals of AIE")
            + _row("Project", "AI Shadow Escape")
            + "</div></div>"
        ),
    )


@solara.component
def EndPanel(snapshot: GameSnapshot, play_again):
    if snapshot.status.value not in {"MISSION COMPLETE", "MISSION FAILED"}:
        return
    won = snapshot.status.value == "MISSION COMPLETE"
    title = "MISSION COMPLETE" if won else "MISSION FAILED"
    subtitle = "You escaped the AI shadows." if won else "The shadows intercepted you."
    css_class = "ase-good" if won else "ase-danger"
    html_text = (
        '<div class="ase-panel" style="margin-top:12px;">'
        f'<div class="ase-stat-value {css_class}">{title}</div>'
        f'<div class="ase-muted" style="margin-bottom:12px;">{subtitle}</div>'
        '<div class="ase-readout">'
        + _row("Final Score", snapshot.score)
        + _row("Moves", snapshot.moves)
        + _row("A* Recalculations", snapshot.route_recalculations)
        + _row("Survival Time", f"{snapshot.elapsed_seconds:.1f}s")
        + "</div></div>"
    )
    solara.HTML(tag="div", unsafe_innerHTML=html_text)
    solara.Button("PLAY AGAIN", on_click=play_again, color="success", style={"width": "100%", "marginTop": "8px"})
