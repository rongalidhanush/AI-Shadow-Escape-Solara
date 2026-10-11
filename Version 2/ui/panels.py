"""Panels — Fullscreen win/loss overlay with restart actions, BFS vs A* lab panel, scan panel, AI intel."""

from __future__ import annotations

import html
from typing import Callable, Optional

import solara

from game.state import GameSnapshot


def _row(label: str, value: str | int, css_class: str = "") -> str:
    val = html.escape(str(value))
    if css_class:
        val = f'<b class="{css_class}">{val}</b>'
    else:
        val = f"<b>{val}</b>"
    return (
        f'<div class="ase-row">'
        f'<span class="ase-muted">{html.escape(label)}</span>'
        f"{val}</div>"
    )


# ── Lab Panel ─────────────────────────────────────────────────────────────────

def _lab_agent_col(agent, label_color: str) -> str:
    emoji = {"Hunter": "👁", "Interceptor": "⚡", "Flanker": "🔮"}.get(agent.role, "?")
    a_nodes = agent.nodes_explored
    b_nodes = agent.bfs_nodes_explored
    delta = b_nodes - a_nodes
    delta_html = (
        f'<span class="ase-delta-up">▲ BFS +{delta}</span>'
        if delta > 0
        else f'<span class="ase-delta-down">▼ BFS {delta}</span>'
    )
    a_path = agent.path_length
    b_path = agent.bfs_path_length

    return (
        f'<div class="ase-agent-col">'
        f'<div class="ase-panel-title" style="color:{label_color};">{emoji} {html.escape(agent.role)}</div>'
        '<div class="ase-readout">'
        + _row("Open Set", agent.open_set_count)
        + _row("Closed Set", agent.closed_set_count)
        + _row("Current Node", str(agent.current_node))
        + _row("A* Path Len", a_path)
        + _row("A* Nodes", a_nodes)
        + _row("BFS Nodes", b_nodes)
        + _row("BFS Path Len", b_path)
        + f'<div class="ase-row"><span class="ase-muted">Node Δ</span>{delta_html}</div>'
        + _row("Replans", agent.recalculations)
        + "</div></div>"
    )


AGENT_COLORS = ["#ff3b5c", "#ff9020", "#bf5af2"]


@solara.component
def LabPanel(snapshot: GameSnapshot):
    if not snapshot.lab_mode:
        return
    cols_html = "".join(
        _lab_agent_col(agent, AGENT_COLORS[i % len(AGENT_COLORS)])
        for i, agent in enumerate(snapshot.agents)
    )
    html_text = (
        '<div class="ase-panel" style="margin-top:14px;">'
        '<div class="ase-panel-title">🔬 Lab Evaluation Mode — A* vs BFS Benchmarks</div>'
        '<div class="ase-code">'
        "<b>Search Formula:</b> f(n) = g(n) + h(n)<br>"
        "<b>g(n):</b> Actual cost from origin | <b>h(n):</b> Heuristic estimate to goal<br>"
        "<b>Manhattan:</b> |x₁-x₂| + |y₁-y₂| | <b>Chebyshev:</b> max(|x₁-x₂|, |y₁-y₂|)"
        "</div>"
        f'<div class="ase-lab-grid">{cols_html}</div>'
        "</div>"
    )
    solara.HTML(tag="div", unsafe_innerHTML=html_text)


# ── Scan Panel ────────────────────────────────────────────────────────────────

@solara.component
def ScanPanel(snapshot: GameSnapshot):
    if not snapshot.scan.active:
        solara.HTML(
            tag="div",
            unsafe_innerHTML=(
                '<div class="ase-panel" style="margin-top:14px;">'
                '<div class="ase-panel-title">🔍 Tactical Shadow Scan</div>'
                '<div class="ase-muted" style="font-size:12px; line-height:1.5;">'
                "Press <b>SCAN</b> in Mission Control to inspect real-time pursuer distances, threat ratings, and trajectories."
                "</div></div>"
            ),
        )
        return

    rows_html = []
    for role, info in snapshot.scan.agents.items():
        emoji = {"Hunter": "👁", "Interceptor": "⚡", "Flanker": "🔮"}.get(role, "?")
        threat = str(info["threat"])
        threat_class = (
            "ase-danger" if threat in {"CRITICAL", "HIGH"}
            else "ase-warn" if threat == "MEDIUM"
            else "ase-good"
        )
        frozen_tag = (
            ' <span style="color:#7ab8dc; font-size:10px;">[FROZEN]</span>'
            if info.get("frozen") == "Yes" else ""
        )
        rows_html.append(
            f'<div class="ase-scan-agent">'
            f'<div style="font-weight:800; font-size:12px; margin-bottom:6px;">{emoji} {html.escape(role)}{frozen_tag}</div>'
            '<div class="ase-readout">'
            + _row("Distance", f"{info['distance']} cells")
            + _row("Threat", threat, threat_class)
            + _row("Path Length", info["path_length"])
            + _row("Target Cell", info["target"])
            + "</div></div>"
        )
    solara.HTML(
        tag="div",
        unsafe_innerHTML=(
            '<div class="ase-panel" style="margin-top:14px; border-color:var(--accent-cyan);">'
            '<div class="ase-panel-title">🔍 Tactical Shadow Scan</div>'
            + "".join(rows_html)
            + "</div>"
        ),
    )


# ── AI Intel / How the AI Works Dossier (GUARANTEED CONTRAST & STYLES) ───────

@solara.component
def ExplanationPanel():
    html_text = """
    <div class="ase-ai-dossier">
        <div class="ase-panel-title" style="color:var(--ai-title-text); font-size:12px; margin-bottom:10px;">
            <span>🤖 AI SYSTEM ARCHITECTURE & ENEMY INTEL</span>
        </div>
        <div style="font-size:12.5px; line-height:1.6; margin-bottom:14px; color:var(--ai-box-muted);">
            AI Shadow Escape utilizes a multi-agent pursuit system powered by real-time <b>A* Pathfinding</b>. Every turn, all three shadow agents independently recalculate optimal trajectories considering walls, dynamic gates, and player motion.
        </div>
        
        <div class="ase-ai-roles-grid">
            <div class="ase-ai-role-card hunter-card">
                <div class="ase-ai-role-header">
                    <span class="ase-ai-role-icon">👁</span>
                    <div>
                        <div class="ase-ai-role-name" style="color:#ff3b5c;">HUNTER</div>
                        <div class="ase-ai-role-badge">Direct Pursuer</div>
                    </div>
                </div>
                <div class="ase-ai-role-desc">
                    Greedily targets your exact current coordinate <code>(x, y)</code> every step. Relentlessly tracks along the mathematically shortest navigable path.
                </div>
            </div>

            <div class="ase-ai-role-card interceptor-card">
                <div class="ase-ai-role-header">
                    <span class="ase-ai-role-icon">⚡</span>
                    <div>
                        <div class="ase-ai-role-name" style="color:#ff9020;">INTERCEPTOR</div>
                        <div class="ase-ai-role-badge">Predictive Ambush</div>
                    </div>
                </div>
                <div class="ase-ai-role-desc">
                    Anticipates your next position 2 steps ahead in your current velocity vector to cut you off at corridors and narrow choke points.
                </div>
            </div>

            <div class="ase-ai-role-card flanker-card">
                <div class="ase-ai-role-header">
                    <span class="ase-ai-role-icon">🔮</span>
                    <div>
                        <div class="ase-ai-role-name" style="color:#bf5af2;">FLANKER</div>
                        <div class="ase-ai-role-badge">Chokepoint Sentry</div>
                    </div>
                </div>
                <div class="ase-ai-role-desc">
                    Navigates directly toward the <b>EXIT 🏁</b> to block your extraction waypoint, preventing rush attempts and forcing evasion maneuvers.
                </div>
            </div>
        </div>

        <div class="ase-ai-rules-grid">
            <div class="ase-ai-rule-item">
                <b>📐 A* Evaluation Function:</b> <code>f(n) = g(n) + h(n)</code> where <code>g(n)</code> is travel cost from origin and <code>h(n)</code> is heuristic distance to goal.
            </div>
            <div class="ase-ai-rule-item">
                <b>⚡ Dynamic Replanning:</b> Whenever you move or a security gate toggles open/closed, all pursuers recalculate their open and closed node sets.
            </div>
            <div class="ase-ai-rule-item">
                <b>✨ Cloak Token:</b> Stepping onto the power-up activates a 5-move cloak, completely freezing all pursuers in their tracks.
            </div>
            <div class="ase-ai-rule-item">
                <b>❤️ 3 Tactical Lives:</b> Each capture costs 1 life and resets your position to the safe zone. Reaching 0 lives results in Mission Failure.
            </div>
        </div>
    </div>
    """
    solara.HTML(tag="div", unsafe_innerHTML=html_text)


# ── Credits Panel ─────────────────────────────────────────────────────────────

@solara.component
def CreditsPanel():
    solara.HTML(
        tag="div",
        unsafe_innerHTML=(
            '<div class="ase-panel ase-credit">'
            '<div class="ase-panel-title" style="color:var(--accent-green);">🎓 Academic Project Credits</div>'
            '<div class="ase-readout">'
            + _row("Student", "Dhanush Naidu")
            + _row("Reg. Number", "BL.S.U4AIE25241")
            + _row("Course", "Fundamentals of AIE")
            + _row("System", "AI Shadow Escape — v2.0")
            + _row("Core AI", "Multi-Agent A*, BFS Benchmarking, Dynamic Replanning")
            + "</div></div>"
        ),
    )


# ── End / Win / Loss Overlay (WITH RESTART, NEW MAZE, NEXT LEVEL BUTTONS) ─────

@solara.component
def EndPanel(
    snapshot: GameSnapshot,
    on_restart: Callable[[], None],
    on_new_maze: Optional[Callable[[], None]] = None,
    on_next_level: Optional[Callable[[int], None]] = None,
):
    if snapshot.status.value not in {"MISSION COMPLETE", "MISSION FAILED"}:
        return

    won = snapshot.status.value == "MISSION COMPLETE"
    title = "🏆 MISSION COMPLETE" if won else "💀 MISSION FAILED"
    subtitle = (
        "Extraction successful! You successfully evaded the AI shadow network."
        if won
        else "Signal compromised. The shadow pursuers intercepted your unit."
    )
    border_color = "var(--accent-green)" if won else "var(--accent-red)"
    title_class = "ase-good" if won else "ase-danger"
    can_next_level = won and snapshot.level_index < 2

    score_items = [
        ("Final Score", str(snapshot.score), "ase-good"),
        ("Total Moves", str(snapshot.moves), ""),
        ("Lives Left", "❤️" * snapshot.lives if snapshot.lives > 0 else "None", "ase-danger" if snapshot.lives == 0 else "ase-good"),
        ("Survival Time", f"{snapshot.elapsed_seconds:.1f}s", ""),
        ("A* Replans", str(snapshot.route_recalculations), "ase-warn"),
        ("Gates Changed", str(snapshot.gates_changed), ""),
    ]
    score_grid = "".join(
        f'<div class="ase-score-item">'
        f'<div class="ase-score-item-label">{html.escape(lbl)}</div>'
        f'<div class="ase-score-item-value {cls}">{html.escape(val)}</div>'
        "</div>"
        for lbl, val, cls in score_items
    )

    with solara.Div(classes=["ase-overlay"]):
        with solara.Div(
            classes=["ase-overlay-card", "win" if won else "loss"],
            style={
                "borderColor": border_color,
                "boxShadow": f"0 12px 60px rgba(0, 0, 0, 0.6)",
            },
        ):
            solara.HTML(
                tag="div",
                unsafe_innerHTML=(
                    f'<div class="ase-overlay-icon">{"🏆" if won else "💀"}</div>'
                    f'<div class="ase-overlay-title {title_class}">{title}</div>'
                    f'<div class="ase-overlay-sub">{html.escape(subtitle)}</div>'
                    f'<div class="ase-score-grid">{score_grid}</div>'
                ),
            )
            with solara.Row(
                style={
                    "gap": "12px",
                    "justifyContent": "center",
                    "marginTop": "22px",
                    "flexWrap": "wrap",
                }
            ):
                if can_next_level and on_next_level:
                    solara.Button(
                        "⏩ NEXT LEVEL",
                        on_click=lambda: on_next_level(snapshot.level_index + 1),
                        color="primary",
                        classes=["ase-modal-btn"],
                        style={"minWidth": "160px"},
                    )
                solara.Button(
                    "↺ PLAY AGAIN",
                    on_click=on_restart,
                    color="success" if won else "error",
                    classes=["ase-modal-btn"],
                    style={"minWidth": "160px"},
                )
                if on_new_maze:
                    solara.Button(
                        "🗺 NEW MAZE",
                        on_click=on_new_maze,
                        color="secondary",
                        classes=["ase-modal-btn"],
                        style={"minWidth": "160px"},
                    )
