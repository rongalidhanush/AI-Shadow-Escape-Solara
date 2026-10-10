"""Shared visual styles for the Solara interface."""

PAGE_CSS = """
<style>
body {
    background: #050912 !important;
}
.ase-root {
    min-height: 100vh;
    color: #e8f4ff;
    background:
        linear-gradient(rgba(49, 216, 255, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(49, 216, 255, 0.035) 1px, transparent 1px),
        radial-gradient(circle at top left, rgba(0, 217, 255, 0.14), transparent 28rem),
        radial-gradient(circle at bottom right, rgba(255, 72, 118, 0.12), transparent 24rem),
        linear-gradient(135deg, #050912 0%, #0b1320 45%, #101827 100%);
    background-size: 32px 32px, 32px 32px, auto, auto, auto;
    font-family: "Segoe UI", Arial, sans-serif;
    padding: 22px;
}
.ase-shell {
    max-width: 1480px;
    margin: 0 auto;
}
.ase-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 0;
    margin: 0;
    color: #f6fbff;
    text-shadow: 0 0 18px rgba(49, 216, 255, 0.38);
}
.ase-subtitle {
    color: #83a6c8;
    font-size: 13px;
    margin-top: 4px;
}
.ase-grid-layout {
    display: grid;
    grid-template-columns: minmax(280px, 1fr) minmax(520px, 780px) minmax(280px, 1fr);
    gap: 16px;
    align-items: start;
}
.ase-panel {
    background: rgba(10, 19, 32, 0.88);
    border: 1px solid rgba(107, 145, 179, 0.35);
    border-radius: 8px;
    box-shadow: 0 0 24px rgba(0, 0, 0, 0.28);
    padding: 14px;
}
.ase-credit {
    background: linear-gradient(135deg, rgba(18, 35, 55, 0.96), rgba(8, 18, 32, 0.94));
    border: 1px solid rgba(46, 232, 137, 0.45);
}
.ase-panel-title {
    color: #31d8ff;
    font-weight: 750;
    font-size: 14px;
    margin-bottom: 10px;
}
.ase-stat-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(120px, 1fr));
    gap: 10px;
    margin: 16px 0;
}
.ase-stat {
    background: rgba(18, 31, 50, 0.92);
    border: 1px solid rgba(66, 101, 135, 0.55);
    border-radius: 8px;
    padding: 12px;
}
.ase-stat-label {
    color: #8ca7c1;
    font-size: 11px;
    text-transform: uppercase;
}
.ase-stat-value {
    color: #f4fbff;
    font-size: 22px;
    font-weight: 780;
    margin-top: 5px;
}
.ase-board-wrap {
    background:
        linear-gradient(180deg, rgba(13, 28, 45, 0.92), rgba(4, 10, 18, 0.94));
    border: 1px solid rgba(49, 216, 255, 0.48);
    border-radius: 8px;
    padding: 12px;
    box-shadow: inset 0 0 34px rgba(49, 216, 255, 0.08), 0 0 36px rgba(0, 0, 0, 0.36);
}
.ase-board-title {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: center;
    color: #31d8ff;
    font-size: 12px;
    font-weight: 800;
    margin: 2px 2px 10px;
    text-transform: uppercase;
}
.ase-board-title span:last-child {
    color: #8fb1cf;
    font-weight: 650;
}
.ase-board {
    display: grid;
    grid-template-columns: repeat(16, minmax(24px, 1fr));
    gap: 5px;
    width: 100%;
    aspect-ratio: 16 / 13;
}
.ase-cell {
    position: relative;
    min-width: 0;
    min-height: 0;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(10px, 1.4vw, 15px);
    font-weight: 800;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.06);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
}
.floor-a { background: radial-gradient(circle at 50% 35%, #1a2c42, #101b2b); }
.floor-b { background: radial-gradient(circle at 50% 35%, #142338, #0d1726); }
.wall {
    background: linear-gradient(135deg, #202938, #556273);
    border-color: #8191a4;
    box-shadow: inset 0 0 12px rgba(0, 0, 0, 0.45);
}
.gate-open {
    background: linear-gradient(135deg, #0e4f63, #16819a);
    border-color: #58e2ff;
    color: #dffbff;
}
.gate-closed {
    background: repeating-linear-gradient(135deg, #4b1d62, #4b1d62 5px, #742995 5px, #742995 10px);
    border-color: #de7dff;
    color: #fff1ff;
}
.exit {
    background: radial-gradient(circle, #24d17a, #0d593d);
    border-color: #2ee889;
    color: #062414;
    animation: exitPulse 1.6s ease-in-out infinite;
}
.player {
    background: radial-gradient(circle, #5fe7ff, #075e8d);
    border-color: #34c8ff;
    color: #00111a;
    box-shadow: 0 0 20px rgba(52, 200, 255, 0.95);
}
.hunter {
    background: radial-gradient(circle, #ff6f86, #761b2b);
    border-color: #ff4a6e;
    color: #250009;
    box-shadow: 0 0 20px rgba(255, 74, 110, 0.86);
}
.interceptor {
    background: radial-gradient(circle, #ffb465, #7a4216);
    border-color: #ff9a3d;
    color: #291100;
    box-shadow: 0 0 20px rgba(255, 154, 61, 0.82);
}
.path-hunter::after,
.path-interceptor::before {
    content: "";
    position: absolute;
    width: 34%;
    height: 34%;
    border-radius: 50%;
    opacity: 0.9;
}
.path-hunter::after { background: #31d8ff; box-shadow: 0 0 10px #31d8ff; }
.path-interceptor::before { background: #ff9a3d; box-shadow: 0 0 10px #ff9a3d; transform: translate(28%, 28%); }
.ase-cell-label {
    position: relative;
    z-index: 2;
    text-shadow: 0 1px 4px rgba(255, 255, 255, 0.55);
}
.ase-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    color: #9eb9d2;
    font-size: 12px;
    margin-top: 10px;
}
.ase-pill {
    border: 1px solid rgba(120, 157, 190, 0.4);
    border-radius: 999px;
    padding: 5px 8px;
    background: rgba(17, 31, 50, 0.8);
}
.ase-kpad {
    display: grid;
    grid-template-columns: repeat(3, 64px);
    gap: 8px;
    justify-content: center;
    margin-top: 8px;
}
.ase-readout {
    display: grid;
    gap: 7px;
    font-size: 13px;
}
.ase-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    border-bottom: 1px solid rgba(110, 144, 176, 0.16);
    padding-bottom: 6px;
}
.ase-muted { color: #91abc4; }
.ase-good { color: #2ee889; }
.ase-warn { color: #ffcf48; }
.ase-danger { color: #ff4d5f; }
.ase-code {
    background: rgba(0, 0, 0, 0.24);
    border: 1px solid rgba(49, 216, 255, 0.2);
    border-radius: 6px;
    padding: 10px;
    font-family: Consolas, monospace;
    color: #d7f9ff;
}
@media (max-width: 1100px) {
    .ase-grid-layout { grid-template-columns: 1fr; }
    .ase-stat-grid { grid-template-columns: repeat(2, minmax(120px, 1fr)); }
}
@keyframes exitPulse {
    0%, 100% { box-shadow: 0 0 12px rgba(46, 232, 137, 0.55); }
    50% { box-shadow: 0 0 26px rgba(46, 232, 137, 0.95); }
}
</style>
"""


button_css = {
    "minHeight": "42px",
    "borderRadius": "8px",
    "fontWeight": "700",
    "letterSpacing": "0",
}

wide_button_css = {
    "width": "100%",
    "minHeight": "42px",
    "borderRadius": "8px",
    "fontWeight": "700",
}
