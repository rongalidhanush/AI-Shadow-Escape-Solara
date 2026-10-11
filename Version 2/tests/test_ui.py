"""Tests for UI components, themes, and game over / restart mechanics."""

import solara
from game.engine import GameEngine
from game.state import GameStatus
from ui.panels import EndPanel, ExplanationPanel
from ui.styles import PAGE_CSS


def test_page_css_contains_themes_and_ai_contrast_rules():
    assert "data-theme=\"dark\"" in PAGE_CSS or ".ase-theme-dark" in PAGE_CSS
    assert "data-theme=\"light\"" in PAGE_CSS or ".ase-theme-light" in PAGE_CSS
    assert "--ai-box-bg" in PAGE_CSS
    assert "--ai-box-text" in PAGE_CSS
    assert "--ai-title-text" in PAGE_CSS
    assert ".ase-ai-dossier" in PAGE_CSS
    assert ".ase-overlay" in PAGE_CSS
    assert ".ase-theme-btn" in PAGE_CSS


def test_end_panel_inactive_during_play():
    engine = GameEngine()
    engine.start()
    snapshot = engine.snapshot()
    assert snapshot.status == GameStatus.PLAYING
    # When playing, the underlying EndPanel function returns None
    result = EndPanel.f(snapshot, on_restart=lambda: None)
    assert result is None


def test_end_panel_element_creation_on_game_over():
    engine = GameEngine()
    engine.status = GameStatus.LOST
    snapshot = engine.snapshot()
    assert snapshot.status == GameStatus.LOST

    # In Solara, calling the component creates an Element with the correct props
    element = EndPanel(snapshot, on_restart=lambda: None)
    assert element is not None
    assert element.component == EndPanel


def test_end_panel_element_creation_on_win():
    engine = GameEngine()
    engine.status = GameStatus.WON
    snapshot = engine.snapshot()
    assert snapshot.status == GameStatus.WON

    element = EndPanel(snapshot, on_restart=lambda: None, on_next_level=lambda idx: None)
    assert element is not None
    assert element.component == EndPanel


def test_explanation_panel_element_creation():
    element = ExplanationPanel()
    assert element is not None
    assert element.component == ExplanationPanel
