"""Control panel — upgraded with Undo, Cloak, Heuristic selector, Level selector."""

from __future__ import annotations

from typing import Callable

import solara

from game.state import Difficulty, GameSnapshot, GameStatus, Heuristic
from .styles import button_css, kpad_button_css, wide_button_css


@solara.component_vue("keyboard_bridge.vue")
def KeyboardBridge(event_key: Callable[[str], None] | None = None):
    pass


@solara.component
def ControlPanel(
    snapshot: GameSnapshot,
    on_start,
    on_pause,
    on_resume,
    on_restart,
    on_scan,
    on_new_maze,
    on_move,
    on_difficulty,
    on_lab_mode,
    on_show_paths,
    on_undo,
    on_cloak,
    on_heuristic,
    on_level,
):
    KeyboardBridge(
        event_key=lambda key: on_move(
            {"up": (0, -1), "left": (-1, 0), "down": (0, 1), "right": (1, 0)}[key]
        )
    )

    is_playing = snapshot.status == GameStatus.PLAYING

    solara.HTML(
        tag="div",
        unsafe_innerHTML='<div class="ase-panel-title">🎮 Mission Control</div>',
    )

    with solara.Column(style={"gap": "10px"}):

        # ── Mission buttons ────────────────────────────────────────────────────
        with solara.Row(style={"display": "flex", "gap": "6px", "flexWrap": "wrap"}):
            solara.Button(
                "▶ START",
                on_click=on_start,
                color="success",
                style=button_css,
            )
            solara.Button(
                "⏸ PAUSE",
                on_click=on_pause,
                disabled=snapshot.status != GameStatus.PLAYING,
                style=button_css,
            )
            solara.Button(
                "▶▶ RESUME",
                on_click=on_resume,
                disabled=snapshot.status != GameStatus.PAUSED,
                style=button_css,
            )

        with solara.Row(style={"display": "flex", "gap": "6px", "flexWrap": "wrap"}):
            solara.Button(
                "↺ RESTART",
                on_click=on_restart,
                color="warning",
                style=button_css,
            )
            solara.Button(
                "🔍 SCAN",
                on_click=on_scan,
                disabled=not is_playing,
                color="primary",
                style=button_css,
            )
            solara.Button(
                "🗺 NEW MAZE",
                on_click=on_new_maze,
                color="secondary",
                style=button_css,
            )

        # ── Undo & Cloak ────────────────────────────────────────────────────────
        with solara.Row(style={"display": "flex", "gap": "6px", "flexWrap": "wrap"}):
            solara.Button(
                "↩ UNDO",
                on_click=on_undo,
                disabled=not is_playing or not snapshot.undo_available,
                style={**button_css, "color": "#ffcf48"},
            )
            cloak_label = (
                f"👻 CLOAK ({snapshot.cloak_moves_left})"
                if snapshot.cloak_active
                else "👻 ACTIVATE CLOAK"
            )
            solara.Button(
                cloak_label,
                on_click=on_cloak,
                disabled=(
                    not is_playing
                    or not snapshot.cloak_collected
                    or snapshot.cloak_active
                ),
                style={**button_css, "background": "rgba(160,96,255,0.2)", "color": "#c89fff"},
            )

        # ── Selectors ──────────────────────────────────────────────────────────
        solara.Select(
            "Difficulty",
            values=[d.value for d in Difficulty],
            value=snapshot.difficulty.value,
            on_value=lambda v: on_difficulty(Difficulty(v)),
            style={"width": "100%"},
        )

        solara.Select(
            "Level",
            values=["1 – Shadow District", "2 – Neon Labyrinth", "3 – Blacksite"],
            value=f"{snapshot.level_index + 1} – {snapshot.level_name}",
            on_value=lambda v: on_level(int(v[0]) - 1),
            style={"width": "100%"},
        )

        solara.Select(
            "A* Heuristic",
            values=[h.value for h in Heuristic],
            value=snapshot.heuristic.value,
            on_value=lambda v: on_heuristic(Heuristic(v)),
            style={"width": "100%"},
        )

        solara.Switch(
            label="🔬 LAB EVALUATION MODE",
            value=snapshot.lab_mode,
            on_value=on_lab_mode,
            color="cyan",
        )
        solara.Switch(
            label="👁 Show A* Paths",
            value=snapshot.show_paths,
            on_value=on_show_paths,
            color="cyan",
        )

        # ── D-Pad ──────────────────────────────────────────────────────────────
        solara.HTML(
            tag="div",
            unsafe_innerHTML=(
                '<div class="ase-panel-title" style="margin-top:8px;">🕹 Movement</div>'
            ),
        )
        with solara.Column(style={"alignItems": "center", "gap": "4px"}):
            solara.Button(
                "▲",
                on_click=lambda: on_move((0, -1)),
                disabled=not is_playing,
                style=kpad_button_css,
            )
            with solara.Row(style={"display": "flex", "gap": "4px"}):
                solara.Button(
                    "◀",
                    on_click=lambda: on_move((-1, 0)),
                    disabled=not is_playing,
                    style=kpad_button_css,
                )
                solara.Button(
                    "▼",
                    on_click=lambda: on_move((0, 1)),
                    disabled=not is_playing,
                    style=kpad_button_css,
                )
                solara.Button(
                    "▶",
                    on_click=lambda: on_move((1, 0)),
                    disabled=not is_playing,
                    style=kpad_button_css,
                )

        solara.HTML(
            tag="div",
            unsafe_innerHTML=(
                '<div class="ase-muted" style="font-size:11px; text-align:center; margin-top:4px;">'
                "W/A/S/D or arrow keys also work"
                "</div>"
            ),
        )
