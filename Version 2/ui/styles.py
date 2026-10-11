"""Shared visual styles — Comprehensive Dark & Light Themes with Cyber Tactical UI."""

PAGE_CSS = """
<style>
/* ── Reset & Base ─────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

/* ── Overrides for Vuetify / Solara defaults ──────────────────────────────── */
.v-application, .v-application--wrap {
    background: transparent !important;
    color: var(--text-primary) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", Roboto, sans-serif !important;
}
.v-application .v-input, .v-application .v-label {
    color: var(--text-muted) !important;
}
.v-application .v-input--switch .v-label {
    color: var(--text-primary) !important;
    font-weight: 700;
    font-size: 12px;
}
.v-select .v-select__selection {
    color: var(--text-primary) !important;
    font-weight: 600;
}
.solara-markdown, .solara-markdown p, .solara-markdown li {
    color: var(--text-primary) !important;
}

/* ── CSS Variables — Dark Theme (default) ─────────────────────────────────── */
:root, [data-theme="dark"], .ase-theme-dark {
    --bg-body:          #030712;
    --bg-root:          #030712;
    --bg-panel:         rgba(8, 17, 34, 0.82);
    --bg-panel-h:       rgba(12, 24, 48, 0.92);
    --bg-card:          rgba(10, 22, 42, 0.85);
    --bg-cell-a:        #101e36;
    --bg-cell-b:        #0a1426;
    --bg-code:          rgba(0, 0, 0, 0.45);
    --bg-scan:          rgba(0, 0, 0, 0.28);
    --bg-pill:          rgba(14, 28, 52, 0.75);
    --bg-overlay:       rgba(2, 6, 16, 0.92);
    --bg-overlay-card:  rgba(8, 18, 38, 0.98);
    --border-panel:     rgba(49, 216, 255, 0.22);
    --border-card:      rgba(49, 216, 255, 0.18);
    --border-pill:      rgba(49, 216, 255, 0.28);
    --border-row:       rgba(255, 255, 255, 0.07);
    --border-code:      rgba(49, 216, 255, 0.25);
    --text-primary:     #e4f2ff;
    --text-muted:       #749bb8;
    --text-label:       #749bb8;
    --text-value:       #f4fbff;
    --text-code:        #80e5ff;
    --text-panel-title: #31d8ff;
    --text-sub:         #6898bd;
    --grid-line:        rgba(49, 216, 255, 0.04);
    --accent-cyan:      #00f0ff;
    --accent-green:     #10f589;
    --accent-red:       #ff3b5c;
    --accent-warn:      #ffb834;
    --accent-purple:    #bf5af2;
    --shadow-panel:     0 8px 32px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    --shadow-board:     0 0 50px rgba(0, 0, 0, 0.6);
    --glow-board:       inset 0 0 50px rgba(49, 216, 255, 0.08);
    --bg-radial-1:      rgba(0, 240, 255, 0.14);
    --bg-radial-2:      rgba(255, 59, 92, 0.12);
    --bg-radial-3:      rgba(191, 90, 242, 0.08);
    --bg-grad-from:     #030712;
    --bg-grad-mid:      #080f20;
    --bg-grad-to:       #0d172e;
    --ai-box-bg:        rgba(6, 17, 34, 0.95);
    --ai-box-border:    rgba(49, 216, 255, 0.35);
    --ai-box-text:      #e2f3ff;
    --ai-box-muted:     #8bb6d8;
    --ai-title-text:    #00f0ff;
    --ai-card-bg:       rgba(10, 25, 48, 0.7);
    --ai-card-border:   rgba(49, 216, 255, 0.2);
    --theme-btn-bg:     rgba(255, 255, 255, 0.08);
    --theme-btn-border: rgba(49, 216, 255, 0.4);
    --theme-btn-color:  #e4f2ff;
    --theme-btn-hover:  rgba(49, 216, 255, 0.2);
    --wall-from:        #182336;
    --wall-to:          #27374e;
    --wall-border:      #3b4f6b;
}

/* ── CSS Variables — Light Theme ─────────────────────────────────────────── */
[data-theme="light"], .ase-theme-light {
    --bg-body:          #eef3fa;
    --bg-root:          #eef3fa;
    --bg-panel:         rgba(255, 255, 255, 0.94);
    --bg-panel-h:       rgba(242, 247, 255, 0.98);
    --bg-card:          rgba(240, 246, 255, 0.95);
    --bg-cell-a:        #d4e4f7;
    --bg-cell-b:        #c6dbf2;
    --bg-code:          rgba(10, 30, 70, 0.06);
    --bg-scan:          rgba(10, 30, 70, 0.05);
    --bg-pill:          rgba(220, 234, 252, 0.9);
    --bg-overlay:       rgba(215, 228, 245, 0.94);
    --bg-overlay-card:  rgba(255, 255, 255, 0.99);
    --border-panel:     rgba(14, 116, 214, 0.22);
    --border-card:      rgba(14, 116, 214, 0.2);
    --border-pill:      rgba(14, 116, 214, 0.25);
    --border-row:       rgba(10, 30, 70, 0.08);
    --border-code:      rgba(14, 116, 214, 0.25);
    --text-primary:     #0b1e36;
    --text-muted:       #486581;
    --text-label:       #486581;
    --text-value:       #061528;
    --text-code:        #084887;
    --text-panel-title: #0969da;
    --text-sub:         #335272;
    --grid-line:        rgba(14, 116, 214, 0.06);
    --accent-cyan:      #0969da;
    --accent-green:     #089858;
    --accent-red:       #d81d45;
    --accent-warn:      #ca6d00;
    --accent-purple:    #8232c9;
    --shadow-panel:     0 8px 24px rgba(10, 35, 70, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.8);
    --shadow-board:     0 6px 30px rgba(10, 35, 70, 0.12);
    --glow-board:       inset 0 0 35px rgba(14, 116, 214, 0.05);
    --bg-radial-1:      rgba(9, 105, 218, 0.08);
    --bg-radial-2:      rgba(216, 29, 69, 0.06);
    --bg-radial-3:      rgba(130, 50, 201, 0.05);
    --bg-grad-from:     #e4ecf8;
    --bg-grad-mid:      #edf2fa;
    --bg-grad-to:       #f5f8fd;
    --ai-box-bg:        rgba(255, 255, 255, 0.98);
    --ai-box-border:    rgba(14, 116, 214, 0.35);
    --ai-box-text:      #0d213a;
    --ai-box-muted:     #486581;
    --ai-title-text:    #0969da;
    --ai-card-bg:       rgba(240, 246, 255, 0.9);
    --ai-card-border:   rgba(14, 116, 214, 0.2);
    --theme-btn-bg:     rgba(10, 30, 70, 0.08);
    --theme-btn-border: rgba(14, 116, 214, 0.35);
    --theme-btn-color:  #0b1e36;
    --theme-btn-hover:  rgba(14, 116, 214, 0.15);
    --wall-from:        #334155;
    --wall-to:          #1e293b;
    --wall-border:      #475569;
}

body {
    background: var(--bg-body) !important;
    margin: 0;
    transition: background 0.35s ease, color 0.3s ease;
}

/* ── Root Container ───────────────────────────────────────────────────────── */
.ase-root {
    min-height: 100vh;
    color: var(--text-primary);
    background:
        linear-gradient(var(--grid-line) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-line) 1px, transparent 1px),
        radial-gradient(ellipse at 15% 10%, var(--bg-radial-1) 0%, transparent 45%),
        radial-gradient(ellipse at 85% 90%, var(--bg-radial-2) 0%, transparent 40%),
        radial-gradient(ellipse at 50% 50%, var(--bg-radial-3) 0%, transparent 60%),
        linear-gradient(160deg, var(--bg-grad-from) 0%, var(--bg-grad-mid) 50%, var(--bg-grad-to) 100%);
    background-size: 28px 28px, 28px 28px, auto, auto, auto, auto;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", Roboto, sans-serif;
    padding: 16px 20px 40px 20px;
    transition: background 0.35s ease, color 0.3s ease;
    position: relative;
}

/* ── Shell ────────────────────────────────────────────────────────────────── */
.ase-shell { max-width: 1560px; margin: 0 auto; }

/* ── Floating & Header Theme Toggle Buttons ───────────────────────────────── */
.ase-theme-toggle-floating {
    position: fixed;
    top: 16px;
    right: 20px;
    z-index: 1000;
}
.ase-theme-btn {
    background: var(--theme-btn-bg) !important;
    border: 1px solid var(--theme-btn-border) !important;
    border-radius: 999px !important;
    color: var(--theme-btn-color) !important;
    padding: 8px 18px !important;
    font-size: 13px !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
}
.ase-theme-btn:hover {
    transform: translateY(-2px);
    background: var(--theme-btn-hover) !important;
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.28) !important;
}
.ase-header-theme-btn {
    background: var(--theme-btn-bg) !important;
    border: 1px solid var(--theme-btn-border) !important;
    color: var(--theme-btn-color) !important;
    transition: all 0.2s ease !important;
}
.ase-header-theme-btn:hover {
    border-color: var(--accent-cyan) !important;
    transform: translateY(-1px);
}

/* ── Typography ───────────────────────────────────────────────────────────── */
.ase-title {
    font-size: 34px;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1.15;
    background: linear-gradient(135deg, var(--text-primary) 0%, #7df9ff 45%, #c08fff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 16px rgba(49, 216, 255, 0.45));
}
.ase-theme-light .ase-title, [data-theme="light"] .ase-title {
    background: linear-gradient(135deg, #094098 0%, #0969da 50%, #8232c9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 2px 10px rgba(9, 105, 218, 0.25));
}
.ase-subtitle {
    color: var(--text-sub);
    font-size: 12px;
    font-weight: 600;
    margin-top: 4px;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}

/* ── Glassmorphism Panel ──────────────────────────────────────────────────── */
.ase-panel {
    background: var(--bg-panel);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--border-panel);
    border-radius: 14px;
    box-shadow: var(--shadow-panel);
    padding: 16px;
    transition: border-color 0.25s ease, background 0.3s ease, box-shadow 0.25s ease;
}
.ase-panel:hover {
    border-color: rgba(49, 216, 255, 0.4);
}
.ase-theme-light .ase-panel:hover, [data-theme="light"] .ase-panel:hover {
    border-color: rgba(14, 116, 214, 0.4);
}

.ase-credit {
    background: linear-gradient(135deg, var(--bg-panel-h), var(--bg-panel));
    border-color: rgba(16, 245, 137, 0.45);
    box-shadow: 0 0 24px rgba(16, 245, 137, 0.1), var(--shadow-panel);
}
.ase-theme-light .ase-credit, [data-theme="light"] .ase-credit {
    border-color: rgba(8, 152, 88, 0.4);
    box-shadow: 0 0 20px rgba(8, 152, 88, 0.08), var(--shadow-panel);
}

.ase-panel-title {
    color: var(--text-panel-title);
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
    grid-template-columns: minmax(270px, 320px) minmax(500px, 780px) minmax(270px, 320px);
    gap: 16px;
    align-items: start;
}

/* ── Stat Cards ───────────────────────────────────────────────────────────── */
.ase-stat-grid {
    display: grid;
    grid-template-columns: repeat(6, minmax(110px, 1fr));
    gap: 10px;
    margin: 14px 0;
}
.ase-stat {
    background: var(--bg-card);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-card);
    border-radius: 12px;
    padding: 12px 14px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, border-color 0.2s ease;
}
.ase-stat::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-cyan), transparent);
    opacity: 0.6;
}
.ase-stat:hover {
    transform: translateY(-2px);
    border-color: var(--accent-cyan);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}
.ase-stat-label {
    color: var(--text-label);
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.ase-stat-value {
    color: var(--text-value);
    font-size: 20px;
    font-weight: 900;
    margin-top: 4px;
    font-feature-settings: "tnum";
}

/* ── Mission Message Banner ───────────────────────────────────────────────── */
.ase-mission-banner {
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 14px;
    font-weight: 700;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 12px;
    backdrop-filter: blur(10px);
    border: 1px solid;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    transition: border-color 0.25s ease, background 0.25s ease;
}

/* ── Danger Ring ──────────────────────────────────────────────────────────── */
.danger-ring-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    padding: 6px 0;
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
    font-weight: 800;
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
    gap: 5px;
    justify-content: center;
    font-size: 18px;
    margin: 2px 0;
}

/* ── Cloak Badge ──────────────────────────────────────────────────────────── */
.cloak-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
    transition: all 0.25s ease;
}
.cloak-active-badge {
    background: rgba(191, 90, 242, 0.22);
    border: 1px solid rgba(191, 90, 242, 0.8);
    color: #e5b3ff;
    animation: cloakPulse 1.2s ease-in-out infinite;
}
.cloak-ready-badge {
    background: rgba(16, 245, 137, 0.18);
    border: 1px solid rgba(16, 245, 137, 0.6);
    color: #10f589;
}
.ase-theme-light .cloak-ready-badge, [data-theme="light"] .cloak-ready-badge {
    color: #089858;
}
.cloak-none-badge {
    background: rgba(120, 140, 160, 0.1);
    border: 1px solid rgba(120, 140, 160, 0.25);
    color: var(--text-muted);
}
@keyframes cloakPulse {
    0%, 100% { box-shadow: 0 0 8px rgba(191, 90, 242, 0.4); }
    50%      { box-shadow: 0 0 22px rgba(191, 90, 242, 0.9); }
}

/* ── Game Board ───────────────────────────────────────────────────────────── */
.ase-board-wrap {
    background: linear-gradient(180deg, rgba(8, 20, 38, 0.95), rgba(3, 8, 16, 0.98));
    border: 1px solid rgba(49, 216, 255, 0.45);
    border-radius: 16px;
    padding: 16px;
    box-shadow: var(--glow-board), var(--shadow-board);
    transition: background 0.35s ease, border-color 0.3s ease;
    position: relative;
}
.ase-theme-light .ase-board-wrap, [data-theme="light"] .ase-board-wrap {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(240, 246, 255, 0.98));
    border-color: rgba(14, 116, 214, 0.4);
}
.ase-board-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--text-panel-title);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.ase-board-title span:last-child {
    color: var(--text-muted);
    font-weight: 700;
    letter-spacing: 0.5px;
}
.ase-board {
    display: grid;
    gap: 4px;
    width: 100%;
}
.ase-cell {
    position: relative;
    aspect-ratio: 1;
    min-width: 0;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(10px, 1.4vw, 16px);
    font-weight: 800;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: transform 0.12s ease, filter 0.2s ease, box-shadow 0.2s ease;
}

/* ── Cell Types ───────────────────────────────────────────────────────────── */
.floor-a { background: radial-gradient(circle at 40% 35%, var(--bg-cell-a), #0a1426); }
.floor-b { background: radial-gradient(circle at 60% 60%, var(--bg-cell-b), #070e1c); }
.ase-theme-light .floor-a, [data-theme="light"] .floor-a {
    background: radial-gradient(circle at 40% 35%, #d8e6f8, #c8dbf2);
    border-color: rgba(14, 116, 214, 0.08);
}
.ase-theme-light .floor-b, [data-theme="light"] .floor-b {
    background: radial-gradient(circle at 60% 60%, #cedef4, #bdd3ee);
    border-color: rgba(14, 116, 214, 0.08);
}

.wall {
    background: linear-gradient(145deg, var(--wall-from), var(--wall-to));
    border-color: var(--wall-border);
    box-shadow: inset 0 -2px 0 rgba(0, 0, 0, 0.5), inset 0 2px 0 rgba(255, 255, 255, 0.08);
}
.ase-theme-light .wall, [data-theme="light"] .wall {
    background: linear-gradient(145deg, #334155, #1e293b);
    border-color: #475569;
    box-shadow: inset 0 -2px 0 rgba(0, 0, 0, 0.3), inset 0 2px 0 rgba(255, 255, 255, 0.2);
}

.gate-open {
    background: linear-gradient(135deg, #0b4660, #12718a);
    border-color: #40d4f0;
    box-shadow: 0 0 12px rgba(49, 216, 255, 0.35);
}
.gate-closed {
    background: repeating-linear-gradient(135deg, #3a1250 0px, #3a1250 5px, #5e2080 5px, #5e2080 10px);
    border-color: #cc66ff;
    box-shadow: 0 0 12px rgba(180, 80, 255, 0.4);
}
.exit {
    background: radial-gradient(circle, #10f589, #086638);
    border-color: #10f589;
    box-shadow: 0 0 22px rgba(16, 245, 137, 0.8);
    animation: exitPulse 1.4s ease-in-out infinite;
    z-index: 5;
}
.player {
    background: radial-gradient(circle, #6af2ff, #0a6ea8);
    border-color: #31d8ff;
    box-shadow: 0 0 24px rgba(49, 216, 255, 1);
    animation: playerGlow 2s ease-in-out infinite;
    z-index: 10;
}
.player-cloaked {
    background: radial-gradient(circle, #e5b3ff, #6b18a8);
    border-color: #bf5af2;
    box-shadow: 0 0 24px rgba(191, 90, 242, 0.95);
    animation: cloakShimmer 1.2s ease-in-out infinite;
    z-index: 10;
}
.hunter {
    background: radial-gradient(circle, #ff6a82, #7a1527);
    border-color: #ff3b5c;
    box-shadow: 0 0 22px rgba(255, 59, 92, 0.9);
    animation: enemyPulse 1.5s ease-in-out infinite;
    z-index: 8;
}
.hunter-frozen {
    background: radial-gradient(circle, #a0c8e8, #2a4a68);
    border-color: #7ab8dc;
    box-shadow: 0 0 12px rgba(122, 184, 220, 0.5);
    filter: grayscale(0.5);
    animation: none;
    z-index: 8;
}
.interceptor {
    background: radial-gradient(circle, #ffb850, #8a420a);
    border-color: #ff9020;
    box-shadow: 0 0 22px rgba(255, 144, 32, 0.9);
    animation: enemyPulse 1.8s ease-in-out infinite;
    z-index: 8;
}
.interceptor-frozen {
    background: radial-gradient(circle, #b8d8e8, #3a5a70);
    border-color: #88b8d0;
    filter: grayscale(0.5);
    animation: none;
    z-index: 8;
}
.flanker {
    background: radial-gradient(circle, #d078ff, #5c0896);
    border-color: #b040ef;
    box-shadow: 0 0 22px rgba(176, 64, 239, 0.9);
    animation: enemyPulse 2s ease-in-out infinite;
    z-index: 8;
}
.flanker-frozen {
    background: radial-gradient(circle, #c8b0e0, #3a2060);
    border-color: #9088b0;
    filter: grayscale(0.5);
    animation: none;
    z-index: 8;
}
.power-up {
    background: radial-gradient(circle, #fff480, #aa6800);
    border-color: #ffd020;
    box-shadow: 0 0 20px rgba(255, 208, 32, 0.85);
    animation: powerUpBounce 1s ease-in-out infinite;
    z-index: 6;
}

/* ── Path Markers ─────────────────────────────────────────────────────────── */
.path-hunter::after,
.path-interceptor::before,
.path-flanker::after {
    content: "";
    position: absolute;
    width: 30%;
    height: 30%;
    border-radius: 50%;
    opacity: 0.9;
}
.path-hunter::after       { background: #00f0ff; box-shadow: 0 0 8px #00f0ff; top: 3px; right: 3px; }
.path-interceptor::before { background: #ff9020; box-shadow: 0 0 8px #ff9020; bottom: 3px; left: 3px; }
.path-flanker::after      { background: #d060ff; box-shadow: 0 0 8px #d060ff; bottom: 3px; right: 3px; }

/* ── Cell Label ───────────────────────────────────────────────────────────── */
.ase-cell-label {
    position: relative;
    z-index: 2;
    line-height: 1;
    user-select: none;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.5));
}

/* ── Legend ───────────────────────────────────────────────────────────────── */
.ase-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
}
.ase-pill {
    border: 1px solid var(--border-pill);
    border-radius: 999px;
    padding: 4px 11px;
    font-size: 11px;
    font-weight: 700;
    background: var(--bg-pill);
    color: var(--text-muted);
    transition: background 0.25s, color 0.25s, border-color 0.25s;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.ase-pill:hover {
    border-color: var(--accent-cyan);
    color: var(--text-primary);
}

/* ── Movement Keypad ──────────────────────────────────────────────────────── */
.ase-kpad {
    display: grid;
    grid-template-columns: repeat(3, 54px);
    gap: 6px;
    justify-content: center;
    margin-top: 8px;
}

/* ── Readout Rows ─────────────────────────────────────────────────────────── */
.ase-readout { display: grid; gap: 8px; font-size: 12px; color: var(--text-primary); }
.ase-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid var(--border-row);
    padding-bottom: 6px;
    color: var(--text-primary);
}
.ase-row b { color: var(--text-value); font-weight: 700; }
.ase-muted  { color: var(--text-muted); }
.ase-good   { color: var(--accent-green); }
.ase-warn   { color: var(--accent-warn); }
.ase-danger { color: var(--accent-red); }
.ase-purple { color: var(--accent-purple); }

/* ── Code Block ───────────────────────────────────────────────────────────── */
.ase-code {
    background: var(--bg-code);
    border: 1px solid var(--border-code);
    border-radius: 10px;
    padding: 10px 14px;
    font-family: ui-monospace, SFMono-Regular, Consolas, "Fira Code", monospace;
    color: var(--text-code);
    font-size: 12px;
    line-height: 1.6;
}

/* ── AI System Architecture & Intel Dossier (FIXED CONTRAST & STYLES) ─────── */
.ase-ai-dossier {
    background: var(--ai-box-bg) !important;
    border: 1px solid var(--ai-box-border) !important;
    border-radius: 16px;
    padding: 18px 20px;
    margin-top: 14px;
    box-shadow: var(--shadow-panel);
    transition: all 0.3s ease;
}
.ase-ai-dossier, .ase-ai-dossier * {
    color: var(--ai-box-text);
}
.ase-ai-dossier p,
.ase-ai-dossier div,
.ase-ai-dossier span,
.ase-ai-dossier li,
.ase-ai-dossier strong,
.ase-ai-dossier b {
    color: var(--ai-box-text) !important;
}
.ase-ai-roles-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 14px 0;
}
.ase-ai-role-card {
    background: var(--ai-card-bg);
    border: 1px solid var(--ai-card-border);
    border-radius: 12px;
    padding: 12px 14px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.ase-ai-role-card:hover {
    transform: translateY(-2px);
}
.hunter-card { border-left: 3px solid #ff3b5c; }
.interceptor-card { border-left: 3px solid #ff9020; }
.flanker-card { border-left: 3px solid #bf5af2; }

.ase-ai-role-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}
.ase-ai-role-icon {
    font-size: 20px;
}
.ase-ai-role-name {
    font-weight: 800;
    font-size: 12px;
    letter-spacing: 0.5px;
}
.ase-ai-role-badge {
    font-size: 10px;
    font-weight: 700;
    color: var(--ai-box-muted) !important;
    text-transform: uppercase;
}
.ase-ai-role-desc {
    font-size: 11.5px;
    line-height: 1.5;
    color: var(--ai-box-muted) !important;
}
.ase-ai-rules-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 14px;
}
.ase-ai-rule-item {
    background: var(--ai-card-bg);
    border: 1px solid var(--ai-card-border);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 11.5px;
    line-height: 1.55;
    color: var(--ai-box-text) !important;
}
.ase-ai-rule-item code {
    background: rgba(0, 0, 0, 0.18);
    padding: 2px 5px;
    border-radius: 4px;
    color: var(--accent-cyan) !important;
    font-weight: 700;
    font-size: 11px;
}
.ase-theme-light .ase-ai-rule-item code, [data-theme="light"] .ase-ai-rule-item code {
    background: rgba(9, 105, 218, 0.1);
}

/* ── Win / Loss Fullscreen Overlay with Interactive Buttons ───────────────── */
.ase-overlay {
    position: fixed;
    inset: 0;
    background: var(--bg-overlay);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    animation: overlayFadeIn 0.35s ease;
    padding: 20px;
}
@keyframes overlayFadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
.ase-overlay-card {
    background: var(--bg-overlay-card);
    border: 2px solid;
    border-radius: 24px;
    padding: 36px 44px;
    width: 100%;
    max-width: 540px;
    text-align: center;
    box-shadow: 0 16px 80px rgba(0, 0, 0, 0.6);
    animation: overlayCardPop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    z-index: 100000;
}
@keyframes overlayCardPop {
    from { transform: scale(0.75) translateY(30px); opacity: 0; }
    to   { transform: scale(1) translateY(0); opacity: 1; }
}
.ase-overlay-icon {
    font-size: 44px;
    margin-bottom: 8px;
    filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.4));
}
.ase-overlay-title {
    font-size: 32px;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
}
.ase-overlay-sub {
    font-size: 13.5px;
    color: var(--text-muted);
    margin-bottom: 22px;
    line-height: 1.5;
}
.ase-score-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 20px 0;
    text-align: left;
}
.ase-score-item {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 10px 14px;
}
.ase-theme-light .ase-score-item, [data-theme="light"] .ase-score-item {
    background: rgba(10, 30, 70, 0.04);
    border-color: rgba(10, 30, 70, 0.1);
}
.ase-score-item-label {
    color: var(--text-muted);
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.ase-score-item-value {
    font-size: 18px;
    font-weight: 800;
    margin-top: 3px;
    color: var(--text-value);
}

/* ── Modal Buttons ────────────────────────────────────────────────────────── */
.ase-modal-btn {
    min-height: 48px !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
    transition: transform 0.15s ease, box-shadow 0.2s ease !important;
    font-family: inherit !important;
}
.ase-modal-btn:hover {
    transform: translateY(-2px) !important;
}

/* ── Scan Panel ───────────────────────────────────────────────────────────── */
.ase-scan-agent {
    background: var(--bg-scan);
    border: 1px solid var(--border-code);
    border-radius: 10px;
    padding: 10px 14px;
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
    background: var(--bg-scan);
    border: 1px solid var(--border-row);
    border-radius: 10px;
    padding: 10px 12px;
    color: var(--text-primary);
}
.ase-delta-up   { color: var(--accent-green); font-size: 10px; font-weight: 700; }
.ase-delta-down { color: var(--accent-red);   font-size: 10px; font-weight: 700; }

/* ── Animations ───────────────────────────────────────────────────────────── */
@keyframes exitPulse {
    0%, 100% { box-shadow: 0 0 14px rgba(16, 245, 137, 0.6); }
    50%      { box-shadow: 0 0 32px rgba(16, 245, 137, 1); }
}
@keyframes playerGlow {
    0%, 100% { box-shadow: 0 0 18px rgba(49, 216, 255, 0.8); }
    50%      { box-shadow: 0 0 36px rgba(49, 216, 255, 1), 0 0 60px rgba(49, 216, 255, 0.4); }
}
@keyframes cloakShimmer {
    0%   { box-shadow: 0 0 18px rgba(191, 90, 242, 0.8); filter: hue-rotate(0deg); }
    50%  { box-shadow: 0 0 40px rgba(191, 90, 242, 1), 0 0 70px rgba(191, 90, 242, 0.5); filter: hue-rotate(30deg); }
    100% { box-shadow: 0 0 18px rgba(191, 90, 242, 0.8); filter: hue-rotate(0deg); }
}
@keyframes enemyPulse {
    0%, 100% { filter: brightness(1); }
    50%      { filter: brightness(1.25); }
}
@keyframes powerUpBounce {
    0%, 100% { transform: scale(1); box-shadow: 0 0 14px rgba(255, 208, 32, 0.7); }
    50%      { transform: scale(1.12); box-shadow: 0 0 28px rgba(255, 208, 32, 1); }
}

/* ── Separator ────────────────────────────────────────────────────────────── */
.ase-sep {
    border: none;
    border-top: 1px solid var(--border-row);
    margin: 10px 0;
}

/* ── Responsive ───────────────────────────────────────────────────────────── */
@media (max-width: 1200px) {
    .ase-grid-layout   { grid-template-columns: 1fr; }
    .ase-stat-grid     { grid-template-columns: repeat(3, 1fr); }
    .ase-lab-grid      { grid-template-columns: 1fr 1fr; }
    .ase-ai-roles-grid { grid-template-columns: 1fr; }
    .ase-ai-rules-grid { grid-template-columns: 1fr; }
}
@media (max-width: 700px) {
    .ase-stat-grid     { grid-template-columns: repeat(2, 1fr); }
    .ase-overlay-card  { padding: 24px 20px; min-width: unset; margin: 12px; }
    .ase-theme-toggle-floating { top: 10px; right: 10px; }
    .ase-theme-btn     { padding: 6px 12px !important; font-size: 11px !important; }
}
</style>
"""

button_css = {
    "minHeight": "40px",
    "borderRadius": "10px",
    "fontWeight": "800",
    "fontSize": "12px",
    "letterSpacing": "0.3px",
}

wide_button_css = {
    "width": "100%",
    "minHeight": "40px",
    "borderRadius": "10px",
    "fontWeight": "800",
    "fontSize": "12px",
}

kpad_button_css = {
    "width": "54px",
    "height": "48px",
    "borderRadius": "10px",
    "fontWeight": "900",
    "fontSize": "18px",
    "padding": "0",
    "minWidth": "0",
}
