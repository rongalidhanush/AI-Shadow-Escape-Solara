"""Control panel components."""

from __future__ import annotations

from typing import Callable

import solara

from game.state import Difficulty, GameSnapshot, GameStatus
from .styles import button_css, wide_button_css


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
):
    KeyboardBridge(event_key=lambda key: on_move({
        "up": (0, -1),
        "left": (-1, 0),
        "down": (0, 1),
        "right": (1, 0),
    }[key]))
    solara.HTML(tag="div", unsafe_innerHTML='<div class="ase-panel-title">CONTROL PANEL</div>')
    with solara.Column(style={"gap": "10px"}):
        with solara.Row(style={"display": "flex", "gap": "8px", "flexWrap": "wrap"}):
            solara.Button("START GAME", on_click=on_start, color="success", style=button_css)
            solara.Button("PAUSE", on_click=on_pause, disabled=snapshot.status != GameStatus.PLAYING, style=button_css)
            solara.Button("RESUME", on_click=on_resume, disabled=snapshot.status != GameStatus.PAUSED, style=button_css)
        with solara.Row(style={"display": "flex", "gap": "8px", "flexWrap": "wrap"}):
            solara.Button("RESTART", on_click=on_restart, color="warning", style=button_css)
            solara.Button("SCAN", on_click=on_scan, disabled=snapshot.status != GameStatus.PLAYING, color="primary", style=button_css)
            solara.Button("NEW MAZE", on_click=on_new_maze, color="secondary", style=button_css)

        solara.Select(
            "Difficulty",
            values=[difficulty.value for difficulty in Difficulty],
            value=snapshot.difficulty.value,
            on_value=lambda value: on_difficulty(Difficulty(value)),
            style={"width": "100%"},
        )
        solara.Switch(label="LAB EVALUATION MODE", value=snapshot.lab_mode, on_value=on_lab_mode, color="cyan")
        solara.Switch(label="Show A* Paths", value=snapshot.show_paths, on_value=on_show_paths, color="cyan")

        solara.HTML(tag="div", unsafe_innerHTML='<div class="ase-panel-title" style="margin-top:8px;">MOVEMENT</div>')
        with solara.Column(style={"alignItems": "center", "gap": "8px"}):
            solara.Button("UP / W", on_click=lambda: on_move((0, -1)), disabled=snapshot.status != GameStatus.PLAYING, style=wide_button_css)
            with solara.Row(style={"display": "flex", "gap": "8px"}):
                solara.Button("LEFT / A", on_click=lambda: on_move((-1, 0)), disabled=snapshot.status != GameStatus.PLAYING, style=button_css)
                solara.Button("DOWN / S", on_click=lambda: on_move((0, 1)), disabled=snapshot.status != GameStatus.PLAYING, style=button_css)
                solara.Button("RIGHT / D", on_click=lambda: on_move((1, 0)), disabled=snapshot.status != GameStatus.PLAYING, style=button_css)
        solara.HTML(
            tag="div",
            unsafe_innerHTML=(
                '<div class="ase-muted" style="font-size:12px; margin-top:6px;">'
                "W/A/S/D and arrow keys trigger these same movement controls when the page has focus."
                "</div>"
            ),
        )
