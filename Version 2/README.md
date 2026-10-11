# AI SHADOW ESCAPE

Autonomous Multi-Agent Pursuit using A* Pathfinding

## Problem Statement

AI Shadow Escape is a grid-based pursuit and escape game. The player must reach an exit while two AI agents track and pursue the player through a maze. The challenge is dynamic because the player moves, gates can change the obstacle map, and the AI must continuously replan valid routes.

## Objective

The objective is to demonstrate AI pathfinding in a playable browser application using Python and Solara. The project preserves the original A* pursuit idea while separating the game engine from the web user interface.

## AI Concepts Used

- A* search
- Manhattan distance heuristic
- Multi-agent pursuit
- Dynamic replanning
- Grid-world maze representation
- Collision and danger detection
- Scoring based on survival, movement, scans and gates

## A* Algorithm Explanation

A* evaluates grid cells using:

```text
f(n) = g(n) + h(n)
```

`g(n)` is the cost from the start node to the current node. `h(n)` is the estimated cost from the current node to the target. The node with the lowest total estimated cost is expanded first.

## Manhattan Heuristic

The game uses Manhattan distance:

```text
h(n) = |x1 - x2| + |y1 - y2|
```

This is appropriate because movement is restricted to up, down, left and right.

## Multi-Agent Pursuit

The game contains two A* agents:

- Hunter: targets the player's current cell.
- Interceptor: targets a short predicted player position based on the player's latest movement direction.

Both agents recalculate when the player moves or when dynamic gates change the maze.

## Dynamic Environment

The maze contains fixed walls and dynamic gates. Gates can open or close during play, forcing the AI agents to replan paths. Gate changes are only accepted when the player still has a valid path to the exit.

## System Architecture

```text
AI / GAME ENGINE
        |
GAME STATE SNAPSHOT
        |
SOLARA UI
        |
BROWSER
```

Important files:

- `solara_app.py`: Solara web entry point.
- `game/pathfinding.py`: A* search and lab metrics.
- `game/engine.py`: gameplay loop, movement, gates, scoring and win/loss checks.
- `game/agents.py`: player, hunter and interceptor models.
- `game/maze.py`: solvable maze generation.
- `ui/board.py`: visual grid board.
- `ui/controls.py`: working controls and difficulty selection.
- `ui/panels.py`: scan, lab evaluation, explanation and end screens.

## How to Install

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## How to Run

```powershell
run_solara.bat
```

Or:

```powershell
python -m solara run solara_app.py --host 127.0.0.1 --port 8766
```

Open the browser URL printed by Solara, normally `http://127.0.0.1:8766`.

## Controls

- START GAME: begins a mission.
- PAUSE: suspends gameplay.
- RESUME: resumes after pause.
- RESTART: resets the current maze.
- SCAN: displays live enemy distance, threat and path length.
- NEW MAZE: generates a new solvable maze.
- UP / W, LEFT / A, DOWN / S, RIGHT / D: move the player using on-screen controls.
- Keyboard: click anywhere on the app page after starting, then use W/A/S/D or arrow keys.

## Difficulty Levels

- EASY: lower wall density, longer launch grace and slower enemy pursuit ticks.
- NORMAL: balanced wall density, dynamic gates and beat-based enemy movement that can be escaped with a good route.
- HARD: higher wall density, faster gates and more frequent enemy pursuit ticks.

## Lab Evaluation Mode

Lab Evaluation Mode displays:

- A* formula
- Manhattan heuristic formula
- Open set count
- Closed set count
- Current node
- Nodes explored
- Path length
- Replanning count

This mode is intended for viva and faculty demonstration.

## Expected Output

The browser shows a dark AI command-center dashboard with a playable maze, visible player, hunter, interceptor, gates, exit, A* path highlights, live metrics, scan results and win/loss reports.

## Credits

Project Creator: Dhanush Naidu  
Registration Number: BL.S.U4AIE25241  
Branch: AIE  
Course: Fundamentals of AIE

## Future Enhancements

- Compare A*, BFS and Greedy Best-First Search.
- Add adaptive AI that learns player patterns.
- Add multiple exits with different path costs.
- Add limited visibility or stealth zones.
- Add persistent leaderboard storage.

