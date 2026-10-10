"""UI-independent AI Shadow Escape game engine."""

from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Dict, Iterable, Set, Tuple

from .agents import Player, Pursuer
from .gates import GateSystem
from .maze import COLS, ROWS, LEVELS, generate_walls
from .pathfinding import astar, manhattan, path_length
from .scoring import Metrics, danger_label, danger_value
from .state import AgentSnapshot, Difficulty, GameSnapshot, GameStatus, ScanReport

Cell = Tuple[int, int]


@dataclass(frozen=True)
class DifficultyConfig:
    wall_density_delta: float
    gate_period_moves: int
    enemy_steps: int
    enemy_move_period: int
    launch_grace_moves: int
    interceptor_replans_every_step: bool


DIFFICULTY_CONFIG: dict[Difficulty, DifficultyConfig] = {
    Difficulty.EASY: DifficultyConfig(-0.06, 7, 1, 3, 5, False),
    Difficulty.NORMAL: DifficultyConfig(-0.02, 5, 1, 3, 4, True),
    Difficulty.HARD: DifficultyConfig(0.03, 4, 1, 2, 3, True),
}


class GameEngine:
    """Plain Python engine that owns state, AI decisions, gates and scoring."""

    def __init__(self, difficulty: Difficulty = Difficulty.NORMAL):
        self.difficulty = difficulty
        self.level_index = 0
        self.seed_counter = 0
        self.status = GameStatus.MENU
        self.lab_mode = False
        self.show_paths = True
        self.message = "System ready. Start the mission to activate A* pursuit."
        self.start_time = time.monotonic()
        self.end_time: float | None = None
        self.player: Player
        self.pursuers: list[Pursuer]
        self.base_walls: Set[Cell] = set()
        self.walls: Set[Cell] = set()
        self.safe_zone: Cell = (0, 0)
        self.gates = GateSystem()
        self.metrics = Metrics()
        self.current_score = 0
        self.last_scan: ScanReport = ScanReport(False, {})
        self.load_level()

    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        self.new_maze()

    def start(self) -> None:
        if self.status in {GameStatus.WON, GameStatus.LOST}:
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
        self.load_level(seed_offset=0)
        self.status = GameStatus.PLAYING
        self.message = "Mission restarted with the same maze profile."

    def new_maze(self) -> None:
        self.load_level(seed_offset=1)
        self.status = GameStatus.PLAYING
        self.message = "New maze generated. A* routes recalculated."

    def toggle_lab_mode(self, enabled: bool) -> None:
        self.lab_mode = enabled

    def toggle_paths(self, enabled: bool) -> None:
        self.show_paths = enabled

    def load_level(self, seed_offset: int = 1) -> None:
        spec = LEVELS[self.level_index]
        self.seed_counter += seed_offset
        config = DIFFICULTY_CONFIG[self.difficulty]
        density = max(0.08, min(0.35, spec.wall_density + config.wall_density_delta))
        seed = 1000 + self.seed_counter
        self.base_walls = generate_walls(spec, COLS, ROWS, seed, density)
        self.walls = set(self.base_walls)
        self.safe_zone = spec.safe_zone
        self.gates = GateSystem(set(spec.gate_candidates), set())
        self.player = Player(spec.start, spec.start)
        self.pursuers = [
            Pursuer(f"Shadow {index + 1}", cell, role, index)
            for index, (cell, role) in enumerate(spec.pursuers)
        ]
        self.metrics = Metrics()
        self.current_score = 0
        self.start_time = time.monotonic()
        self.end_time = None
        self.last_scan = ScanReport(False, {})
        self.status = GameStatus.MENU
        self._recalculate_all("Initial A* paths calculated.")

    def move_player(self, direction: Cell) -> bool:
        if self.status != GameStatus.PLAYING:
            self.message = "Start or resume the mission before moving."
            return False

        moved = self.player.try_move(direction[0], direction[1], self.walls, COLS, ROWS)
        self.metrics.player_distance = self.player.distance_travelled
        if not moved:
            self.metrics.obstacle_collisions += 1
            self.message = "Blocked cell. Wall or closed gate detected."
            return False

        self._update_elapsed()
        self._recalculate_all("Player moved. A* routes replanned.")
        if self._check_victory_or_capture():
            return True

        self._move_pursuers_after_player()
        self._maybe_update_gate()
        self._update_score_preview()
        self._check_victory_or_capture()
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
            }
        self.last_scan = ScanReport(True, agents)
        self.message = "Shadow Scan complete. Enemy distances and path lengths updated."
        self._update_score_preview()
        return self.last_scan

    def _target_for(self, pursuer: Pursuer) -> Cell:
        if pursuer.role == "Interceptor":
            return self._predicted_target()
        return self.player.cell

    def _predicted_target(self) -> Cell:
        x, y = self.player.cell
        dx, dy = self.player.last_direction
        predicted = (max(0, min(COLS - 1, x + dx * 2)), max(0, min(ROWS - 1, y + dy * 2)))
        if predicted in self.walls:
            return self.player.cell
        return predicted

    def _recalculate_all(self, message: str) -> None:
        for pursuer in self.pursuers:
            others = {other.cell for other in self.pursuers if other is not pursuer}
            pursuer.recalculate(self._target_for(pursuer), self.walls, COLS, ROWS, others)
        self.metrics.route_recalculations += len(self.pursuers)
        self.message = message

    def _move_pursuers_after_player(self) -> None:
        config = DIFFICULTY_CONFIG[self.difficulty]
        if self.player.moves <= config.launch_grace_moves:
            self.message = f"Launch grace active. Shadows engage in {config.launch_grace_moves - self.player.moves + 1} move(s)."
            return
        if (self.player.moves - config.launch_grace_moves) % config.enemy_move_period != 0:
            self.message = "A* routes updated. Shadows are tracking before their next pursuit step."
            return
        for _ in range(config.enemy_steps):
            for pursuer in self.pursuers:
                target = self._target_for(pursuer)
                others = {other.cell for other in self.pursuers if other is not pursuer}
                pursuer.move_one_step(target, self.walls, COLS, ROWS, others)
                self.metrics.enemy_steps += 1
                if pursuer.role == "Interceptor" and config.interceptor_replans_every_step:
                    pursuer.recalculate(self._target_for(pursuer), self.walls, COLS, ROWS, others)
                    self.metrics.route_recalculations += 1
                if pursuer.cell == self.player.cell:
                    self._lose()
                    return

    def _maybe_update_gate(self) -> None:
        config = DIFFICULTY_CONFIG[self.difficulty]
        if self.player.moves == 0 or self.player.moves % config.gate_period_moves != 0:
            return
        self.toggle_next_gate()

    def toggle_next_gate(self) -> bool:
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
            gate_message = "Gate opened. Routes replanned through dynamic environment."
        else:
            proposed = set(self.gates.closed)
            proposed.add(cell)
            proposed_walls = set(self.base_walls) | proposed
            changed = bool(astar(self.player.cell, self.safe_zone, proposed_walls, COLS, ROWS))
            if changed:
                self.gates.closed.add(cell)
                gate_message = "Gate closed. A* network forced to replan."
            else:
                gate_message = "Gate change skipped to preserve a valid escape route."
        self.walls = set(self.base_walls) | set(self.gates.closed)
        if changed:
            self.metrics.gates_changed += 1
            self._recalculate_all(gate_message)
        return changed

    def _check_victory_or_capture(self) -> bool:
        if self.player.cell == self.safe_zone:
            self._win()
            return True
        if self.player.cell in {p.cell for p in self.pursuers}:
            self._lose()
            return True
        return False

    def _win(self) -> None:
        if self.status != GameStatus.PLAYING:
            return
        self.metrics.successful_escape = True
        self._update_elapsed()
        optimal = path_length(astar(self.player.start_cell, self.safe_zone, self.walls, COLS, ROWS))
        self.current_score = self.metrics.final_score(optimal)
        self.status = GameStatus.WON
        self.end_time = time.monotonic()
        self.message = "MISSION COMPLETE: You escaped the AI shadows."

    def _lose(self) -> None:
        if self.status != GameStatus.PLAYING:
            return
        self._update_elapsed()
        self.metrics.capture_time = self.metrics.elapsed_seconds
        self.current_score = 0
        self.status = GameStatus.LOST
        self.end_time = time.monotonic()
        self.message = "MISSION FAILED: The shadows intercepted you."

    def _update_elapsed(self) -> None:
        if self.status == GameStatus.PLAYING:
            self.metrics.elapsed_seconds = time.monotonic() - self.start_time

    def _update_score_preview(self) -> None:
        nearest = self._nearest_distance()
        survival = int(self.metrics.elapsed_seconds * 4)
        movement = self.player.moves * 12
        danger_bonus = max(0, nearest * 3)
        penalties = self.metrics.scans_used * 8 + self.metrics.obstacle_collisions * 15
        self.current_score = max(0, 250 + survival + movement + danger_bonus + self.metrics.gates_changed * 15 - penalties)

    def _nearest_distance(self) -> int:
        distances = [manhattan(p.cell, self.player.cell) for p in self.pursuers]
        return min(distances) if distances else 99

    def snapshot(self) -> GameSnapshot:
        self._update_elapsed()
        nearest = self._nearest_distance()
        agents = []
        for pursuer in self.pursuers:
            report = pursuer.last_report
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
                )
            )
        return GameSnapshot(
            status=self.status,
            difficulty=self.difficulty,
            cols=COLS,
            rows=ROWS,
            level_name=LEVELS[self.level_index].name,
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
            scan=self.last_scan,
        )

    def force_player_to_exit_for_test(self) -> None:
        self.player.cell = self.safe_zone
        self._win()

    def force_collision_for_test(self) -> None:
        self.pursuers[0].cell = self.player.cell
        self._lose()
