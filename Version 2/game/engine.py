"""UI-independent AI Shadow Escape game engine — Upgraded Edition."""

from __future__ import annotations

from dataclasses import dataclass
import random
import time
from typing import Dict, List, Optional, Set, Tuple

from .agents import Player, Pursuer
from .gates import GateSystem
from .maze import LEVELS, LevelSpec, generate_walls
from .pathfinding import astar, manhattan, path_length
from .scoring import Metrics, danger_label, danger_value
from .state import (
    AgentSnapshot,
    Difficulty,
    GameSnapshot,
    GameStatus,
    Heuristic,
    ScanReport,
)

Cell = Tuple[int, int]

CLOAK_FREEZE_MOVES = 5   # pursuer freeze duration
MAX_LIVES = 3


@dataclass(frozen=True)
class DifficultyConfig:
    wall_density_delta: float
    gate_period_moves: int
    enemy_steps: int
    enemy_move_period: int
    launch_grace_moves: int
    interceptor_replans_every_step: bool


DIFFICULTY_CONFIG: dict[Difficulty, DifficultyConfig] = {
    Difficulty.EASY:   DifficultyConfig(-0.06, 8, 1, 4, 6, False),
    Difficulty.NORMAL: DifficultyConfig(-0.02, 5, 1, 3, 4, True),
    Difficulty.HARD:   DifficultyConfig(0.03,  4, 1, 2, 3, True),
    Difficulty.EXPERT: DifficultyConfig(0.06,  3, 2, 1, 2, True),
}


class GameEngine:
    """Plain Python engine that owns state, AI decisions, gates, scoring and new power-ups."""

    def __init__(self, difficulty: Difficulty = Difficulty.NORMAL):
        self.difficulty = difficulty
        self.heuristic = Heuristic.MANHATTAN
        self.level_index = 0
        self.seed_counter = 0
        self.status = GameStatus.MENU
        self.lab_mode = False
        self.show_paths = True
        self.message = "System ready. Start the mission to activate A* pursuit."
        self.start_time = time.monotonic()
        self.end_time: Optional[float] = None
        self.player: Player
        self.pursuers: List[Pursuer]
        self.base_walls: Set[Cell] = set()
        self.walls: Set[Cell] = set()
        self.safe_zone: Cell = (0, 0)
        self.gates = GateSystem()
        self.metrics = Metrics()
        self.current_score = 0
        self.last_scan: ScanReport = ScanReport(False, {})
        # Lives & power-up
        self.lives = MAX_LIVES
        self.cloak_active = False
        self.cloak_moves_left = 0
        self.cloak_collected = False   # becomes True once player steps on power-up
        self.power_up_cell: Optional[Cell] = None
        self.load_level()

    # ── Public API ────────────────────────────────────────────────────────────

    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        self.new_maze()

    def set_heuristic(self, heuristic: Heuristic) -> None:
        self.heuristic = heuristic
        self._recalculate_all("Heuristic changed. A* routes recalculated.")

    def set_level(self, index: int) -> None:
        self.level_index = max(0, min(index, len(LEVELS) - 1))
        self.seed_counter = 0
        self.load_level()
        self.status = GameStatus.PLAYING
        self.message = f"Level {self.level_index + 1}: {LEVELS[self.level_index].name} loaded."

    def start(self) -> None:
        if self.status in {GameStatus.WON, GameStatus.LOST}:
            self.lives = MAX_LIVES
            self.load_level()
        self.status = GameStatus.PLAYING
        self.start_time = time.monotonic()
        self.end_time = None
        self.message = "Mission online. A* shadows are tracking the player."

    def pause(self) -> None:
        if self.status == GameStatus.PLAYING:
            self._update_elapsed()
            self.status = GameStatus.PAUSED
            self.message = "Mission paused. AI movement suspended."

    def resume(self) -> None:
        if self.status == GameStatus.PAUSED:
            self.start_time = time.monotonic() - self.metrics.elapsed_seconds
            self.status = GameStatus.PLAYING
            self.message = "Mission resumed. Pursuit paths restored."

    def restart(self) -> None:
        self.lives = MAX_LIVES
        self.load_level(seed_offset=0)
        self.status = GameStatus.PLAYING
        self.message = "Mission restarted with the same maze profile."

    def new_maze(self) -> None:
        self.lives = MAX_LIVES
        self.load_level(seed_offset=1)
        self.status = GameStatus.PLAYING
        self.message = "New maze generated. A* routes recalculated."

    def toggle_lab_mode(self, enabled: bool) -> None:
        self.lab_mode = enabled

    def toggle_paths(self, enabled: bool) -> None:
        self.show_paths = enabled

    def load_level(self, seed_offset: int = 1) -> None:
        spec: LevelSpec = LEVELS[self.level_index]
        self.seed_counter += seed_offset
        config = DIFFICULTY_CONFIG[self.difficulty]
        density = max(0.08, min(0.38, spec.wall_density + config.wall_density_delta))
        seed = 1000 + self.seed_counter + self.level_index * 100
        self.base_walls = generate_walls(spec, seed, density)
        self.walls = set(self.base_walls)
        self.safe_zone = spec.safe_zone
        self.gates = GateSystem(set(spec.gate_candidates), set())
        self.player = Player(spec.start, spec.start)
        self.pursuers = [
            Pursuer(f"Shadow {idx + 1}", cell, role, idx)
            for idx, (cell, role) in enumerate(spec.pursuers)
        ]
        self.metrics = Metrics()
        self.current_score = 0
        self.start_time = time.monotonic()
        self.end_time = None
        self.last_scan = ScanReport(False, {})
        self.status = GameStatus.MENU
        # Pick a random power-up location from candidates
        candidates = [c for c in spec.power_up_candidates if c not in self.base_walls]
        self.power_up_cell = random.choice(candidates) if candidates else None
        self.cloak_active = False
        self.cloak_moves_left = 0
        self.cloak_collected = False
        self._recalculate_all("Initial A* paths calculated.")

    def move_player(self, direction: Cell) -> bool:
        if self.status != GameStatus.PLAYING:
            self.message = "Start or resume the mission before moving."
            return False

        moved = self.player.try_move(direction[0], direction[1], self.walls, *self._dims())
        self.metrics.player_distance = self.player.distance_travelled
        if not moved:
            self.metrics.obstacle_collisions += 1
            self.message = "Blocked cell. Wall or closed gate detected."
            return False

        # Cloak countdown
        if self.cloak_active:
            self.cloak_moves_left -= 1
            if self.cloak_moves_left <= 0:
                self.cloak_active = False
                self.message = "Cloak worn off. Shadows resuming pursuit."

        # Check power-up collection
        self._maybe_collect_power_up()

        self._update_elapsed()
        self._recalculate_all()
        if self._check_victory_or_capture():
            return True

        self._move_pursuers_after_player()
        self._maybe_update_gate()
        self._update_score_preview()
        self._check_victory_or_capture()
        return True

    def undo_move(self) -> bool:
        """Undo the last player move (costs score)."""
        if self.status != GameStatus.PLAYING:
            return False
        if not self.player.undo():
            self.message = "No move to undo."
            return False
        self.metrics.undo_used += 1
        self._recalculate_all("Move undone. A* routes recalculated.")
        self._update_score_preview()
        self.message = f"Move undone. (-{5} score penalty)"
        return True

    def activate_cloak(self) -> bool:
        """Activate cloak power-up — freeze all pursuers for CLOAK_FREEZE_MOVES moves."""
        if not self.cloak_collected or self.cloak_active:
            return False
        self.cloak_active = True
        self.cloak_moves_left = CLOAK_FREEZE_MOVES
        self.metrics.cloak_used += 1
        for p in self.pursuers:
            p.freeze(CLOAK_FREEZE_MOVES)
        self.message = f"CLOAK ACTIVE! Shadows frozen for {CLOAK_FREEZE_MOVES} moves."
        return True

    def scan(self) -> ScanReport:
        self.metrics.scans_used += 1
        agents: Dict[str, Dict[str, str | int]] = {}
        for agent in self.pursuers:
            dist = manhattan(agent.cell, self.player.cell)
            agents[agent.role] = {
                "distance": dist,
                "threat": danger_label(dist),
                "path_length": path_length(agent.path),
                "target": str(agent.current_target),
                "frozen": "Yes" if agent.frozen else "No",
            }
        self.last_scan = ScanReport(True, agents)
        self.message = "Shadow Scan complete. Enemy distances and path lengths updated."
        self._update_score_preview()
        return self.last_scan

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _dims(self) -> tuple[int, int]:
        spec = LEVELS[self.level_index]
        return spec.cols, spec.rows

    def _target_for(self, pursuer: Pursuer) -> Cell:
        if pursuer.role == "Flanker":
            return self.safe_zone          # cut off the exit
        if pursuer.role == "Interceptor":
            return self._predicted_target()
        return self.player.cell

    def _predicted_target(self) -> Cell:
        cols, rows = self._dims()
        x, y = self.player.cell
        dx, dy = self.player.last_direction
        predicted = (
            max(0, min(cols - 1, x + dx * 2)),
            max(0, min(rows - 1, y + dy * 2)),
        )
        if predicted in self.walls:
            return self.player.cell
        return predicted

    def _recalculate_all(self, message: Optional[str] = None) -> None:
        cols, rows = self._dims()
        h = self.heuristic.value
        for pursuer in self.pursuers:
            others = {other.cell for other in self.pursuers if other is not pursuer}
            pursuer.recalculate(self._target_for(pursuer), self.walls, cols, rows, others, h)
        self.metrics.route_recalculations += len(self.pursuers)
        if message is not None:
            self.message = message

    def _move_pursuers_after_player(self) -> None:
        config = DIFFICULTY_CONFIG[self.difficulty]
        cols, rows = self._dims()
        h = self.heuristic.value
        if self.player.moves <= config.launch_grace_moves:
            return
        if (self.player.moves - config.launch_grace_moves) % config.enemy_move_period != 0:
            return
        for _ in range(config.enemy_steps):
            for pursuer in self.pursuers:
                target = self._target_for(pursuer)
                others = {other.cell for other in self.pursuers if other is not pursuer}
                pursuer.move_one_step(target, self.walls, cols, rows, others, h)
                self.metrics.enemy_steps += 1
                if pursuer.role == "Interceptor" and config.interceptor_replans_every_step:
                    pursuer.recalculate(self._target_for(pursuer), self.walls, cols, rows, others, h)
                    self.metrics.route_recalculations += 1
                # Flanker replans every step too (dynamic blocking)
                if pursuer.role == "Flanker":
                    pursuer.recalculate(self._target_for(pursuer), self.walls, cols, rows, others, h)
                    self.metrics.route_recalculations += 1
                if pursuer.cell == self.player.cell:
                    self._capture()
                    return

    def _maybe_update_gate(self) -> None:
        config = DIFFICULTY_CONFIG[self.difficulty]
        if self.player.moves == 0 or self.player.moves % config.gate_period_moves != 0:
            return
        self.toggle_next_gate()

    def toggle_next_gate(self) -> bool:
        cols, rows = self._dims()
        candidates = [
            cell
            for cell in self.gates.ordered_candidates()
            if cell not in {self.player.cell, self.safe_zone, *(p.cell for p in self.pursuers)}
        ]
        if not candidates:
            return False
        cell = candidates[self.gates.cursor % len(candidates)]
        self.gates.cursor += 1
        if cell in self.gates.closed:
            self.gates.closed.remove(cell)
            changed = True
        else:
            proposed = set(self.gates.closed)
            proposed.add(cell)
            proposed_walls = set(self.base_walls) | proposed
            changed = bool(astar(self.player.cell, self.safe_zone, proposed_walls, cols, rows))
            if changed:
                self.gates.closed.add(cell)
        self.walls = set(self.base_walls) | set(self.gates.closed)
        if changed:
            self.metrics.gates_changed += 1
            self._recalculate_all()
        return changed

    def _maybe_collect_power_up(self) -> None:
        if self.power_up_cell and self.player.cell == self.power_up_cell:
            self.cloak_collected = True
            self.power_up_cell = None
            self.message = "🔮 CLOAK collected! Press ACTIVATE CLOAK to freeze shadows."

    def _check_victory_or_capture(self) -> bool:
        if self.player.cell == self.safe_zone:
            self._win()
            return True
        if self.player.cell in {p.cell for p in self.pursuers}:
            self._capture()
            return True
        return False

    def _capture(self) -> None:
        """Handle a capture event — deduct a life or end the game."""
        if self.status != GameStatus.PLAYING:
            return
        self.lives -= 1
        self.metrics.lives_lost += 1
        if self.lives <= 0:
            self._lose()
        else:
            # Respawn at start — reset player but keep maze
            spec = LEVELS[self.level_index]
            self.player = Player(spec.start, spec.start)
            self.cloak_active = False
            self.cloak_moves_left = 0
            self.message = (
                f"Captured! {self.lives} {'life' if self.lives == 1 else 'lives'} remaining. "
                "Respawning at start…"
            )
            self._recalculate_all(self.message)

    def _win(self) -> None:
        if self.status != GameStatus.PLAYING:
            return
        self.metrics.successful_escape = True
        self._update_elapsed()
        cols, rows = self._dims()
        optimal = path_length(astar(self.player.start_cell, self.safe_zone, self.walls, cols, rows))
        self.current_score = self.metrics.final_score(optimal)
        self.status = GameStatus.WON
        self.end_time = time.monotonic()
        self.message = "🏆 MISSION COMPLETE: You escaped the AI shadows!"

    def _lose(self) -> None:
        if self.status != GameStatus.PLAYING:
            return
        self._update_elapsed()
        self.metrics.capture_time = self.metrics.elapsed_seconds
        self.current_score = 0
        self.status = GameStatus.LOST
        self.end_time = time.monotonic()
        self.message = "💀 MISSION FAILED: The shadows intercepted you."

    def _update_elapsed(self) -> None:
        if self.status == GameStatus.PLAYING:
            self.metrics.elapsed_seconds = time.monotonic() - self.start_time

    def _update_score_preview(self) -> None:
        nearest = self._nearest_distance()
        survival = int(self.metrics.elapsed_seconds * 4)
        movement = self.player.moves * 12
        danger_bonus = max(0, nearest * 3)
        penalties = (
            self.metrics.scans_used * 8
            + self.metrics.obstacle_collisions * 15
            + self.metrics.undo_used * 5
        )
        lives_bonus = (MAX_LIVES - self.metrics.lives_lost) * 80
        self.current_score = max(
            0,
            250 + survival + movement + danger_bonus
            + self.metrics.gates_changed * 15
            + lives_bonus
            - penalties,
        )

    def _nearest_distance(self) -> int:
        distances = [manhattan(p.cell, self.player.cell) for p in self.pursuers]
        return min(distances) if distances else 99

    def snapshot(self) -> GameSnapshot:
        self._update_elapsed()
        nearest = self._nearest_distance()
        spec = LEVELS[self.level_index]
        agents = []
        for pursuer in self.pursuers:
            report = pursuer.last_report
            bfs_report = pursuer.last_bfs_report
            agents.append(
                AgentSnapshot(
                    name=pursuer.name,
                    role=pursuer.role,
                    cell=pursuer.cell,
                    path=list(pursuer.path),
                    path_length=path_length(pursuer.path),
                    distance_to_player=manhattan(pursuer.cell, self.player.cell),
                    target=pursuer.current_target,
                    open_set_count=report.open_set_count if report else 0,
                    closed_set_count=report.closed_set_count if report else 0,
                    current_node=report.current_node if report else None,
                    nodes_explored=report.nodes_explored if report else 0,
                    recalculations=pursuer.route_recalculations,
                    frozen=pursuer.frozen,
                    bfs_nodes_explored=bfs_report.nodes_explored if bfs_report else 0,
                    bfs_path_length=bfs_report.path_length if bfs_report else 0,
                )
            )
        return GameSnapshot(
            status=self.status,
            difficulty=self.difficulty,
            heuristic=self.heuristic,
            cols=spec.cols,
            rows=spec.rows,
            level_index=self.level_index,
            level_name=spec.name,
            player=self.player.cell,
            exit_cell=self.safe_zone,
            walls=set(self.walls),
            gate_cells=set(self.gates.candidates),
            closed_gates=set(self.gates.closed),
            agents=agents,
            score=self.current_score,
            moves=self.player.moves,
            elapsed_seconds=self.metrics.elapsed_seconds,
            route_recalculations=self.metrics.route_recalculations,
            obstacle_collisions=self.metrics.obstacle_collisions,
            gates_changed=self.metrics.gates_changed,
            scans_used=self.metrics.scans_used,
            nearest_distance=nearest,
            danger_label=danger_label(nearest),
            danger_value=danger_value(nearest),
            message=self.message,
            lab_mode=self.lab_mode,
            show_paths=self.show_paths,
            lives=self.lives,
            cloak_active=self.cloak_active,
            cloak_moves_left=self.cloak_moves_left,
            cloak_collected=self.cloak_collected,
            undo_available=self.player.prev_cell is not None,
            power_up_cell=self.power_up_cell,
            scan=self.last_scan,
        )

    # ── Test helpers ──────────────────────────────────────────────────────────

    def force_player_to_exit_for_test(self) -> None:
        self.player.cell = self.safe_zone
        self._win()

    def force_collision_for_test(self) -> None:
        self.pursuers[0].cell = self.player.cell
        self._capture()
