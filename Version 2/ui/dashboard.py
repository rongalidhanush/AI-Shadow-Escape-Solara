"""Top dashboard — animated stat cards, danger ring, lives counter, cloak badge, theme toggle."""

from __future__ import annotations

import html
from typing import Callable, Optional

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
        ring_color = "var(--accent-red)"
        label_class = "ase-danger"
    elif danger_label == "HIGH":
        ring_color = "#ff8020"
        label_class = "ase-warn"
    elif danger_label == "MEDIUM":
        ring_color = "var(--accent-warn)"
        label_class = "ase-warn"
    else:
        ring_color = "var(--accent-green)"
        label_class = "ase-good"

    return (
        '<div class="danger-ring-wrap">'
        '<div class="danger-ring">'
        '<svg viewBox="0 0 80 80">'
        f'<circle cx="40" cy="40" r="{radius}" fill="none" stroke="rgba(128,128,128,0.18)" stroke-width="7"/>'
        f'<circle cx="40" cy="40" r="{radius}" fill="none" stroke="{ring_color}" stroke-width="7" '
        f'stroke-dasharray="{fill:.1f} {gap:.1f}" stroke-linecap="round" '
        f'style="filter:drop-shadow(0 0 4px {ring_color})"/>'
        "</svg>"
        f'<span class="danger-ring-value {label_class}">{danger_value}</span>'
        "</div>"
        f'<div class="danger-ring-label {label_class}">{html.escape(danger_label)} THREAT</div>'
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
def Header(
    snapshot: GameSnapshot,
    theme: str = "dark",
    on_toggle_theme: Optional[Callable[[], None]] = None,
):
    status_color = {
        "MISSION COMPLETE": "var(--accent-green)",
        "MISSION FAILED":   "var(--accent-red)",
        "PLAYING":          "var(--accent-cyan)",
        "PAUSED":           "var(--accent-warn)",
        "READY":            "var(--text-muted)",
    }.get(snapshot.status.value, "var(--text-muted)")

    with solara.Div(classes=["ase-shell"]):
        with solara.Row(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "flexWrap": "wrap",
                "gap": "16px",
                "marginBottom": "16px",
            }
        ):
            # Left: Title and subtitle
            with solara.Column(style={"gap": "2px"}):
                solara.HTML(
                    tag="div",
                    unsafe_innerHTML=(
                        '<div>'
                        '<h1 class="ase-title">⚡ AI SHADOW ESCAPE</h1>'
                        '<div class="ase-subtitle">Autonomous Multi-Agent Pursuit · A* Pathfinding · Dynamic Replanning</div>'
                        '</div>'
                    ),
                )

            # Right: Theme button, status, cloak, lives
            with solara.Row(style={"alignItems": "center", "gap": "10px", "flexWrap": "wrap"}):
                if on_toggle_theme:
                    solara.Button(
                        "☀️ Bright Mode" if theme == "dark" else "🌙 Dark Mode",
                        on_click=on_toggle_theme,
                        classes=["ase-theme-btn"],
                    )
                solara.HTML(
                    tag="div",
                    unsafe_innerHTML=(
                        '<div style="display:flex; flex-direction:column; align-items:flex-end; gap:6px;">'
                        f'<span class="ase-pill" style="border-color:{status_color}; color:{status_color};">'
                        f'● {html.escape(snapshot.status.value)}</span>'
                        + _cloak_badge(snapshot)
                        + _lives_html(snapshot.lives)
                        + '</div>'
                    ),
                )

        # Stat cards grid & danger ring
        solara.HTML(
            tag="div",
            unsafe_innerHTML=(
                '<div class="ase-stat-grid">'
                + _card("Score", str(snapshot.score), "ase-good")
                + _card("Moves", str(snapshot.moves))
                + _card("Level", f"{snapshot.level_index + 1} / 3")
                + _card("A* Replans", str(snapshot.route_recalculations), "ase-warn")
                + _card("Heuristic", snapshot.heuristic.value)
                + _card("Difficulty", snapshot.difficulty.value)
                + '</div>'
                + _danger_ring(snapshot.danger_value, snapshot.danger_label)
            ),
        )


@solara.component
def MissionMessage(snapshot: GameSnapshot):
    msg = snapshot.message or ""
    if not msg:
        return

    # In PLAYING status, only show meaningful tactical alerts (e.g. Cloak, Blocked, Captured, Undo)
    # Routine status is already cleanly indicated by the header status badge and KPI telemetry.
    if snapshot.status.value == "PLAYING":
        is_alert = any(
            trigger in msg
            for trigger in (
                "Blocked",
                "CLOAK",
                "Cloak",
                "Captured",
                "penal",
                "Penalty",
                "Warning",
                "Scan complete",
            )
        )
        if not is_alert:
            return

    color = {
        "MISSION COMPLETE": "var(--accent-green)",
        "MISSION FAILED":   "var(--accent-red)",
        "PAUSED":           "var(--accent-warn)",
    }.get(snapshot.status.value, "var(--accent-cyan)")

    icon = {
        "MISSION COMPLETE": "🏆",
        "MISSION FAILED":   "💀",
        "PAUSED":           "⏸",
    }.get(snapshot.status.value, "⚡")

    solara.HTML(
        tag="div",
        unsafe_innerHTML=(
            f'<div class="ase-mission-banner" style="border-color:{color}; '
            f'background:var(--bg-panel); color:{color};">'
            f'<span style="font-size:18px;">{icon}</span>'
            f'<span style="color:var(--text-primary);">{html.escape(msg)}</span>'
            "</div>"
        ),
    )
