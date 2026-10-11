# AI SHADOW ESCAPE
### Autonomous Multi-Agent Pursuit using A* Pathfinding

## 🚀 Live Demo

🎮 **Play AI Shadow Escape online!**

Experience the game directly in your browser without installing anything locally.

### 👉 [PLAY AI SHADOW ESCAPE — LIVE DEMO](https://ai-shadow-escape.onrender.com/)

**Explore the following features:**
- 🧠 A* pathfinding with the Manhattan distance heuristic
- 🤖 Two intelligent AI agents: Hunter and Interceptor
- 🗺️ Dynamic maze navigation and gate changes
- 📊 Live AI metrics and pathfinding analysis
- 🎯 Three difficulty levels: Easy, Normal, and Hard
- 🔬 Lab Evaluation Mode for understanding the AI algorithm
- 🎮 Interactive gameplay with keyboard and on-screen controls

> **Note:** The application is hosted on Render. If the service has been inactive, the first page load may take a little longer while it starts.

---

## 📌 Problem Statement

AI Shadow Escape is a grid-based pursuit and escape game. The player must reach an exit while two AI agents track and pursue the player through a maze.

The challenge is dynamic because the player moves, gates can change the obstacle map, and the AI must continuously replan valid routes.

## 🎯 Objective

The objective is to demonstrate AI pathfinding in a playable browser application using Python and Solara.

The project preserves the original A* pursuit idea while separating the game engine from the web user interface.

## 🧠 AI Concepts Used

- A* search
- Manhattan distance heuristic
- Multi-agent pursuit
- Dynamic replanning
- Grid-world maze representation
- Collision and danger detection
- Scoring based on survival, movement, scans and gates

## 🔍 A* Algorithm Explanation

A* evaluates grid cells using the following formula:

```text
f(n) = g(n) + h(n)
```

Where:

- `g(n)` is the cost from the start node to the current node.
- `h(n)` is the estimated cost from the current node to the target.
- `f(n)` is the total estimated cost of a path through the current node.

The node with the lowest total estimated cost is expanded first.

## 📐 Manhattan Heuristic

The game uses Manhattan distance:

```text
h(n) = |x1 - x2| + |y1 - y2|
```

This heuristic is appropriate because movement is restricted to four directions:

- Up
- Down
- Left
- Right

It estimates the minimum number of horizontal and vertical steps between two cells, ignoring obstacles.

## 🤖 Multi-Agent Pursuit

The game contains two A* agents.

### 1. Hunter

- Targets the player's current cell.
- Calculates a route through the maze.
- Replans its route as the player moves.

### 2. Interceptor

- Targets a short predicted player position based on the player's latest movement direction.
- Attempts to anticipate the player's movement.
- Recalculates its route as the game state changes.

Both agents recalculate when the player moves or when dynamic gates change the maze.

## 🗺️ Dynamic Environment

The maze contains fixed walls and dynamic gates.

Gates can open or close during play, forcing the AI agents to replan their paths.

Gate changes are only accepted when the player still has a valid path to the exit.

This demonstrates how pathfinding algorithms can operate in a changing environment rather than relying on a single fixed route.

## 🏗️ System Architecture

```text
       AI / GAME ENGINE
               |
               v
       GAME STATE SNAPSHOT
               |
               v
           SOLARA UI
               |
               v
            BROWSER
```

The application separates game logic from the user interface, making the project easier to understand, maintain and extend.

## 📂 Project Structure

Important files and directories:

| File or Directory | Purpose |
|---|---|
| `solara_app.py` | Main Solara web application entry point |
| `game/pathfinding.py` | A* search and lab metrics |
| `game/engine.py` | Gameplay, movement, gates, scoring and win/loss checks |
| `game/agents.py` | Player, Hunter and Interceptor models |
| `game/maze.py` | Solvable maze generation |
| `ui/board.py` | Visual game board |
| `ui/controls.py` | Game controls and difficulty selection |
| `ui/panels.py` | Scan, lab evaluation, explanations and end screens |
| `requirements.txt` | Python dependencies |
| `run_solara.bat` | Windows startup script |
| `tests/` | Project tests |

## ⚙️ Installation

To run the project locally, ensure Python is installed.

Open a terminal in the project directory and execute:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

## ▶️ How to Run

### Method 1: Using the Windows startup script

```powershell
run_solara.bat
```

### Method 2: Running Solara directly

```powershell
python -m solara run solara_app.py --host 127.0.0.1 --port 8766
```

Open the browser URL printed by Solara, normally:

```text
http://127.0.0.1:8766
```

## 🎮 Game Controls

| Control | Function |
|---|---|
| START GAME | Begins a mission |
| PAUSE | Suspends gameplay |
| RESUME | Resumes a paused game |
| RESTART | Resets the current maze |
| SCAN | Displays enemy distance, threat and path length |
| NEW MAZE | Generates a new solvable maze |
| UP / W | Moves the player upward |
| DOWN / S | Moves the player downward |
| LEFT / A | Moves the player left |
| RIGHT / D | Moves the player right |

### Keyboard Controls

Click the application page after starting the game, then use:

- `W` or `↑` — Move up
- `A` or `←` — Move left
- `S` or `↓` — Move down
- `D` or `→` — Move right

On-screen controls are also available.

## 🎯 Difficulty Levels

### EASY
- Lower wall density
- Longer launch grace period
- Slower enemy pursuit ticks

### NORMAL
- Balanced wall density
- Dynamic gates
- Beat-based enemy movement that can be escaped with a good route

### HARD
- Higher wall density
- Faster gates
- More frequent enemy pursuit ticks

## 🔬 Lab Evaluation Mode

Lab Evaluation Mode displays information about the pathfinding process.

It includes:

- A* formula
- Manhattan heuristic formula
- Open set count
- Closed set count
- Current node
- Nodes explored
- Path length
- Replanning count

This mode is intended for academic demonstrations, algorithm analysis and viva presentations.

## 📊 Expected Output

The application presents a dark AI command-center dashboard containing:

- A playable maze
- A visible player
- Hunter and Interceptor agents
- Dynamic gates and an exit
- A* path highlights
- Live metrics
- Scan results
- Win/loss reports

The interface provides visual feedback about the player's progress and the AI agents' pursuit behaviour.

## 🌐 Deployment

AI Shadow Escape is deployed using Render.

**Live application:**

👉 https://ai-shadow-escape.onrender.com/

The application can be accessed through a web browser without requiring users to install Python or the project dependencies locally.

## 👨‍💻 Credits

- **Project Creator:** Dhanush Naidu
- **Registration Number:** BL.SU4AIE25241
- **Branch:** AIE
- **Course:** Fundamentals of AIE

## 🔮 Future Enhancements

Potential improvements include:

- Comparing A* with BFS and Greedy Best-First Search
- Adding adaptive AI that learns player patterns
- Introducing multiple exits with different path costs
- Adding limited-visibility mechanics or stealth zones
- Implementing persistent leaderboard storage

---

## 🎮 Try the Game

### Ready to escape?

**[🚀 LAUNCH AI SHADOW ESCAPE](https://ai-shadow-escape.onrender.com/)**

Navigate the maze, avoid the pursuing agents, use your knowledge of the environment, and reach the exit!

---
