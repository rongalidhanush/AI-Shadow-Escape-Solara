from game.engine import GameEngine
from game.pathfinding import astar, astar_search
from game.state import Difficulty, GameStatus


def first_open_direction(engine):
    snapshot = engine.snapshot()
    x, y = snapshot.player
    for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        target = (x + direction[0], y + direction[1])
        if 0 <= target[0] < snapshot.cols and 0 <= target[1] < snapshot.rows and target not in snapshot.walls:
            return direction
    raise AssertionError("start cell has no open neighbor")


def test_maze_generation_and_astar_path():
    engine = GameEngine()
    snapshot = engine.snapshot()
    report = astar_search(snapshot.player, snapshot.exit_cell, snapshot.walls, snapshot.cols, snapshot.rows)
    assert report.path
    assert report.nodes_explored > 0
    assert report.path[0] == snapshot.player
    assert report.path[-1] == snapshot.exit_cell


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
    assert scan.agents["Hunter"]["distance"] >= 0


def test_collision_loss():
    engine = GameEngine()
    engine.start()
    engine.force_collision_for_test()
    assert engine.snapshot().status == GameStatus.LOST


def test_victory():
    engine = GameEngine()
    engine.start()
    engine.force_player_to_exit_for_test()
    snapshot = engine.snapshot()
    assert snapshot.status == GameStatus.WON
    assert snapshot.score >= 0


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


def test_easy_and_normal_can_be_won_by_following_astar_route():
    for difficulty in (Difficulty.EASY, Difficulty.NORMAL):
        engine = GameEngine(difficulty)
        engine.start()
        for _ in range(80):
            snapshot = engine.snapshot()
            if snapshot.status != GameStatus.PLAYING:
                break
            path = astar(snapshot.player, snapshot.exit_cell, snapshot.walls, snapshot.cols, snapshot.rows)
            assert len(path) >= 2
            next_cell = path[1]
            engine.move_player((next_cell[0] - snapshot.player[0], next_cell[1] - snapshot.player[1]))
        assert engine.snapshot().status == GameStatus.WON
