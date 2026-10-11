"""Top dashboard — animated stat cards, danger ring, lives counter, cloak badge."""

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


def _danger_ring(danger_value: int, danger_label: str) -> str:
    """Render an SVG ring that fills red as danger increases."""
    radius = 32
    circ = 2 * 3.14159 * radius
    fill = circ * (danger_value / 100)
    gap = circ - fill

    if danger_label == "CRITICAL":
        ring_color = "#ff2040"
        label_class = "ase-danger"
    elif danger_label == "HIGH":
        ring_color = "#ff8020"
        label_class = "ase-warn"
    elif danger_label == "MEDIUM":
        ring_color = "#ffcf48"
        label_class = "ase-warn"
    else:
        ring_color = "#2ee889"
        label_class = "ase-good"

    return (
        '<div class="danger-ring-wrap">'
        '<div class="danger-ring">'
        '<svg viewBox="0 0 80 80">'
        f'<circle cx="40" cy="40" r="{radius}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="7"/>'
        f'<circle cx="40" cy="40" r="{radius}" fill="none" stroke="{ring_color}" stroke-width="7" '
        f'stroke-dasharray="{fill:.1f} {gap:.1f}" stroke-linecap="round" '
        f'style="filter:drop-shadow(0 0 4px {ring_color})"/>'
        "</svg>"
        f'<span class="danger-ring-value {label_class}">{danger_value}</span>'
        "</div>"
        f'<div class="danger-ring-label {label_class}">{html.escape(danger_label)}</div>'
        "</div>"
    )


def _lives_html(lives: int, max_lives: int = 3) -> str:
    hearts = "❤️" * lives + '<span style="opacity:0.25">❤️</span>' * (max_lives - lives)
    return f'<div class="ase-lives">{hearts}</div>'


def _cloak_badge(snapshot: GameSnapshot) -> str:
    if snapshot.cloak_active:
        return (
            f'<div class="cloak-badge cloak-active-badge">👻 CLOAK ACTIVE — '
            f'{snapshot.cloak_moves_left} moves left</div>'
        )
    if snapshot.cloak_collected:
        return '<div class="cloak-badge cloak-ready-badge">✨ CLOAK READY</div>'
    if snapshot.power_up_cell:
        return '<div class="cloak-badge cloak-none-badge">🔍 Find the ✨ Cloak token</div>'
    return '<div class="cloak-badge cloak-none-badge">No cloak available</div>'


@solara.component
def Header(snapshot: GameSnapshot):
    danger_class = (
        "ase-danger" if snapshot.danger_label in {"HIGH", "CRITICAL"}
        else "ase-warn"
    )
    status_color = {
        "MISSION COMPLETE": "#2ee889",
        "MISSION FAILED":   "#ff4060",
        "PLAYING":          "#31d8ff",
        "PAUSED":           "#ffcf48",
        "READY":            "#6a8fa8",
    }.get(snapshot.status.value, "#6a8fa8")

    html_text = (
        '<div class="ase-shell">'
        '<div style="display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap; align-items:flex-end; margin-bottom:14px;">'
        "<div>"
        '<h1 class="ase-title">⚡ AI SHADOW ESCAPE</h1>'
        '<div class="ase-subtitle">Autonomous Multi-Agent Pursuit · A* Pathfinding · 3 AI Agents</div>'
        "</div>"
        '<div style="display:flex; flex-direction:column; align-items:flex-end; gap:6px;">'
        f'<span class="ase-pill" style="border-color:{status_color}; color:{status_color};">'
        f'● {html.escape(snapshot.status.value)}</span>'
        + _cloak_badge(snapshot)
        + _lives_html(snapshot.lives)
        + "</div></div>"
        '<div class="ase-stat-grid">'
        + _card("Score", str(snapshot.score), "ase-good")
        + _card("Moves", str(snapshot.moves))
        + _card("Level", f"{snapshot.level_index + 1} / 3")
        + _card("A* Replans", str(snapshot.route_recalculations), "ase-warn")
        + _card("Heuristic", snapshot.heuristic.value)
        + _card("Difficulty", snapshot.difficulty.value)
        + "</div>"
        + _danger_ring(snapshot.danger_value, snapshot.danger_label)
        + "</div>"
    )
    solara.HTML(tag="div", unsafe_innerHTML=html_text)


@solara.component
def MissionMessage(snapshot: GameSnapshot):
    color = {
        "MISSION COMPLETE": "#2ee889",
        "MISSION FAILED":   "#ff4060",
        "PAUSED":           "#ffcf48",
    }.get(snapshot.status.value, "#31d8ff")

    icon = {
        "MISSION COMPLETE": "🏆",
        "MISSION FAILED":   "💀",
        "PAUSED":           "⏸",
        "PLAYING":          "▶",
    }.get(snapshot.status.value, "ℹ")

    solara.HTML(
        tag="div",
        unsafe_innerHTML=(
            f'<div class="ase-mission-banner" style="border-color:{color}; '
            f'background:rgba(0,0,0,0.3); color:{color};">'
            f'<span style="font-size:16px;">{icon}</span>'
            f'<span>{html.escape(snapshot.message)}</span>'
            "</div>"
        ),
    )
