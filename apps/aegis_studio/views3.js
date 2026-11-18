/* Janus · three extra views of the same AEGIS web, driven by the same live wave amplitudes (amp[]) as the weave:
   ONION   — concentric shells, one per layer (string sector core → theory → toolkits → lanes → wiring skin)
   VORTEX  — differential-rotation funnel; nodes ordered oldest (outer) → newest (inner) by their latest D-note
   BLACK HOLE — event horizon, photon ring, Doppler accretion disk and a lensed image of the disk; nodes orbit by layer
   Every node is a small solid whose shape encodes its layer and status; waves deform it ("geometry through the waves").
   The selected node is shown large in a GEOMETRY LENS whose vertices ripple with the node's own wave and its neighbours'.
   Particles: names + state; anything not discovered is flagged (⚑ predicted / bounded / inferred). */
(() => {
const NODES = WEB.nodes, EDGES = WEB.edges, PART = (window.AEGIS.particles || []);
const SHAPE = {strings: () => new THREE.TorusKnotGeometry(0.9, 0.28, 64, 8), theory: () => new THREE.IcosahedronGeometry(1.15, 0),
  janus: () => new THREE.OctahedronGeometry(1.25, 0), wiring: () => new THREE.TorusGeometry(0.95, 0.32, 10, 24),
  left: () => new THREE.DodecahedronGeometry(1.1, 0), centre: () => new THREE.DodecahedronGeometry(1.1, 0), right: () => new THREE.DodecahedronGeometry(1.1, 0)};
const PRISM = f => new THREE.Color().setHSL(0.57 + 0.36*Math.pow(Math.min(1, Math.max(0, f)), 1.3), 0.95, 0.6);
const laneF = {strings: 0.0, theory: 0.35, janus: 0.75, wiring: 0.15, left: 0.05, centre: 0.5, right: 0.95};
const nbr = NODES.map(() => []); EDGES.forEach(e => { const a = ix[e.s], b = ix[e.t]; if (a != null && b != null) { nbr[a].push(b); nbr[b].push(a); } });
const lastD = n => { const m = String(n.refs || '').match(/D(\d{3,4})/g); return m ? Math.max(...m.map(x => +x.slice(1))) : 0; };

function makeView() {
  const g = new THREE.Group(); g.visible = false; scene.add(g);
  const meshes = NODES.map((n, i) => {
    const geo = (SHAPE[n.lane] || SHAPE.theory)(); const c = PRISM((laneF[n.lane] ?? 0.5) + 0.08*Math.sin(i));
    const killed = n.status === 'killed', post = n.status === 'postulate';
    const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({color: c, wireframe: killed || post, transparent: true, opacity: killed ? 0.45 : 0.95}));
    m.userData = {i, id: n.id, base: c.clone(), post}; g.add(m); return m; });
  const ePos = new Float32Array(EDGES.length*6), eCol = new Float32Array(EDGES.length*6);
  const eGeo = new THREE.BufferGeometry(); eGeo.setAttribute('position', new THREE.BufferAttribute(ePos, 3)); eGeo.setAttribute('color', new THREE.BufferAttribute(eCol, 3));
  const lines = new THREE.LineSegments(eGeo, new THREE.LineBasicMaterial({vertexColors: true, transparent: true, opacity: 0.35})); g.add(lines);
  return {g, meshes, ePos, eCol, eGeo, P: NODES.map(() => new THREE.Vector3())};
}
function updateCommon(V, t) {
  V.meshes.forEach((m, i) => { const a = amp[i] || 0; m.position.copy(V.P[i]); const s = 1 + 0.9*Math.min(2, Math.abs(a)) + (m.userData.post ? 0.25*Math.sin(3*t + i) : 0);
    m.scale.setScalar(s); m.rotation.x += 0.004 + 0.05*Math.abs(a); m.rotation.y += 0.006 + 0.04*a;
    m.material.color.copy(m.userData.base).offsetHSL(0, 0, Math.max(-0.2, Math.min(0.3, 0.25*a))); });
  EDGES.forEach((e, k) => { const a = ix[e.s], b = ix[e.t]; if (a == null || b == null) return; const pa = V.P[a], pb = V.P[b];
    V.ePos.set([pa.x, pa.y, pa.z, pb.x, pb.y, pb.z], 6*k); const w = 0.35 + 0.65*Math.min(1, Math.abs((amp[a] || 0) + (amp[b] || 0)));
    const c = e.sign < 0 ? new THREE.Color(C('--red')) : PRISM(0.2 + 0.6*((k*0.37) % 1)); c.multiplyScalar(w); V.eCol.set([c.r, c.g, c.b, c.r, c.g, c.b], 6*k); });
  V.eGeo.attributes.position.needsUpdate = true; V.eGeo.attributes.color.needsUpdate = true;
}
// ---------- particles: labels with discovery flags ----------
const FLAG = {observed: ['discovered', '#4cc3ff'], inferred: ['⚑ inferred (not directly seen)', '#a07bff'], predicted: ['⚑ NOT DISCOVERED — predicted by SERAPIS', '#ff4fd8'],
  bounded: ['⚑ NOT DISCOVERED — bounded', '#ff6ec7'], computed: ['⚑ NOT DISCOVERED — computed (string sector)', '#ff9bd9']};
function label(p) { const [flag, col] = FLAG[p.state] || ['?', '#fff']; const cv = document.createElement('canvas'); cv.width = 512; cv.height = 112; const x = cv.getContext('2d');
  x.fillStyle = 'rgba(6,2,20,0.72)'; x.fillRect(0, 0, 512, 112); x.strokeStyle = col; x.lineWidth = 3; x.strokeRect(2, 2, 508, 108);
  x.font = 'bold 44px Segoe UI, sans-serif'; x.fillStyle = col; x.fillText(`${p.sym}  ${p.name}`.slice(0, 26), 14, 50); x.font = '26px Segoe UI, sans-serif'; x.fillStyle = '#f3eeff'; x.fillText(flag, 14, 92);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({map: new THREE.CanvasTexture(cv), transparent: true, depthWrite: false})); s.scale.set(16, 3.5, 1); s.userData = p; return s; }
function addParticles(V) { V.parts = PART.filter(p => ix[p.node] != null).map(p => { const s = label(p); V.g.add(s); return s; }); }
function updateParticles(V, t) { (V.parts || []).forEach((s, k) => { const i = ix[s.userData.node]; const p = V.P[i];
  const rr = Math.hypot(p.x, p.y) || 1, out = V.labelOut || 0; s.position.set(p.x + (out ? out*p.x/rr : 4*Math.cos(k*1.3)), p.y + (out ? out*p.y/rr : 4*Math.sin(k*1.3)), p.z + 5 + 3*((k % 4) - 1.5)*(out ? 1 : 0) + 1.5*Math.sin(t + k)); s.material.opacity = partsOn ? 0.95 : 0; }); }
let partsOn = true;
// ---------- geometry lens: the selected node, its vertices rippled by its own wave and its neighbours' ----------
function makeLens(V) { const geo = new THREE.IcosahedronGeometry(9, 3); const base = geo.attributes.position.array.slice();
  const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({color: PRISM(0.6), wireframe: true, transparent: true, opacity: 0.85})); V.g.add(m); V.lens = {m, base, geo, cur: null}; }
function updateLens(V, t, at) { const L = V.lens; if (!L) return; const id = sel; if (!id) { L.m.visible = false; return; } L.m.visible = true; const i = ix[id];
  if (L.cur !== id) { const n = NODES[i]; const ng = (SHAPE[n.lane] || SHAPE.theory)(); const src = ng.attributes.position; const lg = new THREE.IcosahedronGeometry(9, 3);
    L.geo.dispose(); L.m.geometry = lg; L.geo = lg; L.base = lg.attributes.position.array.slice(); L.cur = id; L.m.material.color = PRISM((laneF[n.lane] ?? 0.5)); L.k = 2 + (n.lane || '').length % 5; }
  const pos = L.geo.attributes.position.array, b = L.base, own = amp[i] || 0, nb = nbr[i];
  for (let v = 0; v < pos.length; v += 3) { const x = b[v], y = b[v+1], z = b[v+2]; const r = Math.hypot(x, y, z) || 1; const th = Math.atan2(y, x), ph = Math.acos(z/r);
    let d = 0.18*own*Math.sin(L.k*th + 3*t) * Math.sin(L.k*ph);
    for (let q = 0; q < Math.min(6, nb.length); q++) d += 0.12*(amp[nb[q]] || 0)*Math.cos((q + 2)*th - (q + 1)*ph + 2*t);
    const f = 1 + d + 0.03*Math.sin(2*t + 5*ph); pos[v] = x*f; pos[v+1] = y*f; pos[v+2] = z*f; }
  L.geo.attributes.position.needsUpdate = true; L.m.position.copy(at); L.m.rotation.y = 0.2*t; }
// ---------- ONION ----------
const ON = makeView(); const R0 = {strings: 9, theory: 20, janus: 32, left: 44, centre: 44, right: 44, wiring: 56};
const groups = {}; NODES.forEach((n, i) => (groups[R0[n.lane] ?? 26] ||= []).push(i));
const onShells = Object.keys(groups).map(r => { const s = new THREE.Mesh(new THREE.SphereGeometry(+r, 30, 15), new THREE.MeshBasicMaterial({color: PRISM(+r/60), wireframe: true, transparent: true, opacity: 0.05}));
  s.userData.r = +r; ON.g.add(s); return s; });
const onBase = NODES.map(() => new THREE.Vector3());
Object.entries(groups).forEach(([r, arr]) => arr.forEach((i, k) => { const N = arr.length, y = 1 - 2*(k + 0.5)/N, rr = Math.sqrt(1 - y*y), th = k*2.399963;
  onBase[i].set(+r*rr*Math.cos(th), +r*rr*Math.sin(th), +r*y); }));
addParticles(ON); makeLens(ON);
function onionFrame(t) { onShells.forEach((s, k) => { s.rotation.z = t*0.05*(k % 2 ? -1 : 1)*(1 + k*0.3); const arr = groups[s.userData.r];
    const e = arr.reduce((m, i) => m + Math.abs(amp[i] || 0), 0)/arr.length; s.material.opacity = (s.userData.r > 50 ? 0.025 : 0.05) + 0.25*Math.min(1, e); s.scale.setScalar(1 + 0.04*Math.min(1, e)*Math.sin(6*t)); });
  NODES.forEach((n, i) => { const r = R0[n.lane] ?? 26; const k = Object.keys(groups).indexOf(String(r)); const a = t*0.05*(k % 2 ? -1 : 1)*(1 + k*0.3);
    const b = onBase[i]; ON.P[i].set(b.x*Math.cos(a) - b.y*Math.sin(a), b.x*Math.sin(a) + b.y*Math.cos(a), b.z); });
  updateCommon(ON, t); updateParticles(ON, t); updateLens(ON, t, new THREE.Vector3(0, 0, 0)); }
// ---------- VORTEX ----------
const VX = makeView(); const order = NODES.map((n, i) => [lastD(n), i]).sort((a, b) => a[0] - b[0]).map(x => x[1]); const vr = new Float32Array(NN), vth = new Float32Array(NN);
order.forEach((i, k) => { vr[i] = 62 - 52*Math.pow(k/(NN - 1), 0.85); vth[i] = k*2.399963; });
const SP = 2400, spPos = new Float32Array(SP*3), spR = new Float32Array(SP), spT = new Float32Array(SP), spCol = new Float32Array(SP*3);
for (let q = 0; q < SP; q++) { spR[q] = 6 + 60*Math.random(); spT[q] = Math.random()*6.283; const c = PRISM(Math.random()); spCol.set([c.r, c.g, c.b], 3*q); }
const spGeo = new THREE.BufferGeometry(); spGeo.setAttribute('position', new THREE.BufferAttribute(spPos, 3)); spGeo.setAttribute('color', new THREE.BufferAttribute(spCol, 3));
VX.g.add(new THREE.Points(spGeo, new THREE.PointsMaterial({size: 0.7, vertexColors: true, transparent: true, opacity: 0.8, depthWrite: false})));
addParticles(VX); makeLens(VX);
const zF = r => -150/(r + 4) + 8;
function vortexFrame(t, dt) {
  NODES.forEach((n, i) => { const r = vr[i]*(1 + 0.05*Math.tanh(amp[i] || 0)), th = vth[i] + t*speed*3.2/Math.pow(r, 0.8); VX.P[i].set(r*Math.cos(th), r*Math.sin(th), zF(r)); });
  for (let q = 0; q < SP; q++) { spR[q] -= dt*speed*(3 + 40/spR[q]); spT[q] += dt*speed*9/Math.pow(spR[q], 0.9); if (spR[q] < 4) { spR[q] = 60 + 8*Math.random(); spT[q] = Math.random()*6.283; }
    spPos.set([spR[q]*Math.cos(spT[q]), spR[q]*Math.sin(spT[q]), zF(spR[q])], 3*q); }
  spGeo.attributes.position.needsUpdate = true; updateCommon(VX, t); updateParticles(VX, t); updateLens(VX, t, new THREE.Vector3(0, 0, 30)); }
// ---------- BLACK HOLE ----------
const BH = makeView();
BH.g.add(new THREE.Mesh(new THREE.SphereGeometry(6, 48, 24), new THREE.MeshBasicMaterial({color: 0x000000})));
const ring = new THREE.Mesh(new THREE.TorusGeometry(8.2, 0.35, 12, 120), new THREE.MeshBasicMaterial({color: new THREE.Color('#ffd6ff')})); ring.rotation.x = Math.PI/2; BH.g.add(ring);
const halo = new THREE.Mesh(new THREE.TorusGeometry(12, 1.6, 16, 160, Math.PI), new THREE.MeshBasicMaterial({color: PRISM(0.8), transparent: true, opacity: 0.55})); BH.g.add(halo);   // lensed image of the far disk
const halo2 = new THREE.Mesh(new THREE.TorusGeometry(10.5, 0.7, 12, 140, Math.PI), new THREE.MeshBasicMaterial({color: PRISM(0.4), transparent: true, opacity: 0.45})); halo2.rotation.z = Math.PI; BH.g.add(halo2);
const DP = 7000, dR = new Float32Array(DP), dT = new Float32Array(DP), dPos = new Float32Array(DP*3), dCol = new Float32Array(DP*3);
for (let q = 0; q < DP; q++) { dR[q] = 10 + 55*Math.pow(Math.random(), 1.6); dT[q] = Math.random()*6.283; }
const dGeo = new THREE.BufferGeometry(); dGeo.setAttribute('position', new THREE.BufferAttribute(dPos, 3)); dGeo.setAttribute('color', new THREE.BufferAttribute(dCol, 3));
BH.g.add(new THREE.Points(dGeo, new THREE.PointsMaterial({size: 0.55, vertexColors: true, transparent: true, opacity: 0.9, depthWrite: false})));
const bhR = NODES.map((n, i) => (n.status === 'frozen' || /band|point|serapis_e|janus/.test(n.id)) ? 11 + 3*((i*0.61) % 1)
  : ({theory: 16, strings: 13, janus: 30, left: 42, centre: 42, right: 42, wiring: 52}[n.lane] ?? 24) + 10*((i*0.37) % 1));
const bhT = NODES.map((n, i) => i*2.399963), bhI = NODES.map((n, i) => 0.18*Math.sin(i*1.7));
addParticles(BH); makeLens(BH); BH.labelOut = 14;
function bhFrame(t, dt) {
  for (let q = 0; q < DP; q++) { dT[q] += dt*speed*28/Math.pow(dR[q], 1.5); const x = dR[q]*Math.cos(dT[q]), y = dR[q]*Math.sin(dT[q]); dPos.set([x, y, 0.25*Math.sin(3*dT[q] + dR[q])], 3*q);
    const dop = 0.5 + 0.5*Math.sin(dT[q]); const hot = Math.exp(-(dR[q] - 10)/18); const c = PRISM(0.15 + 0.7*dop); c.multiplyScalar(0.35 + 0.65*hot*(0.5 + dop)); dCol.set([c.r, c.g, c.b], 3*q); }
  dGeo.attributes.position.needsUpdate = true; dGeo.attributes.color.needsUpdate = true;
  halo.lookAt(persp.position); halo2.lookAt(persp.position); halo.rotation.z = 0; halo2.rotation.z = Math.PI;
  NODES.forEach((n, i) => { const th = bhT[i] + t*speed*28/Math.pow(bhR[i], 1.5); const r = bhR[i]*(1 + 0.04*Math.tanh(amp[i] || 0));
    BH.P[i].set(r*Math.cos(th), r*Math.sin(th)*Math.cos(bhI[i]), r*Math.sin(th)*Math.sin(bhI[i])); });
  updateCommon(BH, t); updateParticles(BH, t); updateLens(BH, t, new THREE.Vector3(0, 0, 34)); ring.material.color.copy(PRISM(0.7 + 0.2*Math.sin(t))); }
// ---------- view switching (extends setView) ----------
const V3 = {onion: [ON, onionFrame, [0, -150, 95]], vortex: [VX, vortexFrame, [0, -155, 55]], bh: [BH, bhFrame, [0, -125, 32]]};
['onion', 'vortex', 'bh'].forEach(k => tabs[k] = 't-' + k);
const _sv = setView;
setView = function (v) { if (V3[v]) { view = v; Object.entries(tabs).forEach(([k, id]) => document.getElementById(id)?.setAttribute('aria-selected', String(k === v)));
    weave.visible = false; land.visible = false; document.getElementById('hud').hidden = true; setCam(true); bloom.strength = bloomK;
    Object.entries(V3).forEach(([k, [V]]) => V.g.visible = k === v); const p = V3[v][2]; persp.position.set(...p); ctl.target.set(0, 0, v === 'vortex' ? -6 : 0);
    document.getElementById('partcard').hidden = false; return; }
  Object.values(V3).forEach(([V]) => V.g.visible = false); document.getElementById('partcard').hidden = true; _sv(v); };
['onion', 'vortex', 'bh'].forEach(k => { const b = document.getElementById('t-' + k); if (b) b.onclick = () => setView(k); });
// click a node in these views → select it (same as the weave) → the geometry lens shows it; waves from the rack buttons work as usual
canvas.addEventListener('click', ev => { const V = V3[view]?.[0]; if (!V) return; const r = canvas.getBoundingClientRect();
  mouse.set(((ev.clientX - r.left)/r.width)*2 - 1, -((ev.clientY - r.top)/r.height)*2 + 1); ray.setFromCamera(mouse, persp);
  const hit = ray.intersectObjects(V.meshes, false)[0]; if (hit) select(hit.object.userData.id); });
// particle card (rack)
const ul = document.getElementById('partlist');
if (ul) PART.forEach(p => { const li = document.createElement('li'); const [flag, col] = FLAG[p.state] || ['?', '#fff']; li.style.borderLeft = `3px solid ${col}`; li.style.paddingLeft = '8px';
  li.innerHTML = `<b style="color:${col}">${p.sym}</b> ${p.name} <span class="small">· ${flag}</span>`; li.title = p.info || ''; ul.appendChild(li); });
document.getElementById('bparts')?.addEventListener('click', e => { partsOn = !partsOn; e.target.classList.toggle('on', partsOn); });
let lastT = performance.now();
function loop3(now) { requestAnimationFrame(loop3); const t = now/1000, dt = Math.min(0.05, (now - lastT)/1000); lastT = now; const e = V3[view]; if (e) e[1](t, dt); }
requestAnimationFrame(loop3);
})();
