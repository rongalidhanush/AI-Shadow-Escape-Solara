"""Tests for the upgraded AI Shadow Escape engine."""

from game.engine import GameEngine
from game.pathfinding import astar, astar_search, bfs_search, chebyshev, manhattan
from game.state import Difficulty, GameStatus, Heuristic


def first_open_direction(engine):
    snapshot = engine.snapshot()
    x, y = snapshot.player
    for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        target = (x + direction[0], y + direction[1])
        if (
            0 <= target[0] < snapshot.cols
            and 0 <= target[1] < snapshot.rows
            and target not in snapshot.walls
        ):
            return direction
    raise AssertionError("start cell has no open neighbor")


# ── Pathfinding tests ─────────────────────────────────────────────────────────

def test_maze_generation_and_astar_path():
    engine = GameEngine()
    snapshot = engine.snapshot()
    report = astar_search(snapshot.player, snapshot.exit_cell, snapshot.walls, snapshot.cols, snapshot.rows)
    assert report.path
    assert report.nodes_explored > 0
    assert report.path[0] == snapshot.player
    assert report.path[-1] == snapshot.exit_cell


def test_chebyshev_heuristic():
    assert chebyshev((0, 0), (3, 4)) == 4
    assert chebyshev((2, 2), (5, 5)) == 3


def test_manhattan_heuristic():
    assert manhattan((0, 0), (3, 4)) == 7
    assert manhattan((2, 2), (5, 5)) == 6


def test_bfs_finds_path():
    engine = GameEngine()
    snap = engine.snapshot()
    report = bfs_search(snap.player, snap.exit_cell, snap.walls, snap.cols, snap.rows)
    assert report.path
    assert report.path[0] == snap.player
    assert report.path[-1] == snap.exit_cell
    assert report.nodes_explored > 0


def test_chebyshev_astar_finds_path():
    engine = GameEngine()
    engine.set_heuristic(Heuristic.CHEBYSHEV)
    snap = engine.snapshot()
    path = astar(snap.player, snap.exit_cell, snap.walls, snap.cols, snap.rows, "Chebyshev")
    assert path
    assert path[0] == snap.player
    assert path[-1] == snap.exit_cell


# ── Movement & state tests ────────────────────────────────────────────────────

def test_player_move_replans_and_moves_enemies():
    engine = GameEngine()
    engine.start()
    before = engine.snapshot()
    engine.move_player(first_open_direction(engine))
    after = engine.snapshot()
    assert after.moves == before.moves + 1
    assert after.route_recalculations > before.route_recalculations
    assert after.agents[0].path_length >= 0
    assert after.agents[1].path_length >= 0


def test_three_agents_present():
    engine = GameEngine()
    snap = engine.snapshot()
    roles = {a.role for a in snap.agents}
    assert "Hunter" in roles
    assert "Interceptor" in roles
    assert "Flanker" in roles


def test_flanker_targets_exit():
    engine = GameEngine()
    snap = engine.snapshot()
    flanker = next(a for a in snap.agents if a.role == "Flanker")
    assert flanker.target == snap.exit_cell


def test_gate_update_changes_environment():
    engine = GameEngine()
    engine.start()
    before_changes = engine.snapshot().gates_changed
    changed = engine.toggle_next_gate()
    after = engine.snapshot()
    assert changed is True
    assert after.gates_changed == before_changes + 1
    assert len(after.closed_gates) >= 1


def test_scan_returns_real_agent_metrics():
    engine = GameEngine()
    engine.start()
    scan = engine.scan()
    assert scan.active is True
    assert "Hunter" in scan.agents
    assert "Interceptor" in scan.agents
    assert "Flanker" in scan.agents
    assert scan.agents["Hunter"]["distance"] >= 0


# ── Lives system ──────────────────────────────────────────────────────────────

def test_capture_deducts_life_and_respawns():
    engine = GameEngine()
    engine.start()
    assert engine.lives == 3
    engine.force_collision_for_test()
    snap = engine.snapshot()
    # After one capture with 3 lives: still playing, 2 lives left
    assert snap.status == GameStatus.PLAYING
    assert snap.lives == 2


def test_three_captures_cause_loss():
    engine = GameEngine()
    engine.start()
    engine.force_collision_for_test()
    engine.force_collision_for_test()
    engine.force_collision_for_test()
    assert engine.snapshot().status == GameStatus.LOST


def test_victory():
    engine = GameEngine()
    engine.start()
    engine.force_player_to_exit_for_test()
    snapshot = engine.snapshot()
    assert snapshot.status == GameStatus.WON
    assert snapshot.score >= 0


# ── Undo ──────────────────────────────────────────────────────────────────────

def test_undo_reverts_player_position():
    engine = GameEngine()
    engine.start()
    snap_before = engine.snapshot()
    pos_before = snap_before.player
    engine.move_player(first_open_direction(engine))
    assert engine.snapshot().player != pos_before
    engine.undo_move()
    assert engine.snapshot().player == pos_before


def test_undo_unavailable_on_first_move():
    engine = GameEngine()
    engine.start()
    assert engine.snapshot().undo_available is False


# ── Cloak power-up ────────────────────────────────────────────────────────────

def test_cloak_activation_freezes_pursuers():
    engine = GameEngine()
    engine.start()
    # Simulate collecting cloak
    engine.cloak_collected = True
    engine.activate_cloak()
    snap = engine.snapshot()
    assert snap.cloak_active is True
    assert all(a.frozen for a in snap.agents)


# ── Level selection ───────────────────────────────────────────────────────────

def test_level_selection_changes_grid_size():
    engine = GameEngine()
    engine.set_level(0)
    snap0 = engine.snapshot()
    engine.set_level(1)
    snap1 = engine.snapshot()
    engine.set_level(2)
    snap2 = engine.snapshot()
    assert snap1.cols > snap0.cols
    assert snap2.cols > snap1.cols


# ── Difficulty ────────────────────────────────────────────────────────────────

def test_restart_resets_moves():
    engine = GameEngine()
    engine.start()
    engine.move_player(first_open_direction(engine))
    assert engine.snapshot().moves == 1
    engine.restart()
    snapshot = engine.snapshot()
    assert snapshot.status == GameStatus.PLAYING
    assert snapshot.moves == 0


def test_difficulty_affects_gameplay_config():
    easy = GameEngine(Difficulty.EASY)
    hard = GameEngine(Difficulty.HARD)
    easy_walls = len(easy.snapshot().walls)
    hard_walls = len(hard.snapshot().walls)
    assert hard_walls >= easy_walls
    hard.start()
    hard.move_player(first_open_direction(hard))
    assert hard.snapshot().difficulty == Difficulty.HARD


def test_expert_difficulty_exists():
    engine = GameEngine(Difficulty.EXPERT)
    engine.start()
    snap = engine.snapshot()
    assert snap.difficulty == Difficulty.EXPERT


def test_easy_and_normal_can_be_won_by_following_astar_route():
    for difficulty in (Difficulty.EASY, Difficulty.NORMAL):
        engine = GameEngine(difficulty)
        engine.start()
        for _ in range(120):
            snapshot = engine.snapshot()
            if snapshot.status != GameStatus.PLAYING:
                break
            path = astar(snapshot.player, snapshot.exit_cell, snapshot.walls, snapshot.cols, snapshot.rows)
            assert len(path) >= 2
            next_cell = path[1]
            engine.move_player((next_cell[0] - snapshot.player[0], next_cell[1] - snapshot.player[1]))
        assert engine.snapshot().status == GameStatus.WON
