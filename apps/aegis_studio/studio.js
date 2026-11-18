/* AEGIS Studio — neon weave of the AEGIS web (three.js + bloom), real waves, resonance modes, SERAPIS-E landscape and knobs.
   Data: window.AEGIS (data.js snapshot of docs/web/*.json). Live engine: window.pywebview.api (app.py) when running as the desktop app. */
'use strict';
const D = window.AEGIS; const WEB = D.web, MODES = D.modes, LAND = D.landscape, GRID = D.grid;
const C = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const LANE = {left: {c: '--cyan', name: 'Left string · early universe'}, centre: {c: '--violet', name: 'Centre · shared'}, right: {c: '--amber', name: 'Right string · late universe'},
  theory: {c: '--lime', name: 'Theory map'}, janus: {c: '--magenta', name: 'Toolkits · Janus · Chronos · Hyperion'}, strings: {c: '--yellow', name: 'SERAPIS string sector'}};
const col = k => new THREE.Color(C(LANE[k].c));
const ids = WEB.nodes.map(n => n.id), ix = Object.fromEntries(ids.map((k, i) => [k, i])), NN = ids.length;
const byId = Object.fromEntries(WEB.nodes.map(n => [n.id, n]));
// ---------- layout: everything flows left → right ----------
const P = {}; (() => {
  const rows = {left: 34, centre: 34, right: 34, theory: 6, janus: -22, strings: -42};
  const xr = {left: [-92, -38], centre: [-22, 22], right: [38, 92]};
  const lanes = {}; WEB.nodes.forEach(n => (lanes[n.lane] ||= []).push(n));
  for (const [ln, arr] of Object.entries(lanes)) arr.forEach((n, i) => {
    let x, y = rows[ln];
    if (xr[ln]) { const [a, b] = xr[ln]; x = arr.length > 1 ? a + (b - a)*i/(arr.length - 1) : (a + b)/2; y += (i % 2 ? 5 : -5); }
    else if (ln === 'theory') { const tn = WEB.layers?.[n.id]; const layer = n.layer || 1; x = -90 + (layer - 1)*45 + ((i*37) % 30) - 15; y += ((i*13) % 24) - 12; }
    else { x = -95 + 190*i/Math.max(1, arr.length - 1); y += (i % 3 - 1)*5; }
    P[n.id] = new THREE.Vector3(x, y, 0);
  });
})();
// ---------- renderer / scene ----------
const canvas = document.getElementById('gl'), stage = document.getElementById('stage');
const renderer = new THREE.WebGLRenderer({canvas, antialias: true, powerPreference: 'high-performance'}); renderer.setPixelRatio(Math.min(2, devicePixelRatio));
const scene = new THREE.Scene(); scene.background = new THREE.Color(C('--bg'));
const persp = new THREE.PerspectiveCamera(45, 1, 0.1, 2000); persp.position.set(0, -150, 120);
const ortho = new THREE.OrthographicCamera(-110, 110, 70, -70, -500, 500); ortho.position.set(0, 0, 200);
let cam = persp; const ctl = new THREE.OrbitControls(persp, canvas); ctl.enableDamping = true; ctl.target.set(0, -2, 0); ctl.addEventListener('start', () => ctl._userActive = true); ctl.addEventListener('end', () => setTimeout(() => ctl._userActive = false, 4000));
const composer = new THREE.EffectComposer(renderer); const rpass = new THREE.RenderPass(scene, cam); composer.addPass(rpass);
const bloom = new THREE.UnrealBloomPass(new THREE.Vector2(512, 512), 1.25, 0.55, 0.05); composer.addPass(bloom);
function resize() { const w = stage.clientWidth, h = stage.clientHeight - 170; renderer.setSize(w, h, false); composer.setSize(w, h); persp.aspect = w/h; persp.updateProjectionMatrix();
  const a = w/h; ortho.left = -75*a; ortho.right = 75*a; ortho.top = 75; ortho.bottom = -75; ortho.updateProjectionMatrix(); }
addEventListener('resize', resize);
const weave = new THREE.Group(), land = new THREE.Group(); scene.add(weave, land); land.visible = false;
// ---------- wave field ----------
let knobsReady = false; let marker = null; const scope = document.getElementById('scope'), sx = scope.getContext('2d'); const scopeBuf = new Float32Array(320); let sp = 0;
const amp = new Float32Array(NN); const sigma2 = 14*14; let gain = 1, speed = 1, damp = 0.35, bloomK = 1.25;
let tNow = 0; const ambient = (x, y) => 1.4*Math.sin(0.06*x - 0.9*tNow*speed) * Math.cos(0.08*y + 0.35*tNow*speed);
function field(x, y) { let s = ambient(x, y); for (let i = 0; i < NN; i++) { const a = amp[i]; if (a > -1e-3 && a < 1e-3) continue; const p = P[ids[i]]; const dx = x - p.x, dy = y - p.y; s += a*Math.exp(-(dx*dx + dy*dy)/sigma2); } return s; }
// ---------- fabric (warp left→right, weft top→bottom) ----------
const fabric = []; (() => {
  const mk = (pts, colors) => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(pts.length*3), 3)); g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(colors), 3));
    const l = new THREE.Line(g, new THREE.LineBasicMaterial({vertexColors: true, transparent: true, opacity: 0.32, blending: THREE.AdditiveBlending, depthWrite: false})); l.userData.base = pts; weave.add(l); fabric.push(l); };
  for (let j = 0; j < 46; j++) { const y = -58 + j*2.5; const pts = [], cs = []; const c = new THREE.Color().setHSL(0.57 + 0.36*Math.pow(j/45, 1.3), 1, 0.58);
    for (let i = 0; i <= 160; i++) { const x = -105 + 210*i/160; pts.push([x, y + 0.9*Math.sin(i*0.9 + j)]); cs.push(c.r, c.g, c.b); } mk(pts, cs); }
  for (let i = 0; i < 70; i++) { const x = -105 + 210*i/69; const pts = [], cs = []; const c = new THREE.Color().setHSL(0.57 + 0.36*Math.pow(i/69, 1.3), 1, 0.5);
    for (let j = 0; j <= 90; j++) { const y = -58 + 113*j/90; pts.push([x + 0.9*Math.sin(j*0.9 + i), y]); cs.push(c.r, c.g, c.b); } mk(pts, cs); }
})();
// ---------- threads (the web's links) ----------
const threads = WEB.edges.map((e, k) => { const a = P[e.s], b = P[e.t]; const mid = a.clone().add(b).multiplyScalar(0.5); mid.z += 6 + (k % 5); mid.y += ((k*7) % 9) - 4;
  const curve = new THREE.QuadraticBezierCurve3(a.clone(), mid, b.clone()); const base = curve.getPoints(64);
  const g = new THREE.BufferGeometry().setFromPoints(base); const xm = (a.x + b.x)/2; const c = e.sign < 0 ? new THREE.Color(C('--red')) : new THREE.Color().setHSL(0.57 + 0.36*Math.pow(Math.min(1, Math.max(0, (xm + 100)/200)), 1.3), 1, 0.62);
  const l = new THREE.Line(g, new THREE.LineBasicMaterial({color: c, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending, depthWrite: false})); weave.add(l);
  return {e, l, base, c}; });
// particles running along threads
const NP = threads.length*2; const pg = new THREE.BufferGeometry(); pg.setAttribute('position', new THREE.BufferAttribute(new Float32Array(NP*3), 3)); pg.setAttribute('color', new THREE.BufferAttribute(new Float32Array(NP*3), 3));
const pts = new THREE.Points(pg, new THREE.PointsMaterial({size: 2.2, vertexColors: true, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false})); weave.add(pts);
// ---------- knobs (nodes) ----------
const deg = new Array(NN).fill(0); WEB.edges.forEach(e => { deg[ix[e.s]]++; deg[ix[e.t]]++; });
const knobs = WEB.nodes.map((n, i) => { const g = new THREE.Group(); const c = col(n.lane); const r = 0.75 + 0.14*Math.sqrt(deg[i]);
  const core = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), new THREE.MeshBasicMaterial({color: c})); g.add(core);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(r*1.8, 0.09, 8, 40), new THREE.MeshBasicMaterial({color: c, transparent: true, opacity: n.status === 'open' ? 0.9 : 0.45}));
  if (n.status === 'killed') core.material.color.multiplyScalar(0.3); g.add(ring); g.position.copy(P[n.id]); g.userData = {id: n.id, core, ring, r}; weave.add(g); return g; });
// ---------- HUD ----------
const hud = document.getElementById('hud'); Object.values(LANE).forEach(L => { const d = document.createElement('div'); d.className = 'lane'; d.style.color = C(L.c); d.textContent = L.name; hud.appendChild(d); });
// ---------- wave engine (same model as tools/web/waves.py) ----------
const gate = WEB.nodes.map(n => ({killed: 0.1, frozen: 0.5})[n.status] ?? 1); const S = Array.from({length: NN}, () => new Float64Array(NN));
WEB.edges.forEach(e => { const a = ix[e.s], b = ix[e.t]; S[b][a] += e.sign; S[a][b] += 0.5*e.sign; });
const adj = Array.from({length: NN}, () => []); WEB.edges.forEach(e => { adj[ix[e.s]].push(ix[e.t]); adj[ix[e.t]].push(ix[e.s]); });
function response(src, sgn) { let x = new Float64Array(NN); const e0 = new Float64Array(NN); e0[ix[src]] = sgn; x.set(e0);
  for (let t = 0; t < 80; t++) { const y = new Float64Array(NN); for (let i = 0; i < NN; i++) { let s = 0; const r = S[i]; for (let j = 0; j < NN; j++) if (r[j]) s += r[j]*x[j]; y[i] = e0[i] + D.waves.alpha*gate[i]*s; } x = y; } return x; }
function hops(src) { const d = new Array(NN).fill(99); const q = [ix[src]]; d[ix[src]] = 0; while (q.length) { const u = q.shift(); for (const v of adj[u]) if (d[v] > d[u] + 1) { d[v] = d[u] + 1; q.push(v); } } return d; }
let waves = []; // {r, d, t0, sgn}
let modeOn = null; // resonance mode index
function sendWave(sgn) { if (!sel) return; waves.push({r: response(sel, sgn), d: hops(sel), t0: performance.now()/1000, src: sel}); }
// ---------- selection ----------
let sel = null; const ray = new THREE.Raycaster(); const mouse = new THREE.Vector2();
canvas.addEventListener('click', ev => { const b = canvas.getBoundingClientRect(); mouse.set(((ev.clientX - b.left)/b.width)*2 - 1, -((ev.clientY - b.top)/b.height)*2 + 1);
  ray.setFromCamera(mouse, cam); const hit = ray.intersectObjects(knobs.map(k => k.userData.core))[0]; if (hit) select(hit.object.parent.userData.id); });
function select(id) { sel = id; ['bplus', 'bminus'].forEach(b => document.getElementById(b).disabled = false); const n = byId[id];
  const box = document.getElementById('info'); box.querySelector('.small') && (box.querySelector('.small').textContent = '');
  let t = box.querySelector('.t'); if (!t) { t = document.createElement('div'); t.className = 't'; box.insertBefore(t, box.querySelector('#links')); }
  t.textContent = `${n.label}  [${n.status}]`; const ul = document.getElementById('links'); ul.innerHTML = '';
  const src = document.createElement('li'); src.textContent = 'Sources: ' + (n.refs || '—'); ul.appendChild(src);
  WEB.edges.filter(e => e.s === id || e.t === id).forEach(e => { const li = document.createElement('li'); li.className = e.sign < 0 ? 'neg' : 'pos';
    li.textContent = `${e.s === id ? '→' : '←'} ${e.s === id ? e.t : e.s} · ${e.kind}${e.sign < 0 ? ' (tension)' : ''} · ${e.ref}${e.verdict ? ' · ' + e.verdict : ''}`; ul.appendChild(li); });
  document.getElementById('scopecap').textContent = 'node: ' + id; scopeBuf.fill(0); }
// ---------- knobs UI ----------
function makeKnob(host, o) { const w = document.createElement('div'); w.className = 'knob'; w.tabIndex = 0; w.setAttribute('role', 'slider'); w.setAttribute('aria-label', o.label);
  w.innerHTML = `<svg viewBox="0 0 80 80"><circle cx="40" cy="40" r="30" fill="#0a0418" stroke="${C('--line')}" stroke-width="2"/><path class="arc" fill="none" stroke="${o.color}" stroke-width="5" stroke-linecap="round" style="filter:drop-shadow(0 0 4px ${o.color})"/><line class="ptr" x1="40" y1="40" x2="40" y2="16" stroke="${C('--fg')}" stroke-width="3" stroke-linecap="round"/></svg><div class="lbl"></div><div class="val"></div>`;
  w.querySelector('.lbl').textContent = o.label; host.appendChild(w); let v = o.value;
  const draw = () => { const f = (v - o.min)/(o.max - o.min); const a0 = -135, a = a0 + 270*f; const rad = d => (d - 90)*Math.PI/180;
    const p = d => `${40 + 34*Math.cos(rad(d))} ${40 + 34*Math.sin(rad(d))}`; w.querySelector('.arc').setAttribute('d', `M ${p(a0)} A 34 34 0 ${a - a0 > 180 ? 1 : 0} 1 ${p(a)}`);
    w.querySelector('.ptr').setAttribute('transform', `rotate(${a} 40 40)`); w.querySelector('.val').textContent = o.fmt(v); w.setAttribute('aria-valuenow', v); };
  const set = nv => { v = Math.min(o.max, Math.max(o.min, Math.round(nv/o.step)*o.step)); draw(); o.on(v); };
  let drag = null; w.addEventListener('pointerdown', e => { drag = [e.clientY, v]; w.setPointerCapture(e.pointerId); });
  w.addEventListener('pointermove', e => { if (drag) set(drag[1] + (drag[0] - e.clientY)*(o.max - o.min)/180); }); w.addEventListener('pointerup', () => drag = null);
  w.addEventListener('wheel', e => { e.preventDefault(); set(v - Math.sign(e.deltaY)*o.step); }, {passive: false});
  w.addEventListener('keydown', e => { if (e.key === 'ArrowUp' || e.key === 'ArrowRight') set(v + o.step); if (e.key === 'ArrowDown' || e.key === 'ArrowLeft') set(v - o.step); });
  draw(); o.on(v); return {get: () => v, set}; }
const K = {}; const kh = document.getElementById('knobs');
K.N = makeKnob(kh, {label: 'N*', min: 45, max: 65, step: 0.5, value: 50, color: C('--cyan'), fmt: v => v.toFixed(1), on: () => readout()});
K.C = makeKnob(kh, {label: 'BHK C ×', min: 0, max: 3, step: 0.05, value: 1, color: C('--yellow'), fmt: v => v.toFixed(2), on: () => { readout(); landMarker(); }});
K.G = makeKnob(kh, {label: 'Wave gain', min: 0.2, max: 3, step: 0.1, value: 1, color: C('--teal'), fmt: v => v.toFixed(1), on: v => gain = v});
K.S = makeKnob(kh, {label: 'Speed', min: 0.2, max: 3, step: 0.1, value: 1, color: C('--magenta'), fmt: v => v.toFixed(1), on: v => speed = v});
K.Dm = makeKnob(kh, {label: 'Damping', min: 0.05, max: 1.5, step: 0.05, value: 0.35, color: C('--amber'), fmt: v => v.toFixed(2), on: v => damp = v});
K.B = makeKnob(kh, {label: 'Glow', min: 0, max: 3, step: 0.05, value: 1.25, color: C('--violet'), fmt: v => v.toFixed(2), on: v => { bloomK = v; bloom.strength = v; }});
knobsReady = true;
// ---------- readout from the Janus grid (bilinear), exact on demand ----------
function interp(arr) { const cf = K.C.get(), ns = K.N.get(); const Cs = GRID.Cfac, Ns = GRID.Nstar; let i = Math.min(Cs.length - 2, Math.max(0, Cs.findIndex((c, k) => k < Cs.length - 1 && cf <= Cs[k + 1])));
  let j = Math.min(Ns.length - 2, Math.max(0, Ns.findIndex((c, k) => k < Ns.length - 1 && ns <= Ns[k + 1]))); const u = (cf - Cs[i])/(Cs[i + 1] - Cs[i]), w = (ns - Ns[j])/(Ns[j + 1] - Ns[j]);
  const g = (a, b) => arr[a]?.[b]; const v = [g(i, j), g(i + 1, j), g(i, j + 1), g(i + 1, j + 1)]; if (v.some(x => x == null)) return null;
  return (1 - u)*(1 - w)*v[0] + u*(1 - w)*v[1] + (1 - u)*w*v[2] + u*w*v[3]; }

function readout(exact) { if (!knobsReady) return; const ns = exact ? exact.ns : (GRID ? interp(GRID.ns) : null), r = exact ? exact.r : (GRID ? interp(GRID.r) : null), a = exact ? exact.alpha_s : (GRID ? interp(GRID.alpha_s) : null);
  document.getElementById('rns').textContent = ns == null ? '—' : ns.toFixed(5); document.getElementById('rr').textContent = r == null ? '—' : r.toExponential(2);
  document.getElementById('ra').textContent = a == null ? '—' : a.toExponential(2); document.getElementById('rsrc').textContent = exact ? `exact (Janus core, live) at N* ${K.N.get()}, C ×${K.C.get()}` : 'grid: Janus core on SERAPIS-E (interpolated)';
  const band = document.getElementById('bandns'); band.innerHTML = ''; const lo = 0.955, hi = 0.985, X = v => `${(v - lo)/(hi - lo)*100}%`;
  for (const [m, s, c] of [[0.9684, 0.0030, 'rgba(0,229,255,.35)'], [0.9728, 0.0027, 'rgba(255,43,214,.35)']]) { const i = document.createElement('i'); i.style.left = X(m - s); i.style.width = `${2*s/(hi - lo)*100}%`; i.style.background = c; band.appendChild(i); }
  if (ns != null) { const mk = document.createElement('div'); mk.className = 'mk'; mk.style.left = X(ns); band.appendChild(mk); } }
document.getElementById('bexact').onclick = async () => { const api = window.pywebview?.api; if (!api) { document.getElementById('rsrc').textContent = 'live engine only in the desktop app'; return; }
  document.getElementById('rsrc').textContent = 'computing…'; try { readout(await api.recompute(K.N.get(), K.C.get())); } catch (e) { document.getElementById('rsrc').textContent = 'engine error: ' + e; } };
// ---------- landscape ----------
(() => { if (!LAND) return; const nx = LAND.phi.length, ny = LAND.C.length; const g = new THREE.PlaneGeometry(160, 100, nx - 1, ny - 1); const pos = g.attributes.position; const cols = [];
  let mn = Infinity, mx = -Infinity; LAND.V.forEach(r => r.forEach(v => { mn = Math.min(mn, v); mx = Math.max(mx, v); }));
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const k = j*nx + i; const v = LAND.V[j][i]; const h = (v - mn)/(mx - mn + 1e-12); pos.setZ(k, 55*h); const c = new THREE.Color().setHSL(0.57 + 0.36*Math.pow(h, 1.3), 1, 0.42 + 0.2*h); cols.push(c.r, c.g, c.b); }
  g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3)); g.computeVertexNormals();
  land.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({vertexColors: true, transparent: true, opacity: 0.28, side: THREE.DoubleSide})));
  land.add(new THREE.LineSegments(new THREE.WireframeGeometry(g), new THREE.LineBasicMaterial({vertexColors: true, transparent: true, opacity: 0.55})));
  marker = new THREE.Mesh(new THREE.BoxGeometry(160, 0.8, 2), new THREE.MeshBasicMaterial({color: C('--yellow')})); land.add(marker); })();
function landMarker() { if (!marker || !K.C) return; const f = K.C.get()/3; marker.position.set(0, -50 + 100*f, 58); }
// ---------- scope ----------
function drawScope() { sx.fillStyle = '#05010f'; sx.fillRect(0, 0, scope.width, scope.height); sx.strokeStyle = 'rgba(160,140,255,.18)'; sx.lineWidth = 1;
  for (let y = 0; y <= 4; y++) { sx.beginPath(); sx.moveTo(0, y*50); sx.lineTo(scope.width, y*50); sx.stroke(); }
  sx.strokeStyle = C('--teal'); sx.shadowColor = C('--teal'); sx.shadowBlur = 10; sx.lineWidth = 2.5; sx.beginPath();
  for (let i = 0; i < scopeBuf.length; i++) { const v = scopeBuf[(sp + i) % scopeBuf.length]; const x = i/(scopeBuf.length - 1)*scope.width, y = 100 - 90*Math.tanh(2*v); i ? sx.lineTo(x, y) : sx.moveTo(x, y); }
  sx.stroke(); sx.shadowBlur = 0; }
// ---------- view switching ----------
const tabs = {weave: 't-weave', land: 't-land', classic: 't-classic'}; let view = 'weave';
function setView(v) { if (v === 'classic') { const api = window.pywebview?.api; if (api) api.open_classic(); else open('classic.html', '_blank'); return; }
  view = v; Object.entries(tabs).forEach(([k, id]) => document.getElementById(id).setAttribute('aria-selected', String(k === v))); weave.visible = v === 'weave'; land.visible = v === 'land';
  document.getElementById('hud').hidden = v !== 'weave'; bloom.strength = v === 'land' ? Math.min(bloomK, 0.55) : bloomK; if (v === 'land') { setCam(true); persp.position.set(-40, -200, 150); ctl.target.set(0, 0, 20); } else { persp.position.set(0, -150, 120); ctl.target.set(0, -2, 0); } }
Object.entries(tabs).forEach(([k, id]) => document.getElementById(id).onclick = () => setView(k));
function setCam(three) { cam = three ? persp : ortho; rpass.camera = cam; ctl.enabled = three; document.getElementById('b3d').classList.toggle('on', three); document.getElementById('b2d').classList.toggle('on', !three); }
document.getElementById('b3d').onclick = () => setCam(true); document.getElementById('b2d').onclick = () => setCam(false);
document.getElementById('bplus').onclick = () => sendWave(1); document.getElementById('bminus').onclick = () => sendWave(-1);
document.getElementById('bclear').onclick = () => { waves = []; modeOn = null; amp.fill(0); document.getElementById('bmode').textContent = 'Resonance mode'; };
document.getElementById('bmode').onclick = () => { const ms = MODES.modes.filter(m => m.freq > 0); const k = modeOn == null ? 0 : (ms.findIndex(m => m.k === modeOn.k) + 1) % ms.length; modeOn = ms[k];
  document.getElementById('bmode').textContent = `Mode ${modeOn.k} · ω ${modeOn.freq}`; };
// ---------- frame loop ----------
let last = performance.now(), frames = 0, fpsT = last;
function frame(now) { requestAnimationFrame(frame); const t = now/1000; tNow = t; const dt = Math.min(0.05, (now - last)/1000); last = now;
  amp.fill(0);
  waves = waves.filter(w => t - w.t0 < 12/speed);
  for (const w of waves) { const age = (t - w.t0)*speed; for (let i = 0; i < NN; i++) { const r = w.r[i]; if (Math.abs(r) < 1e-3) continue; const ta = age - 0.45*w.d[i];
      if (ta < 0) continue; amp[i] += gain*8*r*Math.exp(-damp*ta)*Math.cos(5*ta); } }
  if (modeOn) { const ph = Math.sin(t*(1.5 + 4*modeOn.freq)*speed); const mi = Object.fromEntries(MODES.ids.map((k, i) => [k, i])); for (let i = 0; i < NN; i++) amp[i] += gain*6*(modeOn.vec[mi[ids[i]]] ?? 0)*ph; }
  if (view === 'weave') {
    const twoD = cam === ortho;
    for (const l of fabric) { const pa = l.geometry.attributes.position, b = l.userData.base; for (let k = 0; k < b.length; k++) { const [x, y] = b[k]; const f = field(x, y); pa.setXYZ(k, x, y + (twoD ? f*0.8 : 0), twoD ? 0 : f); } pa.needsUpdate = true;
      l.material.opacity = 0.22 + Math.min(0.5, 0.0); }
    threads.forEach(th => { const pa = th.l.geometry.attributes.position; th.base.forEach((p, k) => { const f = field(p.x, p.y); pa.setXYZ(k, p.x, p.y + (twoD ? f*0.8 : 0), twoD ? 0 : p.z + f); }); pa.needsUpdate = true; });
    const pp = pg.attributes.position, pc = pg.attributes.color; threads.forEach((th, k) => { for (let q = 0; q < 2; q++) { const u = ((t*0.25*speed + k*0.137 + q*0.5) % 1); const idx = Math.floor(u*64); const p = th.l.geometry.attributes.position;
      pp.setXYZ(2*k + q, p.getX(idx), p.getY(idx), p.getZ(idx) + 0.4); pc.setXYZ(2*k + q, th.c.r, th.c.g, th.c.b); } }); pp.needsUpdate = true; pc.needsUpdate = true;
    knobs.forEach((g, i) => { const a = amp[i]; const p = P[ids[i]]; g.position.set(p.x, p.y + (twoD ? a*0.8 : 0), twoD ? 0 : a); const s = 1 + Math.min(1.2, Math.abs(a)*0.2) + (ids[i] === sel ? 0.35 + 0.15*Math.sin(t*6) : 0);
      g.scale.setScalar(s); g.userData.ring.rotation.z = t*(0.3 + 0.1*(i % 5)); g.userData.ring.material.color.set(a > 0.05 ? C('--teal') : a < -0.05 ? C('--red') : C(LANE[byId[ids[i]].lane].c)); });
  } else { land.rotation.z = t*0.05; }
  if (sel) { scopeBuf[sp] = amp[ix[sel]]/8; sp = (sp + 1) % scopeBuf.length; } drawScope();
  if (cam === persp) { if (!ctl._userActive && view === 'weave') { const r = Math.hypot(persp.position.x, persp.position.y); const a = Math.atan2(persp.position.y, persp.position.x) + 0.0006*speed; persp.position.x = r*Math.cos(a); persp.position.y = r*Math.sin(a); } ctl.update(); } composer.render(dt);
  frames++; if (now - fpsT > 1000) { document.getElementById('fps').textContent = `${frames} fps`; frames = 0; fpsT = now; } }
resize(); setView('weave'); readout(); landMarker(); requestAnimationFrame(frame);
addEventListener('pywebviewready', () => { const e = document.getElementById('engine'); e.textContent = 'engine: live (Python)'; e.classList.add('live'); });

// ---------- top strip: geometric shapes forming from the strings ----------
(() => { const cv = document.getElementById('shapes'), cx = cv.getContext('2d'); let W2 = 0, H2 = 0;
  const fit = () => { const r = devicePixelRatio || 1; W2 = cv.clientWidth; H2 = cv.clientHeight; cv.width = W2*r; cv.height = H2*r; cx.setTransform(r, 0, 0, r, 0, 0); }; addEventListener('resize', fit); fit();
  const cpow = (re, im, e) => { const r = Math.hypot(re, im), a = Math.atan2(im, re); const rr = Math.pow(r, e); return [rr*Math.cos(a*e), rr*Math.sin(a*e)]; };
  function calabiYau(n, al) { const L = []; for (let k1 = 0; k1 < n; k1++) for (let k2 = 0; k2 < n; k2++) for (let a = 0; a <= 8; a++) { const xi = -1 + 2*a/8; const line = [];
      for (let b = 0; b <= 16; b++) { const th = (Math.PI/2)*b/16; const ch = [Math.cosh(xi)*Math.cos(th), Math.sinh(xi)*Math.sin(th)], sh = [Math.sinh(xi)*Math.cos(th), Math.cosh(xi)*Math.sin(th)];
        let z1 = cpow(ch[0], ch[1], 2/n), z2 = cpow(sh[1], -sh[0], 2/n); const p1 = 2*Math.PI*k1/n, p2 = 2*Math.PI*k2/n;   // −i·sinh = (Im, −Re)
        z1 = [z1[0]*Math.cos(p1) - z1[1]*Math.sin(p1), z1[0]*Math.sin(p1) + z1[1]*Math.cos(p1)]; z2 = [z2[0]*Math.cos(p2) - z2[1]*Math.sin(p2), z2[0]*Math.sin(p2) + z2[1]*Math.cos(p2)];
        line.push([z1[0], z2[0], Math.cos(al)*z1[1] + Math.sin(al)*z2[1]]); } L.push(line); } return L; }
  function torusKnot(p, q) { const line = []; for (let i = 0; i <= 600; i++) { const t = 2*Math.PI*i/600; const r = 0.7 + 0.3*Math.cos(q*t); line.push([r*Math.cos(p*t), r*Math.sin(p*t), 0.3*Math.sin(q*t)]); } return [line]; }
  function cliffordTorus(m) { const L = []; for (let a = 0; a < 18; a++) { const line = []; const u = 2*Math.PI*a/18; for (let b = 0; b <= 48; b++) { const v = 2*Math.PI*b/48;
      const x4 = [Math.cos(u), Math.sin(u), Math.cos(v + m*u), Math.sin(v + m*u)].map(c => c/Math.SQRT2); const w = 1.6 - x4[3]; line.push([x4[0]/w*1.6, x4[1]/w*1.6, x4[2]/w*1.6]); } L.push(line); } return L; }
  function lissajous(a, b, c) { const line = []; for (let i = 0; i <= 700; i++) { const t = 2*Math.PI*i/700; line.push([Math.sin(a*t + 0.5), Math.sin(b*t), Math.sin(c*t + 1.1)].map(v => 0.85*v)); } return [line]; }
  const hue = f => `hsl(${(0.57 + 0.36*Math.pow(f, 1.3))*360} 100% 62%)`;
  let shapes = []; let cycle = -1;
  function rebuild(k) { const m = modeOn ? modeOn.k : (k % 5) + 1; shapes = [
      {name: `Calabi–Yau slice n=${3 + (k % 3)}`, L: calabiYau(3 + (k % 3), 0.6), f: 0.05},
      {name: `torus knot (${2 + (m % 3)}, ${3 + (m % 4)})`, L: torusKnot(2 + (m % 3), 3 + (m % 4)), f: 0.30},
      {name: `Clifford torus twist ${1 + (k % 3)}`, L: cliffordTorus(1 + (k % 3)), f: 0.62},
      {name: `Lissajous ${1 + (m % 3)}:${2 + (k % 3)}:${3 + (m % 2)}`, L: lissajous(1 + (m % 3), 2 + (k % 3), 3 + (m % 2)), f: 0.92}];
    shapes.forEach(sh => { let R = 1e-9; sh.L.forEach(l => l.forEach(p => R = Math.max(R, Math.hypot(...p)))); sh.L = sh.L.map(l => l.map(p => p.map(v => v/R))); }); }
  function frameS(now) { requestAnimationFrame(frameS); const t = now/1000; const T = 9/(speed || 1); const k = Math.floor(t/T); const prog = (t % T)/T;
    if (k !== cycle) { cycle = k; rebuild(k); }
    let energy = 0; for (let i = 0; i < NN; i++) energy += Math.abs(amp[i]); energy = Math.min(1, energy/40);
    cx.clearRect(0, 0, W2, H2); cx.globalCompositeOperation = 'lighter'; const n = shapes.length, cw = W2/n;
    shapes.forEach((sh, si) => { const cxm = cw*(si + 0.5), cym = H2/2 + 6, sc = Math.min(cw, H2 - 34)*0.42*(1 + 0.06*energy); const ry = t*0.4 + si, rx = 0.5 + 0.2*Math.sin(t*0.3 + si);
      const grow = Math.min(1, prog*1.25 + energy*0.3); const fade = prog > 0.88 ? 1 - (prog - 0.88)/0.12 : 1;
      const total = sh.L.reduce((a, l) => a + l.length, 0); let budget = Math.floor(total*grow);
      cx.lineWidth = 1.1; cx.shadowBlur = 10;
      sh.L.forEach((line, li) => { if (budget <= 0) return; const nseg = Math.min(line.length, budget); budget -= nseg; const c = hue((sh.f + 0.25*li/sh.L.length) % 1);
        cx.strokeStyle = c; cx.shadowColor = c; cx.globalAlpha = 0.75*fade; cx.beginPath();
        for (let i = 0; i < nseg; i++) { let [x, y, z] = line[i]; const x1 = x*Math.cos(ry) + z*Math.sin(ry), z1 = -x*Math.sin(ry) + z*Math.cos(ry); const y1 = y*Math.cos(rx) - z1*Math.sin(rx);
          const px = cxm + sc*x1, py = cym + sc*y1; i ? cx.lineTo(px, py) : cx.moveTo(px, py); } cx.stroke(); });
      cx.globalAlpha = 0.85; cx.shadowBlur = 0; cx.fillStyle = hue(sh.f); cx.font = '600 10px Bahnschrift, Segoe UI, sans-serif'; cx.fillText(sh.name.toUpperCase(), cxm - cw*0.45, 16); });
    cx.globalCompositeOperation = 'source-over'; cx.globalAlpha = 0.6; cx.fillStyle = '#a296d8'; cx.font = '500 10px Cascadia Mono, Consolas, monospace';
    cx.fillText('shapes form each cycle; wave energy speeds the weaving; resonance mode sets the knot (visual, not physics)', 12, H2 - 8); cx.globalAlpha = 1; }
  requestAnimationFrame(frameS); })();
