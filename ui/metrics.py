"""Metrics and AI status panels."""

from __future__ import annotations

import html

import solara

from game.state import GameSnapshot


def _row(label: str, value: str | int) -> str:
    return f'<div class="ase-row"><span class="ase-muted">{html.escape(label)}</span><b>{html.escape(str(value))}</b></div>'


@solara.component
def LiveMetrics(snapshot: GameSnapshot):
    hunter = snapshot.agents[0]
    interceptor = snapshot.agents[1]
    html_text = (
        '<div class="ase-panel">'
        '<div class="ase-panel-title">LIVE METRICS</div>'
        '<div class="ase-readout">'
        + _row("Hunter Distance", hunter.distance_to_player)
        + _row("Interceptor Distance", interceptor.distance_to_player)
        + _row("Hunter Path Length", hunter.path_length)
        + _row("Interceptor Path Length", interceptor.path_length)
        + _row("A* Recalculations", snapshot.route_recalculations)
        + _row("Player Moves", snapshot.moves)
        + _row("Gates Active", len(snapshot.closed_gates))
        + _row("Current Score", snapshot.score)
        + _row("Survival Time", f"{snapshot.elapsed_seconds:.1f}s")
        + _row("Danger Level", f"{snapshot.danger_label} ({snapshot.danger_value}%)")
        + "</div></div>"
    )
    solara.HTML(tag="div", unsafe_innerHTML=html_text)


@solara.component
def AiStatus(snapshot: GameSnapshot):
    html_text = (
        '<div class="ase-panel">'
        '<div class="ase-panel-title">AI SYSTEM STATUS</div>'
        '<div class="ase-readout">'
        + _row("Algorithm", "A* Search")
        + _row("Agents", len(snapshot.agents))
        + _row("Heuristic", "Manhattan Distance")
        + _row("Pathfinding", "Dynamic Replanning")
        + _row("Environment", "Grid Maze")
        + _row("Obstacles", "Dynamic Gates + Walls")
        + _row("Difficulty", snapshot.difficulty.value)
        + "</div></div>"
    )
    solara.HTML(tag="div", unsafe_innerHTML=html_text)
