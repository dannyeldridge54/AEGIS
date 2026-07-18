#!/usr/bin/env node
/**
 * AEGIS Optimizer — Desktop Application Launcher
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Launches the AEGIS dashboard + API server and opens it in your browser.
 * This is the main entry point when running AEGIS as a desktop program.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PORT = parseInt(process.env.AEGIS_PORT || '8888');
const API_PORT = parseInt(process.env.AEGIS_API_PORT || '3000');

// ── Landing page with embedded app UI ────────────────────────────────────────

function buildAppHTML() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AEGIS Optimizer</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0e14; color: #c9d1d9; }
  .app { display: flex; flex-direction: column; height: 100vh; }

  /* Top bar */
  .topbar { background: #161b22; border-bottom: 1px solid #30363d; padding: 12px 24px; display: flex; align-items: center; gap: 16px; }
  .topbar .logo { font-size: 20px; font-weight: bold; color: #58a6ff; }
  .topbar .logo span { color: #e6edf3; }
  .topbar .status { margin-left: auto; display: flex; gap: 12px; align-items: center; }
  .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
  .dot.green { background: #3fb950; }
  .dot.yellow { background: #d29922; }
  .dot.red { background: #f85149; }
  .status-text { font-size: 12px; color: #8b949e; }

  /* Tab bar */
  .tabs { background: #0d1117; border-bottom: 1px solid #21262d; display: flex; padding: 0 24px; }
  .tab { padding: 10px 20px; color: #8b949e; cursor: pointer; border-bottom: 2px solid transparent; font-size: 13px; }
  .tab:hover { color: #c9d1d9; }
  .tab.active { color: #58a6ff; border-bottom-color: #58a6ff; }

  /* Content */
  .content { flex: 1; display: flex; }
  .sidebar { width: 280px; background: #0d1117; border-right: 1px solid #21262d; padding: 20px; overflow-y: auto; }
  .main { flex: 1; padding: 0; }
  .main iframe { width: 100%; height: 100%; border: none; }

  /* Sidebar sections */
  .section-title { font-size: 11px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin: 16px 0 8px; }
  .section-title:first-child { margin-top: 0; }

  .btn { display: block; width: 100%; padding: 10px 14px; margin: 4px 0; border: 1px solid #30363d; border-radius: 6px; background: #161b22; color: #c9d1d9; text-align: left; cursor: pointer; font-size: 13px; transition: all 0.15s; }
  .btn:hover { border-color: #58a6ff; background: #1c2128; }
  .btn.primary { background: #238636; border-color: #238636; color: white; }
  .btn.primary:hover { background: #2ea043; }

  .info-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 12px; border-bottom: 1px solid #21262d; }
  .info-label { color: #8b949e; }
  .info-value { color: #e6edf3; font-weight: 500; }

  /* Quick optimize form */
  .form-group { margin: 8px 0; }
  .form-group label { display: block; font-size: 11px; color: #8b949e; margin-bottom: 4px; }
  .form-group input, .form-group textarea, .form-group select {
    width: 100%; padding: 8px; background: #0d1117; border: 1px solid #30363d; border-radius: 4px; color: #c9d1d9; font-size: 12px; font-family: monospace;
  }
  .form-group textarea { height: 80px; resize: vertical; }
  #result-box { margin-top: 12px; padding: 10px; background: #161b22; border: 1px solid #30363d; border-radius: 6px; font-size: 11px; font-family: monospace; white-space: pre-wrap; display: none; max-height: 200px; overflow-y: auto; }
</style>
</head>
<body>
<div class="app">
  <div class="topbar">
    <div class="logo">⚡ <span>AEGIS</span> Optimizer</div>
    <div class="status">
      <span class="dot green" id="api-dot"></span>
      <span class="status-text" id="api-status">API: Checking...</span>
      <span class="dot yellow" id="engine-dot"></span>
      <span class="status-text" id="engine-status">Engine: Idle</span>
    </div>
  </div>

  <div class="tabs">
    <div class="tab active" onclick="switchTab('optimize')">🔍 Optimize</div>
    <div class="tab" onclick="switchTab('benchmark')">🏎️ Benchmark</div>
    <div class="tab" onclick="switchTab('api')">🌐 API Server</div>
    <div class="tab" onclick="switchTab('docs')">📖 Docs</div>
  </div>

  <div class="content">
    <div class="sidebar">
      <div class="section-title">Quick Optimize</div>
      <div class="form-group">
        <label>Objective Function</label>
        <textarea id="obj-fn" placeholder="(p) => (p.x-3)**2 + (p.y+2)**2">(p) => (p.x-3)**2 + (p.y+2)**2</textarea>
      </div>
      <div class="form-group">
        <label>Parameters (JSON)</label>
        <textarea id="params-input" placeholder='[{"name":"x","min":-10,"max":10}]'>[{"name":"x","min":-10,"max":10},{"name":"y","min":-10,"max":10}]</textarea>
      </div>
      <div class="form-group">
        <label>Max Evaluations</label>
        <input type="number" id="max-evals" value="1000">
      </div>
      <div class="form-group">
        <label>Engine</label>
        <select id="engine-select">
          <option value="single">Single Engine</option>
          <option value="dual" selected>Dual Engine (Cross-Pollination)</option>
        </select>
      </div>
      <button class="btn primary" onclick="runOptimize()">▶ Run Optimization</button>

      <div id="result-box"></div>

      <div class="section-title">System Info</div>
      <div class="info-row"><span class="info-label">Version</span><span class="info-value">1.0.0</span></div>
      <div class="info-row"><span class="info-label">API Port</span><span class="info-value">${API_PORT}</span></div>
      <div class="info-row"><span class="info-label">App Port</span><span class="info-value">${PORT}</span></div>
      <div class="info-row"><span class="info-label">Node</span><span class="info-value" id="node-ver">—</span></div>
      <div class="info-row"><span class="info-label">Platform</span><span class="info-value">${process.platform}</span></div>

      <div class="section-title">Quick Actions</div>
      <button class="btn" onclick="runBenchmark()">🏎️ Run Benchmark</button>
      <button class="btn" onclick="openDocs()">📖 API Documentation</button>
      <button class="btn" onclick="window.open('https://github.com/dannyeldridge54/AEGIS')">⭐ GitHub</button>
    </div>
    <div class="main">
      <iframe id="main-frame" src="about:blank"></iframe>
    </div>
  </div>
</div>

<script>
  document.getElementById('node-ver').textContent = '${process.version}';

  // Check API health
  async function checkAPI() {
    try {
      const r = await fetch('http://localhost:${API_PORT}/api/health');
      const d = await r.json();
      document.getElementById('api-dot').className = 'dot green';
      document.getElementById('api-status').textContent = 'API: Online (' + d.activeJobs + ' jobs)';
    } catch {
      document.getElementById('api-dot').className = 'dot red';
      document.getElementById('api-status').textContent = 'API: Offline';
    }
  }
  setInterval(checkAPI, 5000);
  checkAPI();

  function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    const frame = document.getElementById('main-frame');
    switch(tab) {
      case 'optimize': frame.src = 'about:blank'; break;
      case 'benchmark': runBenchmark(); break;
      case 'api': frame.src = 'http://localhost:${API_PORT}/api/info'; break;
      case 'docs': frame.srcdoc = buildDocs(); break;
    }
  }

  async function runOptimize() {
    const box = document.getElementById('result-box');
    box.style.display = 'block';
    box.textContent = '⏳ Optimizing...';
    document.getElementById('engine-dot').className = 'dot green';
    document.getElementById('engine-status').textContent = 'Engine: Running';

    const engine = document.getElementById('engine-select').value;
    const endpoint = engine === 'dual' ? '/api/dual-optimize' : '/api/optimize';

    try {
      const body = {
        objective: document.getElementById('obj-fn').value,
        parameters: JSON.parse(document.getElementById('params-input').value),
        maxEvals: parseInt(document.getElementById('max-evals').value),
      };
      if (engine === 'dual') body.cycles = 5;

      const r = await fetch('http://localhost:${API_PORT}' + endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer demo-key-001' },
        body: JSON.stringify(body),
      });
      const job = await r.json();

      // Poll for result
      let attempts = 0;
      const poll = setInterval(async () => {
        attempts++;
        try {
          const res = await fetch('http://localhost:${API_PORT}/api/result/' + job.jobId, {
            headers: { 'Authorization': 'Bearer demo-key-001' }
          });
          const data = await res.json();
          if (data.status === 'completed') {
            clearInterval(poll);
            document.getElementById('engine-dot').className = 'dot yellow';
            document.getElementById('engine-status').textContent = 'Engine: Idle';
            let text = '✅ OPTIMIZATION COMPLETE\\n';
            text += '═══════════════════════════\\n';
            if (data.best) {
              text += 'Score: ' + data.best.score.toFixed(8) + '\\n';
              text += 'Parameters:\\n';
              for (const [k,v] of Object.entries(data.best.params)) {
                text += '  ' + k + ': ' + (typeof v === 'number' ? v.toPrecision(8) : v) + '\\n';
              }
            }
            text += 'Evals: ' + data.totalEvals + '\\n';
            if (data.ufe) text += 'UFE: ' + (data.ufe.ufeRatio*100).toFixed(1) + '%\\n';
            box.textContent = text;
          } else if (attempts > 120) {
            clearInterval(poll);
            box.textContent = '⏱ Timeout — check API for results';
          } else {
            box.textContent = '⏳ Running... (' + attempts + 's)';
          }
        } catch(e) { box.textContent = '⏳ Waiting... ' + e.message; }
      }, 1000);
    } catch(e) {
      box.textContent = '❌ Error: ' + e.message + '\\n\\nMake sure API server is running (port ${API_PORT})';
      document.getElementById('engine-dot').className = 'dot red';
      document.getElementById('engine-status').textContent = 'Engine: Error';
    }
  }

  function runBenchmark() {
    const frame = document.getElementById('main-frame');
    frame.srcdoc = '<html><body style="background:#0a0e14;color:#c9d1d9;font-family:monospace;padding:24px;"><pre id="out">Running benchmarks via CLI...\\nOpen a terminal and run: aegis benchmark</pre></body></html>';
  }

  function openDocs() { switchTab('docs'); }

  function buildDocs() {
    return '<html><head><style>body{background:#0a0e14;color:#c9d1d9;font-family:-apple-system,sans-serif;padding:32px;max-width:800px;margin:0 auto;line-height:1.7}h1{color:#58a6ff}h2{color:#e6edf3;margin-top:32px}code{background:#161b22;padding:2px 6px;border-radius:3px;font-size:13px}pre{background:#161b22;padding:16px;border-radius:6px;overflow-x:auto;font-size:13px;border:1px solid #30363d}.endpoint{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:16px;margin:8px 0}.method{color:#3fb950;font-weight:bold}.url{color:#58a6ff}</style></head><body>'
    + '<h1>⚡ AEGIS Optimizer API</h1>'
    + '<p>REST API for cloud-hosted optimization. All endpoints require <code>Authorization: Bearer YOUR_KEY</code></p>'
    + '<h2>Endpoints</h2>'
    + '<div class="endpoint"><span class="method">POST</span> <span class="url">/api/optimize</span><br>Single-engine optimization<br><pre>{ "objective": "(p) => ...", "parameters": [...], "maxEvals": 1000 }</pre></div>'
    + '<div class="endpoint"><span class="method">POST</span> <span class="url">/api/dual-optimize</span><br>Dual-engine with cross-pollination<br><pre>{ "objective": "(p) => ...", "parameters": [...], "maxEvals": 1000, "cycles": 5 }</pre></div>'
    + '<div class="endpoint"><span class="method">GET</span> <span class="url">/api/status/:jobId</span><br>Check job status</div>'
    + '<div class="endpoint"><span class="method">GET</span> <span class="url">/api/result/:jobId</span><br>Get completed job results</div>'
    + '<div class="endpoint"><span class="method">GET</span> <span class="url">/api/health</span><br>Server health check</div>'
    + '<div class="endpoint"><span class="method">GET</span> <span class="url">/api/info</span><br>Pricing and documentation</div>'
    + '<h2>SDK Usage</h2>'
    + '<pre>const { optimize, dualOptimize } = require("@aegis/optimizer");\\n\\nconst result = await optimize({\\n  objective: (p) => yourCostFunction(p),\\n  parameters: [\\n    { name: "x", min: 0, max: 100 },\\n    { name: "y", min: -50, max: 50 },\\n  ],\\n});\\n\\nconsole.log(result.best); // { params: { x: 42.7, y: -3.1 }, score: 0.0001 }</pre>'
    + '<h2>CLI</h2>'
    + '<pre>aegis optimize --config task.json\\naegis dual --config task.json\\naegis benchmark\\naegis serve --port 3000</pre>'
    + '</body></html>';
  }
</script>
</body>
</html>`;
}

// ── App server ───────────────────────────────────────────────────────────────

const appServer = http.createServer((req, res) => {
  if (req.url === '/' || req.url === '/index.html') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(buildAppHTML());
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

// ── Start API + App ──────────────────────────────────────────────────────────

function openBrowser(url) {
  try {
    switch (process.platform) {
      case 'win32': execSync(`start "" "${url}"`, { stdio: 'ignore' }); break;
      case 'darwin': execSync(`open "${url}"`, { stdio: 'ignore' }); break;
      default: execSync(`xdg-open "${url}"`, { stdio: 'ignore' }); break;
    }
  } catch { /* browser open is best-effort */ }
}

console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  ⚡ AEGIS Optimizer — Desktop Application                    ║
║  Copyright (c) 2012-2026 Danny Lee Eldridge.                 ║
╚═══════════════════════════════════════════════════════════════╝
`);

// Start API server
process.env.PORT = String(API_PORT);
process.env.API_KEYS = process.env.API_KEYS || 'demo-key-001';
require('./saas/server');

// Start app UI server
appServer.listen(PORT, () => {
  console.log(`\n  🖥️  App UI:     http://localhost:${PORT}`);
  console.log(`  🌐 API:        http://localhost:${API_PORT}`);
  console.log(`  📊 Health:     http://localhost:${API_PORT}/api/health`);
  console.log(`\n  Opening in browser...\n`);
  openBrowser(`http://localhost:${PORT}`);
});
