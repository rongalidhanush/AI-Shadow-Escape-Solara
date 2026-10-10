"""Solara web application for AI Shadow Escape."""

from __future__ import annotations

import solara

from game import Difficulty, GameEngine
from ui.board import GameBoard
from ui.controls import ControlPanel
from ui.dashboard import Header, MissionMessage
from ui.metrics import AiStatus, LiveMetrics
from ui.panels import CreditsPanel, EndPanel, ExplanationPanel, LabPanel, ScanPanel
from ui.styles import PAGE_CSS


@solara.component
def Page():
    engine_ref = solara.use_ref(None)
    revision = solara.use_reactive(0)

    if engine_ref.current is None:
        engine_ref.current = GameEngine(Difficulty.NORMAL)

    engine: GameEngine = engine_ref.current
    _revision_marker = revision.value
    snapshot = engine.snapshot()

    def refresh() -> None:
        revision.value = revision.value + 1

    def start() -> None:
        engine.start()
        refresh()

    def pause() -> None:
        engine.pause()
        refresh()

    def resume() -> None:
        engine.resume()
        refresh()

    def restart() -> None:
        engine.restart()
        refresh()

    def scan() -> None:
        engine.scan()
        refresh()

    def new_maze() -> None:
        engine.new_maze()
        refresh()

    def move(direction: tuple[int, int]) -> None:
        engine.move_player(direction)
        refresh()

    def set_difficulty(difficulty: Difficulty) -> None:
        engine.set_difficulty(difficulty)
        engine.start()
        refresh()

    def set_lab_mode(enabled: bool) -> None:
        engine.toggle_lab_mode(enabled)
        refresh()

    def set_show_paths(enabled: bool) -> None:
        engine.toggle_paths(enabled)
        refresh()

    solara.HTML(tag="div", unsafe_innerHTML=PAGE_CSS)
    with solara.Div(classes=["ase-root"]):
        Header(snapshot)
        with solara.Div(classes=["ase-shell"]):
            MissionMessage(snapshot)
            with solara.Div(classes=["ase-grid-layout"]):
                with solara.Div(classes=["ase-panel"]):
                    ControlPanel(
                        snapshot,
                        on_start=start,
                        on_pause=pause,
                        on_resume=resume,
                        on_restart=restart,
                        on_scan=scan,
                        on_new_maze=new_maze,
                        on_move=move,
                        on_difficulty=set_difficulty,
                        on_lab_mode=set_lab_mode,
                        on_show_paths=set_show_paths,
                    )
                    ScanPanel(snapshot)
                with solara.Div():
                    GameBoard(snapshot)
                    EndPanel(snapshot, play_again=restart)
                    LabPanel(snapshot)
                    ExplanationPanel()
                with solara.Div(style={"display": "grid", "gap": "12px"}):
                    CreditsPanel()
                    AiStatus(snapshot)
                    LiveMetrics(snapshot)

