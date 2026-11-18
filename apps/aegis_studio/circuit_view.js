// SERAPIS circuit view (Danny 2026-11-18): the circuit's layers stacked upward along the nesting chain A2 ⊂ D4 ⊂ E8 ⊂ Leech,
// each layer an A2 hexagonal patch; triangle laws drawn as filled triangles, up/down links as vertical wires.
// Closed = teal, open = pink. "Run circuit" calls the app (api.run_circuit) and redraws with live results.
(function () {
  const stage = document.getElementById('stage'); if (!stage) return;
  const tab = document.createElement('button'); tab.className = 'tab'; tab.setAttribute('role', 'tab'); tab.id = 't-circuit';
  tab.setAttribute('aria-selected', 'false'); tab.textContent = 'Circuit';
  document.querySelector('.tabs')?.insertBefore(tab, document.getElementById('t-classic'));
  const box = document.createElement('div'); box.id = 'circuitbox'; box.hidden = true;
  box.style.cssText = 'position:absolute;inset:0;z-index:5;background:var(--bg);display:flex;flex-direction:column';
  box.innerHTML = `<div style="display:flex;gap:8px;align-items:center;padding:8px 10px;border-bottom:1px solid var(--line)">
      <button class="btn" id="bcircuit">Run circuit</button><span class="pill" id="chealth">not run yet</span>
      <span class="small" id="cnote" style="color:var(--muted)">A2 core at the bottom → D4 sectors → E8 observables → Leech completion. Triangles = three routes agree; vertical wires = values carried up/down.</span></div>
    <svg id="csvg" style="flex:1;width:100%;min-height:0" role="img" aria-label="SERAPIS circuit: four stacked hexagonal layers"></svg>
    <div id="copen" class="small" style="padding:6px 10px;max-height:22%;overflow:auto;border-top:1px solid var(--line)"></div>`;
  stage.appendChild(box);
  const svg = box.querySelector('#csvg'), NS = 'http://www.w3.org/2000/svg';
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim() || '#888';
  const ORDER = ['A2', 'D4', 'E8', 'Leech', '10D'];
  const DEFAULT = { A2: { string_meter: [0, 0], serapis_e: [1, 0], serapis_point: [0, 1], X_ms: [-1, 1], L_nstar: [-1, 0], L_bridge: [0, -1], inverse_meter: [1, -1] },
    D4: { nstar_e: [0, 0], L_reheat: [1, 0], band_e: [0, 1], caps: [-1, 1] },
    E8: { wino_window: [0, 0], Q_dt: [1, 0], Q_panel: [0, 1], Q_future: [-1, 1], Q_life: [-1, 0], tests_cmb: [0, -1], G_A2: [1, -1] },
    Leech: { X_epstein: [0, 0], X_hexin: [1, 0], X_mod: [0, 1], S_stab: [-1, 1] } };
  let last = null;
  function el(n, a, txt) { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (txt != null) e.textContent = txt; svg.appendChild(e); return e; }
  function draw(res) {
    const W = svg.clientWidth || 900, H = svg.clientHeight || 600; svg.setAttribute('viewBox', `0 0 ${W} ${H}`); svg.innerHTML = '';
    const layers = (res && res.layers) || DEFAULT, laneH = H/ORDER.length, s = Math.min(W/7.5, laneH/2.1);
    const pos = {};
    ORDER.forEach((L, i) => {   // bottom layer = A2 (core); upward = nesting chain
      const cy = H - laneH*(i + 0.5), cx = W*0.46 + (i - 1.5)*s*0.9;   // slight shear so the stack reads as going up and out
      el('text', { x: 12, y: cy - laneH*0.32, fill: css('--muted'), 'font-size': 12 }, `${L} layer`);
      for (const [n, qr] of Object.entries(layers[L] || {})) {
        const [q, r] = qr; pos[n] = [cx + s*Math.sqrt(3)*(q + r/2), cy + s*0.42*1.5*r];   // flattened hex (perspective)
      }
    });
    const ok = c => c ? css('--teal') : css('--red');
    for (const l of (res?.laws || [])) {   // triangles first (under the wires)
      const pts = l.nodes.map(n => pos[n]).filter(Boolean);
      if (l.kind === 'triangle' && pts.length === 3) el('polygon', { points: pts.map(p => p.join(',')).join(' '), fill: ok(l.ok), 'fill-opacity': 0.18, stroke: ok(l.ok), 'stroke-width': 1.5 }).appendChild(Object.assign(document.createElementNS(NS, 'title'), { textContent: `${l.law}: ${l.text}` }));
    }
    for (const l of (res?.laws || [])) {
      const pts = l.nodes.map(n => pos[n]).filter(Boolean);
      if ((l.kind === 'up' || l.kind === 'down' || l.kind === 'link') && pts.length >= 2) {
        const e = el('line', { x1: pts[0][0], y1: pts[0][1], x2: pts[1][0], y2: pts[1][1], stroke: ok(l.ok), 'stroke-width': l.kind === 'link' ? 1.5 : 2.5, 'stroke-dasharray': l.kind === 'down' ? '6 4' : '' });
        e.appendChild(Object.assign(document.createElementNS(NS, 'title'), { textContent: `${l.kind.toUpperCase()} ${l.layer}: ${l.law} — ${l.text}` }));
      }
    }
    // hexagon outlines per layer (the lattice the components sit on)
    const st = {}; for (const l of (res?.laws || [])) for (const n of l.nodes) st[n] = (st[n] ?? true) && l.ok;
    for (const [n, [x, y]] of Object.entries(pos)) {
      const c = n in st ? ok(st[n]) : css('--muted');
      const g = el('circle', { cx: x, cy: y, r: 7, fill: css('--panel2'), stroke: c, 'stroke-width': 2.5 });
      g.appendChild(Object.assign(document.createElementNS(NS, 'title'), { textContent: n + (res ? ((res.laws || []).filter(l => l.nodes.includes(n)).map(l => `\n${l.ok ? '✓' : '✗'} ${l.law}: ${l.text}`).join('')) : '') }));
      el('text', { x: x + 10, y: y - 8, fill: css('--fg'), 'font-size': 11, 'paint-order': 'stroke', stroke: css('--bg'), 'stroke-width': 3 }, n);
    }
    if (res) {
      const h = box.querySelector('#chealth'); h.textContent = `health ${(res.health*100).toFixed(0)}% · ${res.closed}/${res.n_laws} laws closed · ${res.seconds}s`;
      h.style.color = res.open.length ? css('--red') : css('--teal'); h.style.borderColor = h.style.color;
      box.querySelector('#copen').innerHTML = res.open.length ? '<b>Open circuits</b><br>' + res.open.map(o => `✗ ${o.layer} · ${o.nodes.join('/')} · ${o.law}: ${o.text}`).join('<br>') : 'All circuits closed. Hover a triangle, wire or node for its law and numbers.';
    }
  }
  async function runIt() {
    const api = window.pywebview?.api; const b = box.querySelector('#bcircuit');
    if (!api || !api.run_circuit) { box.querySelector('#copen').textContent = 'Run the circuit from the Janus app (it needs the toolkit registry).'; return; }
    b.disabled = true; b.textContent = 'Running…';
    try { last = await api.run_circuit(); window.__circuitLast = last; draw(last); } catch (e) { box.querySelector('#copen').textContent = 'Circuit error: ' + e; }
    b.disabled = false; b.textContent = 'Run circuit';
  }
  box.querySelector('#bcircuit').onclick = runIt;
  function show(on) {
    box.hidden = !on; tab.setAttribute('aria-selected', String(on));
    if (on) { document.querySelectorAll('.tabs .tab').forEach(t => { if (t !== tab) t.setAttribute('aria-selected', 'false'); }); draw(last); }
  }
  tab.addEventListener('click', () => show(true));
  document.querySelectorAll('.tabs .tab').forEach(t => { if (t !== tab) t.addEventListener('click', () => show(false)); });
  addEventListener('resize', () => { if (!box.hidden) draw(last); });
  window.circuitResult = r => { last = r; window.__circuitLast = r; if (!box.hidden) draw(r); };   // the weave pass can push its circuit result here
})();
