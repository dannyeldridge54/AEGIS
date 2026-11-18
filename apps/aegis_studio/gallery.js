// Janus Gallery (Danny 2026-11-18: "make them all", "with blue magenta and full rgb").
// Thirteen displays of the same weave/circuit data, each with two palettes: Janus (blue → magenta) and Spectrum (full RGB).
// All 2D canvas (no second WebGL context); only the visible display animates.
(function () {
  if (typeof WEB === 'undefined') return;
  const stage = document.getElementById('stage'); if (!stage) return;
  const tab = document.createElement('button'); tab.className = 'tab'; tab.setAttribute('role', 'tab'); tab.id = 't-gallery';
  tab.setAttribute('aria-selected', 'false'); tab.textContent = 'Gallery';
  document.querySelector('.tabs')?.insertBefore(tab, document.getElementById('t-classic'));
  const VIEWS = [['bundle', 'Edge bundling'], ['chord', 'Chord'], ['hive', 'Hive'], ['force', '3D force'], ['arc', 'Arc flow'],
    ['hyper', 'Hyperbolic'], ['modular', 'Poincaré / SL(2,ℤ)'], ['e8', 'E8 Petrie'], ['circuit3d', 'Circuit 3D'],
    ['spectro', 'Resonance'], ['history', 'History'], ['cymatics', 'Cymatics'], ['sky', 'Sky map']];
  const box = document.createElement('div'); box.id = 'gallerybox'; box.hidden = true;
  box.style.cssText = 'position:absolute;inset:0;z-index:6;background:var(--bg);display:flex;flex-direction:column';
  box.innerHTML = `<div id="gtabs" style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:8px 10px;border-bottom:1px solid var(--line)"></div>
    <div style="position:relative;flex:1;min-height:0"><canvas id="gcv" style="position:absolute;inset:0;width:100%;height:100%"></canvas>
    <div id="gcap" class="small" style="position:absolute;left:12px;bottom:10px;right:12px;color:var(--muted);pointer-events:none"></div></div>`;
  stage.appendChild(box);
  const gt = box.querySelector('#gtabs'), cv = box.querySelector('#gcv'), cx = cv.getContext('2d'), cap = box.querySelector('#gcap');
  const palBtn = document.createElement('button'); palBtn.className = 'btn on'; palBtn.textContent = 'Palette: blue→magenta';
  const soundBtn = document.createElement('button'); soundBtn.className = 'btn'; soundBtn.textContent = 'Sound: off'; soundBtn.hidden = true;
  let cur = 'bundle', spectrum = false, t0 = performance.now();
  try { cur = localStorage.getItem('janus.gallery') || 'bundle'; spectrum = localStorage.getItem('janus.gpal') === 'rgb'; } catch (e) {}
  VIEWS.forEach(([k, name]) => { const b = document.createElement('button'); b.className = 'btn'; b.textContent = name; b.dataset.k = k;
    b.onclick = () => { cur = k; mark(); try { localStorage.setItem('janus.gallery', k); } catch (e) {} reset(); }; gt.appendChild(b); });
  gt.appendChild(palBtn); gt.appendChild(soundBtn);
  palBtn.onclick = () => { spectrum = !spectrum; palBtn.textContent = spectrum ? 'Palette: full RGB' : 'Palette: blue→magenta'; try { localStorage.setItem('janus.gpal', spectrum ? 'rgb' : 'jm'); } catch (e) {} };
  palBtn.textContent = spectrum ? 'Palette: full RGB' : 'Palette: blue→magenta';
  function mark() { gt.querySelectorAll('[data-k]').forEach(b => b.classList.toggle('on', b.dataset.k === cur)); soundBtn.hidden = cur !== 'spectro'; }
  // palette: u in [0,1] → colour.  Janus: blue (215°) → magenta (295°).  Spectrum: red (0°) → violet (300°).
  const pal = (u, a = 1, l = 60) => { u = Math.min(1, Math.max(0, u)); const h = spectrum ? u*300 : 215 + u*80; return `hsla(${h},100%,${l}%,${a})`; };
  // ---- shared data ----
  const N = WEB.nodes, E = WEB.edges, id2i = Object.fromEntries(N.map((n, i) => [n.id, i]));
  const LANES = ['left', 'centre', 'right', 'theory', 'janus', 'strings', 'wiring', 'lattice', 'lhc'];
  const laneOf = n => Math.max(0, LANES.indexOf(n.lane)); const deg = N.map(() => 0); E.forEach(e => { deg[id2i[e.s]]++; deg[id2i[e.t]]++; });
  const order = N.map((n, i) => i).sort((a, b) => laneOf(N[a]) - laneOf(N[b]) || deg[b] - deg[a]);
  const firstD = N.map(n => { const m = (n.refs + ' ' + n.label).match(/D(\d{2,4})/g); return m ? Math.min(...m.map(x => +x.slice(1))) : 9999; });
  let W = 0, H = 0;
  function size() { const r = cv.getBoundingClientRect(), d = Math.min(2, devicePixelRatio || 1); W = r.width; H = r.height; cv.width = W*d; cv.height = H*d; cx.setTransform(d, 0, 0, d, 0, 0); }
  function clear() { cx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg') || '#04020b'; cx.fillRect(0, 0, W, H); }
  const glow = (c, b) => { cx.shadowColor = c; cx.shadowBlur = b; };
  const text = (s, x, y, c = '#cfc6ff', f = 11) => { cx.shadowBlur = 0; cx.fillStyle = c; cx.font = `${f}px system-ui, sans-serif`; cx.fillText(s, x, y); };
  // ---- 1. edge bundling (radial, wires routed through their lane anchors) ----
  function bundle(t) {
    const R = Math.min(W, H)*0.42, X = W/2, Y = H/2, ang = {}; order.forEach((i, k) => ang[i] = k/N.length*2*Math.PI + t*0.02);
    const anchor = l => { const ks = order.filter(i => laneOf(N[i]) === l); const a = ks.reduce((s, i) => s + ang[i], 0)/Math.max(1, ks.length); return [X + R*0.45*Math.cos(a), Y + R*0.45*Math.sin(a)]; };
    const A = LANES.map((_, l) => anchor(l)); cx.lineWidth = 1.1; cx.globalCompositeOperation = 'lighter';
    E.forEach(e => { const a = id2i[e.s], b = id2i[e.t]; const pa = [X + R*Math.cos(ang[a]), Y + R*Math.sin(ang[a])], pb = [X + R*Math.cos(ang[b]), Y + R*Math.sin(ang[b])];
      const qa = A[laneOf(N[a])], qb = A[laneOf(N[b])]; const g = cx.createLinearGradient(pa[0], pa[1], pb[0], pb[1]);
      g.addColorStop(0, pal(ang[a]/(2*Math.PI) % 1, 0.5)); g.addColorStop(1, pal(ang[b]/(2*Math.PI) % 1, 0.5)); cx.strokeStyle = g;
      cx.beginPath(); cx.moveTo(...pa); cx.bezierCurveTo(qa[0], qa[1], qb[0], qb[1], pb[0], pb[1]); cx.stroke(); });
    cx.globalCompositeOperation = 'source-over';
    order.forEach(i => { const x = X + R*Math.cos(ang[i]), y = Y + R*Math.sin(ang[i]); const c = pal(ang[i]/(2*Math.PI) % 1); glow(c, 8); cx.fillStyle = c; cx.beginPath(); cx.arc(x, y, 2 + Math.sqrt(deg[i]), 0, 7); cx.fill(); });
    cap.textContent = 'Edge bundling — every wire routed through its lanes’ anchors, so parallel wires merge into cables. Colour runs along each wire from its start node to its end node.';
  }
  // ---- 2. chord (lanes around a circle, ribbons ∝ wires between lanes) ----
  function chord(t) {
    const X = W/2, Y = H/2, R = Math.min(W, H)*0.38, M = LANES.map(() => LANES.map(() => 0)); E.forEach(e => { M[laneOf(N[id2i[e.s]])][laneOf(N[id2i[e.t]])]++; });
    const tot = M.map((r, i) => r.reduce((s, v) => s + v, 0) + M.reduce((s, row) => s + row[i], 0)), sum = tot.reduce((a, b) => a + b, 0), gap = 0.04;
    let a = -Math.PI/2 + t*0.03; const arc = LANES.map((_, i) => { const w = (2*Math.PI - gap*LANES.length)*tot[i]/sum; const r = [a, a + w]; a += w + gap; return r; });
    const cursor = arc.map(r => r[0]);
    cx.globalCompositeOperation = 'lighter';
    for (let i = 0; i < 9; i++) for (let j = 0; j < 9; j++) { const v = M[i][j]; if (!v) continue;
      const wi = (arc[i][1] - arc[i][0])*v/tot[i], wj = (arc[j][1] - arc[j][0])*v/tot[j]; const a0 = cursor[i], a1 = a0 + wi; cursor[i] = a1; const b0 = cursor[j], b1 = b0 + wj; cursor[j] = b1;
      const g = cx.createLinearGradient(X + R*Math.cos(a0), Y + R*Math.sin(a0), X + R*Math.cos(b0), Y + R*Math.sin(b0)); g.addColorStop(0, pal(i/8, 0.45)); g.addColorStop(1, pal(j/8, 0.45));
      cx.fillStyle = g; cx.beginPath(); cx.arc(X, Y, R, a0, a1); cx.quadraticCurveTo(X, Y, X + R*Math.cos(b0), Y + R*Math.sin(b0)); cx.arc(X, Y, R, b0, b1); cx.quadraticCurveTo(X, Y, X + R*Math.cos(a0), Y + R*Math.sin(a0)); cx.fill(); }
    cx.globalCompositeOperation = 'source-over';
    arc.forEach(([s, e], i) => { const c = pal(i/8); glow(c, 10); cx.strokeStyle = c; cx.lineWidth = 10; cx.beginPath(); cx.arc(X, Y, R + 8, s, e); cx.stroke();
      const m = (s + e)/2; text(LANES[i], X + (R + 26)*Math.cos(m) - 18, Y + (R + 26)*Math.sin(m) + 4, c, 12); });
    cap.textContent = 'Chord — the nine lanes around the circle; each ribbon’s width is the number of wires between two lanes.';
  }
  // ---- 3. hive (one axis per lane, radius = rank by degree) ----
  function hive(t) {
    const X = W/2, Y = H/2, R = Math.min(W, H)*0.44, ax = l => -Math.PI/2 + l*2*Math.PI/9 + 0.15*Math.sin(t*0.2);
    const rank = {}; LANES.forEach((L, l) => { const ks = N.map((n, i) => i).filter(i => laneOf(N[i]) === l).sort((a, b) => deg[b] - deg[a]); ks.forEach((i, k) => rank[i] = 0.18 + 0.82*(k + 0.5)/Math.max(1, ks.length)); });
    const pos = i => { const a = ax(laneOf(N[i])), r = R*rank[i]; return [X + r*Math.cos(a), Y + r*Math.sin(a)]; };
    LANES.forEach((L, l) => { const a = ax(l); cx.strokeStyle = pal(l/8, 0.35); cx.lineWidth = 2; cx.beginPath(); cx.moveTo(X + 0.15*R*Math.cos(a), Y + 0.15*R*Math.sin(a)); cx.lineTo(X + R*Math.cos(a), Y + R*Math.sin(a)); cx.stroke(); text(L, X + (R + 14)*Math.cos(a) - 14, Y + (R + 14)*Math.sin(a), pal(l/8), 12); });
    cx.globalCompositeOperation = 'lighter'; cx.lineWidth = 1;
    E.forEach(e => { const a = id2i[e.s], b = id2i[e.t]; const p = pos(a), q = pos(b); cx.strokeStyle = pal((laneOf(N[a]) + laneOf(N[b]))/16, 0.4); cx.beginPath(); cx.moveTo(...p); cx.quadraticCurveTo(X, Y, ...q); cx.stroke(); });
    cx.globalCompositeOperation = 'source-over';
    N.forEach((n, i) => { const p = pos(i), c = pal(laneOf(n)/8); glow(c, 6); cx.fillStyle = c; cx.beginPath(); cx.arc(p[0], p[1], 2.5, 0, 7); cx.fill(); });
    cap.textContent = 'Hive plot — one axis per lane; a node sits further out the fewer links it has. Wires arc between axes.';
  }
  // ---- 4. 3D force graph (springs + repulsion, projected; slow spin) ----
  let F = null;
  function forceInit() { F = N.map((n, i) => ({ x: Math.cos(i)*50, y: Math.sin(i*1.3)*50, z: Math.sin(i*0.7)*50, vx: 0, vy: 0, vz: 0 })); }
  function force(t) {
    if (!F) forceInit();
    for (let it = 0; it < 2; it++) {
      for (let i = 0; i < F.length; i++) for (let j = i + 1; j < F.length; j++) { const a = F[i], b = F[j]; let dx = a.x - b.x, dy = a.y - b.y, dz = a.z - b.z; const d2 = dx*dx + dy*dy + dz*dz + 25, f = 60/d2;
        a.vx += dx*f; a.vy += dy*f; a.vz += dz*f; b.vx -= dx*f; b.vy -= dy*f; b.vz -= dz*f; }
      E.forEach(e => { const a = F[id2i[e.s]], b = F[id2i[e.t]]; const dx = b.x - a.x, dy = b.y - a.y, dz = b.z - a.z; const d = Math.hypot(dx, dy, dz) + 1e-6, f = 0.02*(d - 22)/d;
        a.vx += dx*f; a.vy += dy*f; a.vz += dz*f; b.vx -= dx*f; b.vy -= dy*f; b.vz -= dz*f; });
      F.forEach(p => { p.vx -= p.x*0.004; p.vy -= p.y*0.004; p.vz -= p.z*0.004; const sp = Math.hypot(p.vx, p.vy, p.vz); if (sp > 4) { p.vx *= 4/sp; p.vy *= 4/sp; p.vz *= 4/sp; } p.x += (p.vx *= 0.8); p.y += (p.vy *= 0.8); p.z += (p.vz *= 0.8); });
    }
    const a = t*0.25, ca = Math.cos(a), sa = Math.sin(a), ext = Math.max(20, ...F.map(p => Math.hypot(p.x, p.y, p.z))), s = Math.min(W, H)*0.42/ext;
    const pj = p => { const x = p.x*ca - p.z*sa, z = (p.x*sa + p.z*ca)/ext, k = 1/(1 + 0.35*z); return [W/2 + x*s*k, H/2 + p.y*s*k, k, z]; };
    const P2 = F.map(pj); cx.globalCompositeOperation = 'lighter'; cx.lineWidth = 1;
    E.forEach(e => { const p = P2[id2i[e.s]], q = P2[id2i[e.t]]; const g = cx.createLinearGradient(p[0], p[1], q[0], q[1]); g.addColorStop(0, pal((p[0])/W, 0.5)); g.addColorStop(1, pal(q[0]/W, 0.5)); cx.strokeStyle = g; cx.beginPath(); cx.moveTo(p[0], p[1]); cx.lineTo(q[0], q[1]); cx.stroke(); });
    cx.globalCompositeOperation = 'source-over';
    P2.map((p, i) => [p, i]).sort((u, v) => v[0][3] - u[0][3]).forEach(([p, i]) => { const c = pal(p[0]/W); glow(c, 10*p[2]); cx.fillStyle = c; cx.beginPath(); cx.arc(p[0], p[1], Math.max(0.5, (2 + Math.sqrt(deg[i]))*p[2]), 0, 7); cx.fill(); });
    cap.textContent = '3D force graph — nodes repel, wires pull like springs; the web settles into its own shape and turns slowly.';
  }
  // ---- 5. arc flow (lanes along a line; supporting wires above, opposing wires below) ----
  function arcflow(t) {
    const xs = {}; order.forEach((i, k) => xs[i] = 30 + (W - 60)*k/(N.length - 1)); const Y = H*0.55; cx.globalCompositeOperation = 'lighter'; cx.lineWidth = 1.2;
    E.forEach((e, k) => { const a = xs[id2i[e.s]], b = xs[id2i[e.t]], m = (a + b)/2, r = Math.abs(b - a)/2, up = e.sign >= 0;
      const ph = (t*0.4 + k*0.031) % 1; const g = cx.createLinearGradient(Math.min(a, b), 0, Math.max(a, b), 0); g.addColorStop(0, pal(Math.min(a, b)/W, 0.55)); g.addColorStop(1, pal(Math.max(a, b)/W, 0.55));
      cx.strokeStyle = g; cx.beginPath(); cx.ellipse(m, Y, r, Math.min(r, H*0.4), 0, up ? Math.PI : 0, up ? 2*Math.PI : Math.PI); cx.stroke();
      const ang = up ? Math.PI + ph*Math.PI : ph*Math.PI, px = m + r*Math.cos(ang)*(a < b ? -1 : 1), py = Y + Math.min(r, H*0.4)*Math.sin(ang); cx.fillStyle = '#fff'; cx.fillRect(px - 1, py - 1, 2, 2); });
    cx.globalCompositeOperation = 'source-over';
    order.forEach(i => { const c = pal(xs[i]/W); glow(c, 6); cx.fillStyle = c; cx.fillRect(xs[i] - 1.5, Y - 4, 3, 8); });
    cap.textContent = 'Arc flow — nodes along a line, grouped by lane; supporting wires arc above, opposing wires below; sparks run along each wire.';
  }
  // ---- 6. hyperbolic (Poincaré-disk fisheye of the weave; focus follows the mouse) ----
  let focus = [0, 0];
  cv.addEventListener('mousemove', ev => { const r = cv.getBoundingClientRect(); focus = [(ev.clientX - r.left - W/2)/(Math.min(W, H)*0.45), (ev.clientY - r.top - H/2)/(Math.min(W, H)*0.45)]; });
  function hyper(t) {
    const R = Math.min(W, H)*0.45, X = W/2, Y = H/2; const raw = N.map(n => { const p = (typeof P !== 'undefined' && P[n.id]) || { x: 0, y: 0 }; return [p.x/110, -p.y/110]; });
    const f = [focus[0]*0.8, focus[1]*0.8];
    const map = ([x, y]) => { const dx = x - f[0], dy = y - f[1], d = Math.hypot(dx, dy), k = Math.tanh(1.8*d)/(d + 1e-9); return [X + R*dx*k, Y + R*dy*k, 1 - Math.tanh(1.8*d)]; };
    const Q = raw.map(map); cx.strokeStyle = pal(0.5, 0.35); cx.lineWidth = 1.5; cx.beginPath(); cx.arc(X, Y, R, 0, 7); cx.stroke();
    cx.globalCompositeOperation = 'lighter'; cx.lineWidth = 1;
    E.forEach(e => { const p = Q[id2i[e.s]], q = Q[id2i[e.t]]; cx.strokeStyle = pal((p[0] + q[0])/(2*W), 0.2 + 0.5*Math.min(p[2], q[2])); cx.beginPath(); cx.moveTo(p[0], p[1]); cx.lineTo(q[0], q[1]); cx.stroke(); });
    cx.globalCompositeOperation = 'source-over';
    Q.forEach((p, i) => { const c = pal(p[0]/W); glow(c, 8); cx.fillStyle = c; cx.beginPath(); cx.arc(p[0], p[1], 1 + 5*p[2], 0, 7); cx.fill(); if (p[2] > 0.75) text(N[i].id, p[0] + 6, p[1] - 4, c, 11); });
    cap.textContent = 'Hyperbolic view — the whole weave inside a disk; move the mouse to focus: what you look at grows, the rest shrinks toward the rim.';
  }
  // ---- 7. Poincaré disk tiled by SL(2,ℤ): the space τ lives in; vacua i and ρ marked ----
  let tiles = null;
  function modInit() {   // images of the fundamental domain under words in S, T (BFS up to a size cap), as point loops in the upper half plane
    const fd = []; for (let k = 0; k <= 24; k++) { const th = Math.PI/3 + k/24*Math.PI/3; fd.push([Math.cos(th), Math.sin(th)]); } fd.push([-0.5, 12], [0.5, 12]);
    const mob = (m, [x, y]) => { const [a, b, c, d] = m, nr = a*x + b, ni = a*y, dr = c*x + d, di = c*y, q = dr*dr + di*di; return [(nr*dr + ni*di)/q, (ni*dr - nr*di)/q]; };
    const mul = (m, n) => [m[0]*n[0] + m[1]*n[2], m[0]*n[1] + m[1]*n[3], m[2]*n[0] + m[3]*n[2], m[2]*n[1] + m[3]*n[3]];
    const G = [[1, 1, 0, 1], [1, -1, 0, 1], [0, -1, 1, 0]], seen = new Set(), out = [], q = [[[1, 0, 0, 1], 0]];
    const key = m => { let s = m; if (s[0] < 0 || (s[0] === 0 && s[2] < 0)) s = s.map(v => -v); return s.join(','); };
    while (q.length && out.length < 700) { const [m, d] = q.shift(); const k = key(m); if (seen.has(k)) continue; seen.add(k); out.push([fd.map(p => mob(m, p)), d]); if (d < 9) G.forEach(g => q.push([mul(m, g), d + 1])); }
    tiles = out;
  }
  function modular(t) {
    if (!tiles) modInit(); const R = Math.min(W, H)*0.45, X = W/2, Y = H/2, rot = t*0.03;
    const toDisk = ([x, y]) => { const nr = x, ni = y - 1, dr = x, di = y + 1, q = dr*dr + di*di; const u = (nr*dr + ni*di)/q, v = (ni*dr - nr*di)/q; const cr = Math.cos(rot), sr = Math.sin(rot); return [X + R*(u*cr - v*sr), Y - R*(u*sr + v*cr)]; };
    cx.strokeStyle = pal(0.5, 0.5); cx.lineWidth = 1.5; cx.beginPath(); cx.arc(X, Y, R, 0, 7); cx.stroke();
    cx.globalCompositeOperation = 'lighter';
    tiles.forEach(([pts, d]) => { const c = pal(d/9, 0.08 + 0.05*Math.sin(t*1.5 - d)); cx.fillStyle = c; cx.strokeStyle = pal(d/9, 0.55); cx.lineWidth = 0.8; cx.beginPath(); pts.forEach((p, k) => { const q = toDisk(p); k ? cx.lineTo(q[0], q[1]) : cx.moveTo(q[0], q[1]); }); cx.closePath(); cx.fill(); cx.stroke(); });
    cx.globalCompositeOperation = 'source-over';
    const mark = (p, lbl, c, r) => { const q = toDisk(p); glow(c, 18); cx.fillStyle = c; cx.beginPath(); cx.arc(q[0], q[1], r, 0, 7); cx.fill(); text(lbl, q[0] + 8, q[1] - 6, c, 12); };
    mark([0, 1], 'τ = i (saddle in SERAPIS-E)', '#ffffff', 4);
    const pr = 4 + 2*Math.sin(t*3); mark([0.5, Math.sqrt(3)/2], 'τ = ρ — SERAPIS vacuum', pal(1), pr); mark([-0.5, Math.sqrt(3)/2], 'ρ − 1', pal(1), pr*0.7);
    cap.textContent = 'Poincaré disk tiled by SL(2,ℤ) — the space the SERAPIS modulus τ lives in. Every tile is a copy of the fundamental domain; τ = i at the centre, the vacuum at ρ pulses.';
  }
  // ---- 8. E8 Petrie projection: 240 roots in 8 rings of 30, 6720 nearest-neighbour links ----
  function e8(t) {
    const D = window.E8_PETRIE; if (!D) { cap.textContent = 'E8 data missing'; return; }
    const X = W/2, Y = H/2, s = Math.min(W, H)*0.4/1.14, rot = t*0.04, c = Math.cos(rot), sn = Math.sin(rot);
    const pp = D.pts.map(([x, y]) => [X + s*(x*c - y*sn), Y + s*(x*sn + y*c)]); const pulse = (t*0.5) % 8;
    cx.globalCompositeOperation = 'lighter'; cx.lineWidth = 0.5;
    const rings = [...new Set(D.ring)].sort((a, b) => a - b); const ri = D.ring.map(r => rings.indexOf(r));
    D.edges.forEach(([i, j], k) => { if (k % 2) return; const lit = Math.abs(ri[i] - pulse) < 0.6 || Math.abs(ri[j] - pulse) < 0.6; cx.strokeStyle = pal((ri[i] + ri[j])/14, lit ? 0.35 : 0.06); cx.beginPath(); cx.moveTo(...pp[i]); cx.lineTo(...pp[j]); cx.stroke(); });
    cx.globalCompositeOperation = 'source-over';
    pp.forEach((p, i) => { const col = pal(ri[i]/7); glow(col, Math.abs(ri[i] - pulse) < 0.6 ? 16 : 6); cx.fillStyle = col; cx.beginPath(); cx.arc(p[0], p[1], 2.4, 0, 7); cx.fill(); });
    cap.textContent = 'E8 in its Petrie (Coxeter-plane) projection: 240 roots, 8 rings of 30, 30-fold symmetry; every root touches 56 others. A pulse runs ring to ring. E8 holds 1,120 copies of the SERAPIS hexagon (D1294).';
  }
  // ---- 9. Circuit 3D: the four hexagon layers as floating sheets with the up/down wires ----
  function circuit3d(t) {
    const res = window.__circuitLast, L = (res && res.layers) || null, ORDER = ['A2', 'D4', 'E8', 'Leech', '10D'];
    const layout = L || { A2: { string_meter: [0, 0], serapis_e: [1, 0], serapis_point: [0, 1], X_ms: [-1, 1], L_nstar: [-1, 0], L_bridge: [0, -1], inverse_meter: [1, -1] }, D4: { nstar_e: [0, 0], L_reheat: [1, 0], band_e: [0, 1], caps: [-1, 1] }, E8: { wino_window: [0, 0], Q_dt: [1, 0], Q_panel: [0, 1], Q_future: [-1, 1], Q_life: [-1, 0], tests_cmb: [0, -1], G_A2: [1, -1] }, Leech: { X_epstein: [0, 0], X_hexin: [1, 0], X_mod: [0, 1], S_stab: [-1, 1] } };
    const a = t*0.3, ca = Math.cos(a), sa = Math.sin(a), s = Math.min(W, H)/9, pos = {};
    const pj = (x, y, z) => { const X1 = x*ca - y*sa, Y1 = x*sa + y*ca, k = 9/(9 + Y1*0.6); return [W/2 + X1*s*k, H*0.55 - z*s*k + Y1*s*0.35*k, k]; };
    ORDER.forEach((Lr, li) => { const z = li*1.6 - 2.4; const hex = []; for (let k = 0; k <= 6; k++) { const th = k*Math.PI/3; hex.push(pj(2.1*Math.cos(th), 2.1*Math.sin(th), z)); }
      cx.fillStyle = pal(li/3, 0.07); cx.strokeStyle = pal(li/3, 0.6); cx.lineWidth = 1.2; cx.beginPath(); hex.forEach((p, k) => k ? cx.lineTo(p[0], p[1]) : cx.moveTo(p[0], p[1])); cx.fill(); cx.stroke();
      text(Lr + ' layer', hex[0][0] + 10, hex[0][1], pal(li/3), 12);
      Object.entries(layout[Lr] || {}).forEach(([n, [q, r]]) => { pos[n] = pj(Math.sqrt(3)*(q + r/2)*0.8, 1.5*r*0.8, z); }); });
    const okc = ok => ok ? pal(0.15) : '#ff3d8b'; cx.globalCompositeOperation = 'lighter';
    (res?.laws || []).forEach(l => { const p = l.nodes.map(n => pos[n]).filter(Boolean); if (p.length < 2) return; cx.strokeStyle = okc(l.ok); cx.lineWidth = l.kind === 'up' || l.kind === 'down' ? 2 : 1;
      cx.beginPath(); p.forEach((q, k) => k ? cx.lineTo(q[0], q[1]) : cx.moveTo(q[0], q[1])); if (l.kind === 'triangle') cx.closePath(); cx.stroke(); });
    cx.globalCompositeOperation = 'source-over';
    Object.entries(pos).forEach(([n, p]) => { const c = pal((p[0])/W); glow(c, 10); cx.fillStyle = c; cx.beginPath(); cx.arc(p[0], p[1], 4*p[2], 0, 7); cx.fill(); });
    cap.textContent = res ? `SERAPIS circuit in 3D — health ${(res.health*100).toFixed(0)}% (${res.closed}/${res.n_laws} laws). A2 core at the bottom; wires run up the nesting chain.` : 'SERAPIS circuit in 3D — run the circuit (Circuit tab or Derive weave) to light its wires.';
  }
  // ---- 10. resonance spectrogram (+ optional sound) ----
  const spec = []; let audio = null, osc = [];
  soundBtn.onclick = () => { if (audio) { audio.close(); audio = null; osc = []; soundBtn.textContent = 'Sound: off'; return; }
    audio = new (window.AudioContext || window.webkitAudioContext)(); const ms = MODES.modes.filter(m => m.freq > 0).slice(0, 8);
    osc = ms.map((m, k) => { const o = audio.createOscillator(), g = audio.createGain(); o.frequency.value = 110*Math.pow(2, k*7/12) * (1 + m.freq*0.05); g.gain.value = 0; o.connect(g).connect(audio.destination); o.start(); return g; });
    soundBtn.textContent = 'Sound: on'; };
  function spectro(t) {
    const ms = MODES.modes.filter(m => m.freq > 0), mi = Object.fromEntries(MODES.ids.map((k, i) => [k, i]));
    const A = (typeof amp !== 'undefined') ? amp : null;
    const col = ms.map((m, k) => { let s = 0; if (A) for (let i = 0; i < N.length; i++) s += (m.vec[mi[N[i].id]] ?? 0)*A[i]; return Math.abs(s) + 0.25*(1 + Math.sin(t*(1 + m.freq) + k)); });
    spec.push(col); if (spec.length > 120) spec.shift();
    const cw = (W - 80)/120, rh = (H - 60)/ms.length;
    spec.forEach((c, x) => c.forEach((v, k) => { cx.fillStyle = pal(k/(ms.length - 1), Math.min(1, v*0.8), 30 + 35*Math.min(1, v)); cx.fillRect(60 + x*cw, 20 + (ms.length - 1 - k)*rh, cw + 0.5, rh - 1); }));
    ms.forEach((m, k) => text(`mode ${m.k} · ω ${(+m.freq).toFixed(2)}`, 6, 20 + (ms.length - 1 - k)*rh + rh/2, pal(k/(ms.length - 1)), 10));
    if (audio) osc.forEach((g, k) => g.gain.setTargetAtTime(Math.min(0.04, 0.02*(col[k] || 0)), audio.currentTime, 0.1));
    cap.textContent = 'Resonance — the weave’s normal modes as a live waterfall (time → right). Send waves on the Weave tab to excite them; Sound plays each mode as a tone.';
  }
  // ---- 11. history time-lapse (nodes appear in D-note order) ----
  function history(t) {
    const ds = firstD.filter(d => d < 9999), lo = Math.min(...ds), hi = Math.max(...ds), cycle = 24, u = (t % cycle)/(cycle - 3), dNow = lo + (hi - lo)*Math.min(1, u);
    if (!history.b) { const ps = N.map(n => (typeof P !== 'undefined' && P[n.id]) || { x: 0, y: 0 }); history.b = [Math.min(...ps.map(p => p.x)), Math.max(...ps.map(p => p.x)), Math.min(...ps.map(p => p.y)), Math.max(...ps.map(p => p.y))]; }
    const [x0, x1, y0, y1] = history.b;
    const pos = i => { const p = (typeof P !== 'undefined' && P[N[i].id]) || { x: 0, y: 0 }; return [40 + (W - 80)*(p.x - x0)/(x1 - x0 || 1), 50 + (H - 100)*(1 - (p.y - y0)/(y1 - y0 || 1))]; };
    const vis = N.map((n, i) => firstD[i] <= dNow || firstD[i] === 9999 && u >= 1);
    cx.globalCompositeOperation = 'lighter'; cx.lineWidth = 1;
    E.forEach(e => { const a = id2i[e.s], b = id2i[e.t]; if (!vis[a] || !vis[b]) return; const p = pos(a), q = pos(b); cx.strokeStyle = pal(Math.max(firstD[a] === 9999 ? 1 : (firstD[a] - lo)/(hi - lo), 0), 0.45); cx.beginPath(); cx.moveTo(...p); cx.lineTo(...q); cx.stroke(); });
    cx.globalCompositeOperation = 'source-over';
    N.forEach((n, i) => { if (!vis[i]) return; const p = pos(i), fresh = dNow - firstD[i] < (hi - lo)*0.03, c = pal(firstD[i] === 9999 ? 1 : (firstD[i] - lo)/(hi - lo)); glow(c, fresh ? 22 : 6); cx.fillStyle = fresh ? '#fff' : c; cx.beginPath(); cx.arc(p[0], p[1], fresh ? 5 : 2.5, 0, 7); cx.fill(); });
    text(`D${Math.round(dNow)}  ·  ${vis.filter(Boolean).length}/${N.length} nodes`, 16, 28, pal(u), 16);
    cap.textContent = 'History — the weave growing in D-note order (first D-note each node cites); colour = when it appeared. Loops every 24 s.';
  }
  // ---- 12. cymatics (Chladni sand patterns of the plate modes) ----
  let sand = null;
  function cymatics(t) {
    if (!sand || (sand.k !== Math.floor(t/6))) { sand = Array.from({ length: 9000 }, () => [Math.random()*2 - 1, Math.random()*2 - 1]); sand.k = Math.floor(t/6); }
    if (!sand) sand = Array.from({ length: 9000 }, () => [Math.random()*2 - 1, Math.random()*2 - 1]);
    const k = Math.floor(t/6) % 8, pairs = [[1, 2], [2, 3], [1, 4], [3, 4], [2, 5], [3, 5], [4, 5], [3, 7]], [n, m] = pairs[k];
    const f = (x, y) => Math.cos(n*Math.PI*x/2)*Math.cos(m*Math.PI*y/2) - Math.cos(m*Math.PI*x/2)*Math.cos(n*Math.PI*y/2);
    const S = Math.min(W, H)*0.44, X = W/2, Y = H/2;
    for (let it = 0; it < 4; it++) sand.forEach(p => { const a = Math.abs(f(p[0], p[1])); p[0] += (Math.random() - 0.5)*0.2*a; p[1] += (Math.random() - 0.5)*0.2*a; p[0] = Math.max(-1, Math.min(1, p[0])); p[1] = Math.max(-1, Math.min(1, p[1])); });
    cx.strokeStyle = pal(0.5, 0.4); cx.strokeRect(X - S, Y - S, 2*S, 2*S);
    sand.forEach(p => { const u = (p[0] + 1)/2; cx.fillStyle = pal(u, 0.85); cx.fillRect(X + p[0]*S, Y + p[1]*S, 1.6, 1.6); });
    text(`plate mode (${n}, ${m}) — weave resonance mode ${MODES.modes[k % MODES.modes.length]?.k ?? k}`, 16, 28, pal(0.5), 14);
    cap.textContent = 'Cymatics — sand on a vibrating plate settles on the still lines (Chladni figures). The pattern steps through eight modes, one every 6 s.';
  }
  // ---- 13. sky map (Hyperion orbits from the Mapper, Mollweide; loads from the app) ----
  let sky = null, skyAsked = false;
  function sky_(t) {
    const X = W/2, Y = H/2, A = 0.95*Math.min(W/(4*Math.SQRT2), H/(2*Math.SQRT2)), moll = (l, b) => { let th = b; for (let i = 0; i < 8; i++) th -= (2*th + Math.sin(2*th) - Math.PI*Math.sin(b))/(2 + 2*Math.cos(2*th) + 1e-9); const L = ((l + 180) % 360 + 360) % 360 - 180; return [X - A*(2*Math.SQRT2/Math.PI)*(L*Math.PI/180)*Math.cos(th), Y - A*Math.SQRT2*Math.sin(th)]; };
    cx.strokeStyle = pal(0.5, 0.25); cx.lineWidth = 1;
    for (let b = -60; b <= 60; b += 30) { cx.beginPath(); for (let l = -180; l <= 180; l += 5) { const p = moll(l, b*Math.PI/180); l === -180 ? cx.moveTo(...p) : cx.lineTo(...p); } cx.stroke(); }
    for (let l = -180; l <= 180; l += 60) { cx.beginPath(); for (let b = -90; b <= 90; b += 5) { const p = moll(l, b*Math.PI/180); b === -90 ? cx.moveTo(...p) : cx.lineTo(...p); } cx.stroke(); }
    if (!sky && !skyAsked && window.pywebview?.api?.sky_sample) { skyAsked = true; window.pywebview.api.sky_sample(30000).then(r => { sky = r; }).catch(() => {}); }
    if (sky && sky.stars) { cx.globalCompositeOperation = 'lighter'; sky.stars.forEach(([l, b, e]) => { const p = moll(l, b*Math.PI/180); cx.fillStyle = pal(Math.min(1, e/0.6), 0.6); cx.fillRect(p[0], p[1], 1.4, 1.4); }); cx.globalCompositeOperation = 'source-over';
      cap.textContent = `Sky map — ${sky.stars.length.toLocaleString()} Hyperion orbits (sampled from ${sky.tiles} tiles, ${sky.model}), Galactic Mollweide, colour = orbital eccentricity (0 → 0.6+).`; }
    else cap.textContent = window.pywebview ? 'Sky map — loading the Mapper’s Hyperion orbits…' : 'Sky map — open in the Janus app to load the Mapper’s Hyperion orbits (Galactic Mollweide, colour = eccentricity).';
  }
  const DRAW = { bundle, chord, hive, force, arc: arcflow, hyper, modular, e8, circuit3d, spectro, history, cymatics, sky: sky_ };
  function reset() { F = null; sand = null; spec.length = 0; t0 = performance.now(); }
  function loop(now) { requestAnimationFrame(loop); if (box.hidden) return; if (cv.clientWidth !== Math.round(W) || cv.clientHeight !== Math.round(H)) size();
    clear(); cx.save(); try { DRAW[cur]((now - t0)/1000); } catch (e) { cap.textContent = 'display error: ' + e; } cx.restore(); cx.shadowBlur = 0; }
  requestAnimationFrame(loop);
  function show(on) { box.hidden = !on; tab.setAttribute('aria-selected', String(on)); if (on) { document.querySelectorAll('.tabs .tab').forEach(t => { if (t !== tab) t.setAttribute('aria-selected', 'false'); }); size(); mark(); } else if (audio) soundBtn.onclick(); }
  tab.addEventListener('click', () => show(true));
  document.querySelectorAll('.tabs .tab').forEach(t => { if (t !== tab) t.addEventListener('click', () => show(false)); });
  if (!DRAW[cur]) cur = 'bundle';
})();
