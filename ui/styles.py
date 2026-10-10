"""Shared visual styles — Upgraded Edition with glassmorphism, animated danger, emoji cells."""

PAGE_CSS = """
<style>
/* ── Reset & Base ─────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
body { background: #030810 !important; margin: 0; }

/* ── Root Container ───────────────────────────────────────────────────────── */
.ase-root {
    min-height: 100vh;
    color: #e8f4ff;
    background:
        linear-gradient(rgba(49,216,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(49,216,255,0.03) 1px, transparent 1px),
        radial-gradient(ellipse at 15% 10%, rgba(0,217,255,0.18) 0%, transparent 40%),
        radial-gradient(ellipse at 85% 90%, rgba(255,60,120,0.15) 0%, transparent 38%),
        radial-gradient(ellipse at 50% 50%, rgba(120,0,255,0.08) 0%, transparent 60%),
        linear-gradient(160deg, #030810 0%, #080e1c 50%, #0c1322 100%);
    background-size: 28px 28px, 28px 28px, auto, auto, auto, auto;
    font-family: "Segoe UI", "Inter", Arial, sans-serif;
    padding: 16px 20px;
}

/* ── Shell ────────────────────────────────────────────────────────────────── */
.ase-shell { max-width: 1560px; margin: 0 auto; }

/* ── Typography ───────────────────────────────────────────────────────────── */
.ase-title {
    font-size: 36px;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin: 0;
    background: linear-gradient(135deg, #fff 0%, #7df9ff 50%, #a060ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 20px rgba(49,216,255,0.5));
}
.ase-subtitle {
    color: #5a8aaa;
    font-size: 12px;
    margin-top: 3px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Glassmorphism Panel ──────────────────────────────────────────────────── */
.ase-panel {
    background: rgba(8,16,30,0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(107,145,179,0.28);
    border-radius: 14px;
    box-shadow:
        0 4px 32px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.06);
    padding: 16px;
}
.ase-panel:hover {
    border-color: rgba(107,145,179,0.45);
    transition: border-color 0.3s ease;
}
.ase-credit {
    background: linear-gradient(135deg, rgba(10,30,50,0.92), rgba(5,18,32,0.88));
    border-color: rgba(46,232,137,0.5);
    box-shadow: 0 0 24px rgba(46,232,137,0.12), 0 4px 32px rgba(0,0,0,0.5);
}
.ase-panel-title {
    color: #31d8ff;
    font-weight: 800;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── Layout Grid ──────────────────────────────────────────────────────────── */
.ase-grid-layout {
    display: grid;
    grid-template-columns: minmax(260px,320px) minmax(480px,760px) minmax(260px,320px);
    gap: 14px;
    align-items: start;
}

/* ── Stat Cards ───────────────────────────────────────────────────────────── */
.ase-stat-grid {
    display: grid;
    grid-template-columns: repeat(6, minmax(110px,1fr));
    gap: 10px;
    margin: 14px 0;
}
.ase-stat {
    background: rgba(10,22,38,0.85);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(66,101,135,0.45);
    border-radius: 12px;
    padding: 12px 14px;
    transition: transform 0.15s, box-shadow 0.15s;
}
.ase-stat:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}
.ase-stat-label {
    color: #6a8fa8;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.ase-stat-value {
    color: #f4fbff;
    font-size: 21px;
    font-weight: 800;
    margin-top: 4px;
}

/* ── Mission Message Banner ───────────────────────────────────────────────── */
.ase-mission-banner {
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 14px;
    font-weight: 600;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 10px;
    backdrop-filter: blur(8px);
    border: 1px solid;
    animation: bannerSlide 0.35s ease;
}
@keyframes bannerSlide {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Danger Ring ──────────────────────────────────────────────────────────── */
.danger-ring-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    padding: 8px 0;
}
.danger-ring {
    position: relative;
    width: 80px;
    height: 80px;
}
.danger-ring svg {
    width: 100%;
    height: 100%;
    transform: rotate(-90deg);
}
.danger-ring-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    text-align: center;
}
.danger-ring-value {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 18px;
    font-weight: 900;
}

/* ── Lives Hearts ─────────────────────────────────────────────────────────── */
.ase-lives {
    display: flex;
    gap: 4px;
    justify-content: center;
    font-size: 20px;
    margin: 4px 0;
}

/* ── Cloak Badge ──────────────────────────────────────────────────────────── */
.cloak-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    border-radius: 999px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.cloak-active-badge {
    background: rgba(160,96,255,0.25);
    border: 1px solid rgba(160,96,255,0.7);
    color: #c89fff;
    animation: cloakPulse 1s ease-in-out infinite;
}
.cloak-ready-badge {
    background: rgba(46,232,137,0.15);
    border: 1px solid rgba(46,232,137,0.5);
    color: #2ee889;
}
.cloak-none-badge {
    background: rgba(100,100,100,0.1);
    border: 1px solid rgba(100,100,100,0.3);
    color: #666;
}
@keyframes cloakPulse {
    0%,100% { box-shadow: 0 0 8px rgba(160,96,255,0.4); }
    50%      { box-shadow: 0 0 20px rgba(160,96,255,0.9); }
}

/* ── Game Board ───────────────────────────────────────────────────────────── */
.ase-board-wrap {
    background: linear-gradient(180deg, rgba(8,20,38,0.95), rgba(3,8,16,0.97));
    border: 1px solid rgba(49,216,255,0.45);
    border-radius: 14px;
    padding: 14px;
    box-shadow:
        inset 0 0 50px rgba(49,216,255,0.06),
        0 0 50px rgba(0,0,0,0.5);
}
.ase-board-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #31d8ff;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.ase-board-title span:last-child { color: #6a8fa8; font-weight: 600; }
.ase-board {
    display: grid;
    gap: 4px;
    width: 100%;
}
.ase-cell {
    position: relative;
    aspect-ratio: 1;
    min-width: 0;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(9px, 1.3vw, 15px);
    font-weight: 800;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.05);
    transition: transform 0.1s, filter 0.2s;
}

/* ── Cell Types ───────────────────────────────────────────────────────────── */
.floor-a { background: radial-gradient(circle at 40% 35%, #14213a, #0b1525); }
.floor-b { background: radial-gradient(circle at 60% 60%, #101c33, #090f1e); }
.wall {
    background: linear-gradient(145deg, #1c2535, #2d3d52);
    border-color: #3d5066;
    box-shadow: inset 0 -2px 0 rgba(0,0,0,0.5), inset 0 2px 0 rgba(255,255,255,0.05);
}
.gate-open {
    background: linear-gradient(135deg, #0b4660, #12718a);
    border-color: #40d4f0;
    box-shadow: 0 0 10px rgba(49,216,255,0.3);
}
.gate-closed {
    background: repeating-linear-gradient(135deg, #3a1250 0px, #3a1250 5px, #5e2080 5px, #5e2080 10px);
    border-color: #cc66ff;
    box-shadow: 0 0 10px rgba(180,80,255,0.35);
}
.exit {
    background: radial-gradient(circle, #1fbe70, #0a4d30);
    border-color: #2ee889;
    box-shadow: 0 0 20px rgba(46,232,137,0.7);
    animation: exitPulse 1.4s ease-in-out infinite;
}
.player {
    background: radial-gradient(circle, #6af2ff, #0a6ea8);
    border-color: #31d8ff;
    box-shadow: 0 0 22px rgba(49,216,255,1);
    animation: playerGlow 2s ease-in-out infinite;
    z-index: 10;
}
.player-cloaked {
    background: radial-gradient(circle, #c89fff, #4a108a);
    border-color: #a060ff;
    box-shadow: 0 0 22px rgba(160,96,255,0.9);
    animation: cloakShimmer 1.2s ease-in-out infinite;
}
.hunter {
    background: radial-gradient(circle, #ff6a82, #6b1828);
    border-color: #ff3d5c;
    box-shadow: 0 0 22px rgba(255,60,90,0.9);
    animation: enemyPulse 1.5s ease-in-out infinite;
}
.hunter-frozen {
    background: radial-gradient(circle, #a0c8e8, #2a4a68);
    border-color: #7ab8dc;
    box-shadow: 0 0 12px rgba(122,184,220,0.5);
    filter: grayscale(0.4);
    animation: none;
}
.interceptor {
    background: radial-gradient(circle, #ffb050, #7a3e10);
    border-color: #ff9020;
    box-shadow: 0 0 22px rgba(255,144,32,0.9);
    animation: enemyPulse 1.8s ease-in-out infinite;
}
.interceptor-frozen {
    background: radial-gradient(circle, #b8d8e8, #3a5a70);
    border-color: #88b8d0;
    filter: grayscale(0.4);
    animation: none;
}
.flanker {
    background: radial-gradient(circle, #d078ff, #5a0090);
    border-color: #b040ef;
    box-shadow: 0 0 22px rgba(176,64,239,0.9);
    animation: enemyPulse 2s ease-in-out infinite;
}
.flanker-frozen {
    background: radial-gradient(circle, #c8b0e0, #3a2060);
    border-color: #9088b0;
    filter: grayscale(0.4);
    animation: none;
}
.power-up {
    background: radial-gradient(circle, #fff080, #a06010);
    border-color: #ffe040;
    box-shadow: 0 0 18px rgba(255,224,64,0.8);
    animation: powerUpBounce 1s ease-in-out infinite;
}

/* ── Path Markers ─────────────────────────────────────────────────────────── */
.path-hunter::after,
.path-interceptor::before,
.path-flanker::after {
    content: "";
    position: absolute;
    width: 28%;
    height: 28%;
    border-radius: 50%;
    opacity: 0.85;
}
.path-hunter::after    { background: #31d8ff; box-shadow: 0 0 8px #31d8ff; top: 4px; right: 4px; }
.path-interceptor::before { background: #ff9020; box-shadow: 0 0 8px #ff9020; bottom: 4px; left: 4px; }
.path-flanker::after   { background: #d060ff; box-shadow: 0 0 8px #d060ff; bottom: 4px; right: 4px; }

/* ── Cell Label ───────────────────────────────────────────────────────────── */
.ase-cell-label {
    position: relative;
    z-index: 2;
    line-height: 1;
    user-select: none;
}

/* ── Legend ───────────────────────────────────────────────────────────────── */
.ase-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 10px;
}
.ase-pill {
    border: 1px solid rgba(120,157,190,0.35);
    border-radius: 999px;
    padding: 3px 9px;
    font-size: 11px;
    background: rgba(12,24,40,0.7);
    color: #8ab0cc;
}

/* ── Movement Keypad ──────────────────────────────────────────────────────── */
.ase-kpad {
    display: grid;
    grid-template-columns: repeat(3, 52px);
    gap: 6px;
    justify-content: center;
    margin-top: 6px;
}

/* ── Readout Rows ─────────────────────────────────────────────────────────── */
.ase-readout { display: grid; gap: 6px; font-size: 12px; }
.ase-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding-bottom: 5px;
}
.ase-muted  { color: #6a8fa8; }
.ase-good   { color: #2ee889; }
.ase-warn   { color: #ffcf48; }
.ase-danger { color: #ff4060; }
.ase-purple { color: #c08fff; }

/* ── Code Block ───────────────────────────────────────────────────────────── */
.ase-code {
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(49,216,255,0.2);
    border-radius: 8px;
    padding: 10px 12px;
    font-family: Consolas, "Fira Code", monospace;
    color: #c0f0ff;
    font-size: 12px;
    line-height: 1.6;
}

/* ── Win / Loss Overlay ───────────────────────────────────────────────────── */
.ase-overlay {
    position: fixed;
    inset: 0;
    background: rgba(2,5,12,0.88);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    animation: overlayIn 0.4s ease;
}
@keyframes overlayIn {
    from { opacity: 0; backdrop-filter: blur(0); }
    to   { opacity: 1; backdrop-filter: blur(16px); }
}
.ase-overlay-card {
    background: rgba(8,18,34,0.96);
    border: 2px solid;
    border-radius: 20px;
    padding: 36px 44px;
    min-width: 380px;
    max-width: 480px;
    text-align: center;
    box-shadow: 0 0 80px rgba(0,0,0,0.8);
    animation: overlayCardIn 0.45s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes overlayCardIn {
    from { transform: scale(0.7) translateY(40px); opacity: 0; }
    to   { transform: scale(1) translateY(0);      opacity: 1; }
}
.ase-overlay-title {
    font-size: 32px;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
}
.ase-overlay-sub {
    font-size: 14px;
    color: #8ab0cc;
    margin-bottom: 24px;
}
.ase-score-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 20px 0;
    text-align: left;
}
.ase-score-item {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px 12px;
}
.ase-score-item-label { color: #6a8fa8; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
.ase-score-item-value { font-size: 18px; font-weight: 800; margin-top: 3px; }

/* ── Scan Panel ───────────────────────────────────────────────────────────── */
.ase-scan-agent {
    background: rgba(0,0,0,0.2);
    border: 1px solid rgba(49,216,255,0.2);
    border-radius: 10px;
    padding: 10px 12px;
    margin-top: 8px;
}

/* ── Lab Panel ────────────────────────────────────────────────────────────── */
.ase-lab-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 12px;
}
.ase-agent-col {
    background: rgba(0,0,0,0.25);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px 12px;
}
.ase-delta-up   { color: #2ee889; font-size: 10px; }
.ase-delta-down { color: #ff4060; font-size: 10px; }

/* ── Animations ───────────────────────────────────────────────────────────── */
@keyframes exitPulse {
    0%,100% { box-shadow: 0 0 14px rgba(46,232,137,0.6); }
    50%      { box-shadow: 0 0 32px rgba(46,232,137,1); }
}
@keyframes playerGlow {
    0%,100% { box-shadow: 0 0 18px rgba(49,216,255,0.8); }
    50%      { box-shadow: 0 0 36px rgba(49,216,255,1), 0 0 60px rgba(49,216,255,0.4); }
}
@keyframes cloakShimmer {
    0%  { box-shadow: 0 0 18px rgba(160,96,255,0.8); filter: hue-rotate(0deg); }
    50% { box-shadow: 0 0 40px rgba(160,96,255,1), 0 0 70px rgba(160,96,255,0.5); filter: hue-rotate(30deg); }
    100%{ box-shadow: 0 0 18px rgba(160,96,255,0.8); filter: hue-rotate(0deg); }
}
@keyframes enemyPulse {
    0%,100% { filter: brightness(1); }
    50%      { filter: brightness(1.3); }
}
@keyframes powerUpBounce {
    0%,100% { transform: scale(1); box-shadow: 0 0 14px rgba(255,224,64,0.7); }
    50%      { transform: scale(1.15); box-shadow: 0 0 28px rgba(255,224,64,1); }
}

/* ── Responsive ───────────────────────────────────────────────────────────── */
@media (max-width: 1200px) {
    .ase-grid-layout { grid-template-columns: 1fr; }
    .ase-stat-grid   { grid-template-columns: repeat(3, 1fr); }
    .ase-lab-grid    { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 700px) {
    .ase-stat-grid { grid-template-columns: repeat(2, 1fr); }
    .ase-overlay-card { padding: 24px 20px; min-width: unset; margin: 16px; }
}
</style>
"""

button_css = {
    "minHeight": "38px",
    "borderRadius": "10px",
    "fontWeight": "700",
    "fontSize": "12px",
    "letterSpacing": "0.3px",
}

wide_button_css = {
    "width": "100%",
    "minHeight": "38px",
    "borderRadius": "10px",
    "fontWeight": "700",
    "fontSize": "12px",
}

kpad_button_css = {
    "width": "52px",
    "height": "46px",
    "borderRadius": "10px",
    "fontWeight": "800",
    "fontSize": "16px",
    "padding": "0",
    "minWidth": "0",
}
