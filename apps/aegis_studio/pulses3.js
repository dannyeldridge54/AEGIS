/* Janus · PULSES — the cosmic web alive. Bright dots travel along the weave edges wherever work is happening,
   seeded from window.AEGIS.pulses (recent activity) and, in the Janus app, polled live from janus_feed.jsonl via the api.
   Honest: a pulse just marks activity on a real connection; it is not a physical signal. */
(() => {
if (typeof weave === 'undefined' || typeof P === 'undefined') return;
const SEED = (window.AEGIS && window.AEGIS.pulses) || [];
const COL = [new THREE.Color('#4cc3ff'), new THREE.Color('#a07bff'), new THREE.Color('#ff4fd8'), new THREE.Color('#ff6ec7')];
const MAX = 160; const geo = new THREE.BufferGeometry();
const pos = new Float32Array(MAX*3), col = new Float32Array(MAX*3);
geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
const mat = new THREE.PointsMaterial({size: 3.4, vertexColors: true, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending, depthWrite: false});
const pts = new THREE.Points(geo, mat); weave.add(pts);
let live = [];   // {a:Vec3, b:Vec3, t0, dur, c}
function spawn(s, t, w, ci) { const a = P[s], b = P[t]; if (!a || !b) return;
  live.push({a, b, t0: performance.now(), dur: 1200 + 800*Math.random(), c: COL[ci % COL.length], w: w || 1}); if (live.length > MAX) live.shift(); }

// --- growth: the web grows as the feed delivers new nodes/edges (AF step e). Honest: just shows new connections, no claim. ---
const LANE_COL = {theory:'#4cc3ff', tool:'#a07bff', art:'#ff6ec7', chem:'#6fb8ff', power:'#ff4fd8', data:'#6fb8ff'};
const NMAX = 140, nGeo = new THREE.BufferGeometry(), nPos = new Float32Array(NMAX*3), nCol = new Float32Array(NMAX*3);
nGeo.setAttribute('position', new THREE.BufferAttribute(nPos, 3)); nGeo.setAttribute('color', new THREE.BufferAttribute(nCol, 3));
const nPts = new THREE.Points(nGeo, new THREE.PointsMaterial({size: 5.5, vertexColors: true, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false}));
weave.add(nPts); let nN = 0;
const EMAX = 260, eGeo = new THREE.BufferGeometry(), ePos = new Float32Array(EMAX*6);
eGeo.setAttribute('position', new THREE.BufferAttribute(ePos, 3));
const eLines = new THREE.LineSegments(eGeo, new THREE.LineBasicMaterial({color: 0xa07bff, transparent: true, opacity: 0.32, blending: THREE.AdditiveBlending, depthWrite: false}));
weave.add(eLines); let eN = 0;
function addNode(id, lane, title) { if (!id || P[id]) return;   // place near an existing node so it visibly attaches
  const ks = Object.keys(P), anc = ks.length ? P[ks[(Math.random()*ks.length)|0]] : new THREE.Vector3();
  const v = new THREE.Vector3(anc.x + (Math.random()-.5)*44, anc.y + (Math.random()-.5)*44, anc.z + (Math.random()-.5)*44);
  P[id] = v; if (typeof weave.userData === 'object') weave.userData.lastNode = id;
  if (nN < NMAX) { const c = new THREE.Color(LANE_COL[lane] || '#f3eeff');
    nPos[3*nN] = v.x; nPos[3*nN+1] = v.y; nPos[3*nN+2] = v.z; nCol[3*nN] = c.r; nCol[3*nN+1] = c.g; nCol[3*nN+2] = c.b; nN++;
    nGeo.attributes.position.needsUpdate = true; nGeo.attributes.color.needsUpdate = true; nGeo.setDrawRange(0, nN); } }
function addEdge(s, t) { const a = P[s], b = P[t]; if (!a || !b || eN >= EMAX) return; const o = eN*6;
  ePos[o]=a.x; ePos[o+1]=a.y; ePos[o+2]=a.z; ePos[o+3]=b.x; ePos[o+4]=b.y; ePos[o+5]=b.z; eN++;
  eGeo.attributes.position.needsUpdate = true; eGeo.setDrawRange(0, eN*2); spawn(s, t, 1, eN); }
window.janusAddNode = addNode; window.janusAddEdge = addEdge;
// continuous ambient: re-fire the seeded pulses on a rolling schedule so the web is always alive
let si = 0;
function ambient() { if (!SEED.length) return; const p = SEED[si % SEED.length]; si++; spawn(p.s, p.t, p.w, si); }
setInterval(() => { if (typeof view !== 'undefined' && view === 'weave') { for (let n = 0; n < 2; n++) ambient(); } }, 420);
// live feed from the Janus app (pywebview). Safe no-op in a browser/headless.
async function poll() { try { const api = window.pywebview && window.pywebview.api; if (api && api.janus_feed) {
    const evs = await api.janus_feed(); (evs || []).forEach((e, i) => {
      if (e.k === 'node') addNode(e.id, e.lane, e.title);
      else if (e.k === 'edge') addEdge(e.s, e.t);
      else if (e.k === 'pulse') spawn(e.s, e.t, e.w, i); }); } } catch (e) {} }
setInterval(poll, 3000);
function frame(now) { requestAnimationFrame(frame);
  if (typeof view === 'undefined' || view !== 'weave') { mat.opacity = 0; return; } mat.opacity = 0.95;
  let n = 0;
  for (let i = live.length - 1; i >= 0; i--) { const L = live[i]; const u = (now - L.t0)/L.dur;
    if (u >= 1) { live.splice(i, 1); continue; }
    if (n < MAX) { const x = L.a.x + (L.b.x - L.a.x)*u, y = L.a.y + (L.b.y - L.a.y)*u, z = (L.a.z + (L.b.z - L.a.z)*u) + 6*Math.sin(Math.PI*u);
      pos[3*n] = x; pos[3*n+1] = y; pos[3*n+2] = z; const g = Math.sin(Math.PI*u)*L.w; col[3*n] = L.c.r*g; col[3*n+1] = L.c.g*g; col[3*n+2] = L.c.b*g; n++; } }
  for (let k = n; k < MAX; k++) { pos[3*k] = pos[3*k+1] = pos[3*k+2] = 1e6; }
  geo.attributes.position.needsUpdate = true; geo.attributes.color.needsUpdate = true; geo.setDrawRange(0, MAX); }
requestAnimationFrame(frame);
window.janusPulse = spawn;   // other modules can fire a pulse
})();
