"""Panels — fullscreen win/loss overlay, BFS vs A* lab panel, scan panel, credits."""

from __future__ import annotations

import html

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
    # BFS vs A* delta comparison
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
        + _row("BFS vs A*", "", )
        + f'<div class="ase-row"><span class="ase-muted">Node Δ</span>{delta_html}</div>'
        + _row("Replans", agent.recalculations)
        + "</div></div>"
    )


AGENT_COLORS = ["#ff6080", "#ff9020", "#c08fff"]


@solara.component
def LabPanel(snapshot: GameSnapshot):
    if not snapshot.lab_mode:
        return
    cols_html = "".join(
        _lab_agent_col(agent, AGENT_COLORS[i % len(AGENT_COLORS)])
        for i, agent in enumerate(snapshot.agents)
    )
    html_text = (
        '<div class="ase-panel" style="margin-top:12px;">'
        '<div class="ase-panel-title">🔬 Lab Evaluation Mode</div>'
        '<div class="ase-code">'
        "f(n) = g(n) + h(n)<br>"
        "g(n) = cost from start node<br>"
        "h(n) = estimated cost to goal<br>"
        "Manhattan: h(n) = |x₁-x₂| + |y₁-y₂|<br>"
        "Chebyshev: h(n) = max(|x₁-x₂|, |y₁-y₂|)"
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
                '<div class="ase-panel" style="margin-top:12px;">'
                '<div class="ase-panel-title">🔍 Shadow Scan</div>'
                '<div class="ase-muted" style="font-size:12px;">'
                "Press SCAN to inspect live enemy distance, threat and path length."
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
            ' <span style="color:#7ab8dc;">[FROZEN]</span>'
            if info.get("frozen") == "Yes" else ""
        )
        rows_html.append(
            f'<div class="ase-scan-agent">'
            f'<div style="font-weight:700; margin-bottom:6px;">{emoji} {html.escape(role)}{frozen_tag}</div>'
            '<div class="ase-readout">'
            + _row("Distance", f"{info['distance']} cells")
            + _row("Threat", threat)
            + _row("Path Length", info["path_length"])
            + _row("Target", info["target"])
            + "</div></div>"
        )
    solara.HTML(
        tag="div",
        unsafe_innerHTML=(
            '<div class="ase-panel" style="margin-top:12px; border-color:rgba(49,216,255,.5);">'
            '<div class="ase-panel-title">🔍 Shadow Scan</div>'
            + "".join(rows_html)
            + "</div>"
        ),
    )


# ── Explanation Panel ─────────────────────────────────────────────────────────

@solara.component
def ExplanationPanel():
    solara.Markdown(
        """
<details class="ase-panel" style="margin-top:12px;">
<summary class="ase-panel-title">❓ How the AI Works</summary>

1. The maze is a grid with walls and dynamic gates.
2. Three AI agents each run their own A* search every move.
3. **Hunter 👁** — targets your current cell directly.
4. **Interceptor ⚡** — predicts your next position (2 steps ahead in last direction).
5. **Flanker 🔮** — targets the EXIT to cut off your escape route.
6. Manhattan or Chebyshev distance estimates the remaining cost.
7. When you move or a gate changes, all agents replan.
8. Collect the ✨ Cloak token to freeze all agents for 5 moves.
9. You have 3 lives — each capture costs one life and respawns you.

</details>
""",
        unsafe_solara_execute=False,
    )


# ── Credits Panel ─────────────────────────────────────────────────────────────

@solara.component
def CreditsPanel():
    solara.HTML(
        tag="div",
        unsafe_innerHTML=(
            '<div class="ase-panel ase-credit">'
            '<div class="ase-panel-title" style="color:#2ee889;">🎓 Project Credits</div>'
            '<div class="ase-readout">'
            + _row("Name", "Dhanush Naidu")
            + _row("Reg. Number", "BL.S.U4AIE25241")
            + _row("Course", "Fundamentals of AIE")
            + _row("Project", "AI Shadow Escape — v2")
            + _row("AI Concepts", "A*, BFS, Multi-Agent, Dynamic Env.")
            + "</div></div>"
        ),
    )


# ── End / Win / Loss Overlay ──────────────────────────────────────────────────

@solara.component
def EndPanel(snapshot: GameSnapshot, play_again):
    if snapshot.status.value not in {"MISSION COMPLETE", "MISSION FAILED"}:
        return

    won = snapshot.status.value == "MISSION COMPLETE"
    title = "🏆 MISSION COMPLETE" if won else "💀 MISSION FAILED"
    subtitle = "You outfoxed the AI shadows!" if won else "The shadows intercepted you."
    border_color = "#2ee889" if won else "#ff4060"
    title_class = "ase-good" if won else "ase-danger"

    score_items = [
        ("Final Score", str(snapshot.score), "ase-good"),
        ("Moves", str(snapshot.moves), ""),
        ("Lives Left", "❤️" * snapshot.lives, ""),
        ("Survival", f"{snapshot.elapsed_seconds:.1f}s", ""),
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

    solara.HTML(
        tag="div",
        unsafe_innerHTML=(
            '<div class="ase-overlay">'
            f'<div class="ase-overlay-card" style="border-color:{border_color}; '
            f'box-shadow: 0 0 60px {border_color}44;">'
            f'<div class="ase-overlay-title {title_class}">{title}</div>'
            f'<div class="ase-overlay-sub">{html.escape(subtitle)}</div>'
            f'<div class="ase-score-grid">{score_grid}</div>'
            "</div></div>"
        ),
    )
    with solara.Column(style={"alignItems": "center", "marginTop": "12px"}):
        solara.Button(
            "▶ PLAY AGAIN",
            on_click=play_again,
            color="success",
            style={"width": "100%", "minHeight": "44px", "fontWeight": "800", "fontSize": "15px"},
        )
