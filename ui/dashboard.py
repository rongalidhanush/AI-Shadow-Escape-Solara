"""Top dashboard and status cards."""

from __future__ import annotations

import html

import solara

from game.state import GameSnapshot


def _card(label: str, value: str, css_class: str = "") -> str:
    return (
        '<div class="ase-stat">'
        f'<div class="ase-stat-label">{html.escape(label)}</div>'
        f'<div class="ase-stat-value {css_class}">{html.escape(value)}</div>'
        "</div>"
    )


@solara.component
def Header(snapshot: GameSnapshot):
    danger_class = "ase-danger" if snapshot.danger_label in {"HIGH", "CRITICAL"} else "ase-warn"
    html_text = (
        '<div class="ase-shell">'
        '<div style="display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap; align-items:flex-end;">'
        "<div>"
        '<h1 class="ase-title">AI SHADOW ESCAPE</h1>'
        '<div class="ase-subtitle">Autonomous Multi-Agent Pursuit using A* Pathfinding</div>'
        "</div>"
        f'<div class="ase-pill">Status: <b>{html.escape(snapshot.status.value)}</b></div>'
        "</div>"
        '<div class="ase-stat-grid">'
        + _card("Game Status", snapshot.status.value)
        + _card("Score", str(snapshot.score), "ase-good")
        + _card("Moves", str(snapshot.moves))
        + _card("A* Replans", str(snapshot.route_recalculations), "ase-warn")
        + _card("Danger Level", snapshot.danger_label, danger_class)
        + "</div></div>"
    )
    solara.HTML(tag="div", unsafe_innerHTML=html_text)


@solara.component
def MissionMessage(snapshot: GameSnapshot):
    color = "#ff4d5f" if snapshot.status.value == "MISSION FAILED" else "#31d8ff"
    solara.HTML(
        tag="div",
        unsafe_innerHTML=(
            f'<div class="ase-panel" style="border-color:{color}; margin-bottom:12px;">'
            f'<div style="color:{color}; font-weight:750;">{html.escape(snapshot.message)}</div>'
            "</div>"
        ),
    )
