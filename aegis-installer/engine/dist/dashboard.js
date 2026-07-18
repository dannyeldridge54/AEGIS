"use strict";
/**
 * AEGIS — Live Web Dashboard
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Serves a real-time web dashboard showing agent progress.
 * Zero dependencies — uses Node's built-in http module.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.createDashboard = createDashboard;
exports.dashboardHandler = dashboardHandler;
const http = __importStar(require("http"));
const DASHBOARD_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AEGIS Dashboard</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, monospace; background: #0a0a1a; color: #e0e0e0; padding: 20px; }
h1 { background: linear-gradient(90deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; font-size: 2rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px; }
.card { background: #1e1e3a; border: 1px solid #2e2e5a; border-radius: 8px; padding: 20px; }
.card h3 { color: #60a5fa; margin-bottom: 10px; }
.metric { font-size: 2rem; font-weight: bold; color: #34d399; }
.metric.score { color: #a78bfa; }
.log { background: #0f0f2a; border: 1px solid #2e2e5a; border-radius: 8px; padding: 15px; max-height: 300px; overflow-y: auto; font-size: 0.85rem; }
.log-entry { padding: 3px 0; border-bottom: 1px solid #1e1e3a; }
.log-entry.best { color: #34d399; }
.log-entry.discovery { color: #fbbf24; }
.strategies { display: flex; gap: 10px; flex-wrap: wrap; }
.strat { background: #2e2e5a; padding: 5px 10px; border-radius: 4px; font-size: 0.8rem; }
.strat.top { background: #34d39930; border: 1px solid #34d399; }
.phase { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; }
.phase.exploring { background: #60a5fa30; color: #60a5fa; }
.phase.exploiting { background: #34d39930; color: #34d399; }
.phase.curious { background: #fbbf2430; color: #fbbf24; }
.phase.converged { background: #a78bfa30; color: #a78bfa; }
</style>
</head>
<body>
<h1>AEGIS Dashboard</h1>
<div class="grid">
  <div class="card"><h3>Evaluations</h3><div class="metric" id="evals">0</div></div>
  <div class="card"><h3>Best Score</h3><div class="metric score" id="best">—</div></div>
  <div class="card"><h3>Phase</h3><div id="phase"><span class="phase exploring">exploring</span></div></div>
  <div class="card"><h3>Runtime</h3><div class="metric" id="runtime">0s</div></div>
</div>
<div class="grid">
  <div class="card"><h3>Best Parameters</h3><pre id="params" style="color:#94a3b8;font-size:0.9rem;">—</pre></div>
  <div class="card"><h3>Strategies (by performance)</h3><div class="strategies" id="strategies"></div></div>
</div>
<h3 style="margin:20px 0 10px;color:#94a3b8;">Event Log</h3>
<div class="log" id="log"></div>

<script>
function refresh() {
  fetch('/api/state').then(r => r.json()).then(s => {
    document.getElementById('evals').textContent = s.totalEvals.toLocaleString();
    document.getElementById('best').textContent = s.best ? s.best.score.toFixed(6) : '—';
    document.getElementById('runtime').textContent = s.runtime.toFixed(1) + 's';
    document.getElementById('phase').innerHTML = '<span class="phase ' + s.phase + '">' + s.phase + '</span>';
    if (s.best) {
      document.getElementById('params').textContent = JSON.stringify(s.best.params, null, 2);
    }
    const stratEl = document.getElementById('strategies');
    stratEl.innerHTML = s.strategies.slice(0, 6).map((st, i) =>
      '<div class="strat' + (i === 0 ? ' top' : '') + '">' + st.type + ' (' + st.avgImprovement.toFixed(3) + ')</div>'
    ).join('');
  }).catch(() => {});
}
function refreshLog() {
  fetch('/api/log').then(r => r.json()).then(entries => {
    const logEl = document.getElementById('log');
    logEl.innerHTML = entries.slice(-50).reverse().map(e => {
      const cls = e.type === 'new_best' ? 'best' : e.type === 'discovery' ? 'discovery' : '';
      return '<div class="log-entry ' + cls + '">' + e.text + '</div>';
    }).join('');
  }).catch(() => {});
}
setInterval(refresh, 1000);
setInterval(refreshLog, 2000);
refresh(); refreshLog();
</script>
</body>
</html>`;
function createDashboard(port = 3333) {
    let currentState = {
        best: null, totalEvals: 0, history: [], strategies: [],
        discoveries: [], runtime: 0, phase: 'exploring',
        ufe: {
            totalEvals: 0, usefulEvals: 0, ufeRatio: 0,
            convergenceVelocity: 0, aucc: 0,
            timeToTarget: { pct10: null, pct50: null, pct90: null },
            convergenceCurve: [],
        },
    };
    let logEntries = [];
    let server = null;
    const requestHandler = (req, res) => {
        const url = req.url || '/';
        if (url === '/api/state') {
            res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
            res.end(JSON.stringify(currentState));
        }
        else if (url === '/api/log') {
            res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
            res.end(JSON.stringify(logEntries.slice(-100)));
        }
        else {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(DASHBOARD_HTML);
        }
    };
    return {
        start() {
            server = http.createServer(requestHandler);
            server.listen(port, () => {
                console.log(`[AEGIS Dashboard] http://localhost:${port}`);
            });
        },
        stop() {
            server?.close();
        },
        updateState(state) {
            currentState = state;
        },
        addLog(entry) {
            logEntries.push({ ...entry, time: Date.now() });
            if (logEntries.length > 500)
                logEntries = logEntries.slice(-250);
        },
    };
}
/**
 * Event handler that feeds the dashboard.
 * Usage: agent.on(dashboardHandler(dashboard));
 */
function dashboardHandler(dashboard) {
    return (event) => {
        switch (event.type) {
            case 'report':
                dashboard.updateState(event.state);
                break;
            case 'new_best':
                dashboard.addLog({ type: 'new_best', text: `⭐ New best: ${event.result.score.toFixed(6)} [${event.result.strategy}]` });
                break;
            case 'discovery':
                dashboard.addLog({ type: 'discovery', text: `💡 ${event.discovery.description}` });
                break;
            case 'strategy_switch':
                dashboard.addLog({ type: 'switch', text: `🔄 ${event.from} → ${event.to}: ${event.reason}` });
                break;
            case 'evaluation':
                // Only log periodically to avoid flood
                break;
            default:
                dashboard.addLog({ type: event.type, text: JSON.stringify(event).slice(0, 100) });
        }
    };
}
//# sourceMappingURL=dashboard.js.map