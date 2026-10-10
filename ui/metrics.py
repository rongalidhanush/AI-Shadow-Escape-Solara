"""Live metrics and AI status panels — supports 3 agents."""

from __future__ import annotations

import html

import solara

from game.state import GameSnapshot


def _row(label: str, value: str | int, css_class: str = "") -> str:
    val_html = html.escape(str(value))
    if css_class:
        val_html = f'<b class="{css_class}">{val_html}</b>'
    else:
        val_html = f"<b>{val_html}</b>"
    return (
        f'<div class="ase-row">'
        f'<span class="ase-muted">{html.escape(label)}</span>'
        f"{val_html}</div>"
    )


def _agent_block(agent) -> str:
    emoji = {"Hunter": "👁", "Interceptor": "⚡", "Flanker": "🔮"}.get(agent.role, "?")
    color = {
        "Hunter": "#ff4060",
        "Interceptor": "#ff9020",
        "Flanker": "#c08fff",
    }.get(agent.role, "#31d8ff")
    frozen_tag = (
        ' <span style="color:#7ab8dc;font-size:10px;">[FROZEN]</span>'
        if agent.frozen else ""
    )
    return (
        f'<div style="font-size:11px; font-weight:700; color:{color}; margin-bottom:6px;">'
        f'{emoji} {html.escape(agent.role)}{frozen_tag}</div>'
        + _row("Distance", f"{agent.distance_to_player} cells")
        + _row("Path Length", agent.path_length)
        + _row("Recalculations", agent.recalculations)
    )


@solara.component
def LiveMetrics(snapshot: GameSnapshot):
    agents_html = ""
    for agent in snapshot.agents:
        agents_html += (
            f'<div style="background:rgba(0,0,0,0.2); border:1px solid rgba(255,255,255,0.07); '
            f'border-radius:10px; padding:10px; margin-top:8px;">'
            + _agent_block(agent)
            + "</div>"
        )

    html_text = (
        '<div class="ase-panel">'
        '<div class="ase-panel-title">📊 Live Metrics</div>'
        '<div class="ase-readout">'
        + _row("Player Moves", snapshot.moves)
        + _row("Survival Time", f"{snapshot.elapsed_seconds:.1f}s")
        + _row("Current Score", snapshot.score, "ase-good")
        + _row("Gates Active", len(snapshot.closed_gates))
        + _row("Scans Used", snapshot.scans_used)
        + _row("Collisions", snapshot.obstacle_collisions)
        + _row("Lives", f"{'❤️' * snapshot.lives}{'🖤' * (3 - snapshot.lives)}")
        + _row("Danger", f"{snapshot.danger_label} ({snapshot.danger_value}%)",
               "ase-danger" if snapshot.danger_label in {"CRITICAL","HIGH"} else "ase-warn")
        + "</div>"
        + agents_html
        + "</div>"
    )
    solara.HTML(tag="div", unsafe_innerHTML=html_text)


@solara.component
def AiStatus(snapshot: GameSnapshot):
    html_text = (
        '<div class="ase-panel">'
        '<div class="ase-panel-title">🤖 AI System</div>'
        '<div class="ase-readout">'
        + _row("Algorithm", "A* Search")
        + _row("Agents", len(snapshot.agents))
        + _row("Primary Heuristic", snapshot.heuristic.value)
        + _row("Comparison", "BFS (Lab Mode)")
        + _row("Pathfinding", "Dynamic Replanning")
        + _row("Environment", "Grid Maze")
        + _row("Obstacles", "Dynamic Gates + Walls")
        + _row("Difficulty", snapshot.difficulty.value)
        + _row("Level", f"{snapshot.level_index + 1} — {snapshot.level_name}")
        + _row("A* Replans", snapshot.route_recalculations, "ase-warn")
        + "</div></div>"
    )
    solara.HTML(tag="div", unsafe_innerHTML=html_text)
