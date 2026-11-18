/* Janus · STRINGS view — where SERAPIS's tilt comes from.
   The inflaton torus of T⁶/(Z₂×Z₂) with complex structure τ = ½ + i·y (y = Im τ is the inflaton, K = −ln 2 Im τ).
   Its four Z₂ fixed points carry O3-planes; stuck D3 branes sit 5 at each half-period and 1 at the origin (tadpole 3N + N₀ = 16, D696).
   The uneven charge (N_eff = 4) gives the BHK one-loop tilt C = 15 N_eff/(64π⁶ Im S·Im ρ) (D689, NA11).
   The torus shape follows the real SERAPIS-E history y(N) at the A1 point (Janus background; data: docs/web/string_geom.json):
   long thin tube during inflation (y ≈ 14.6 at horizon exit) → round torus at the vacuum ρ (y = √3/2). Waves on stuck_d3 / bhk_tilt / serapis_e light the branes. */
(() => {
const SG = window.AEGIS.strings; if (!SG) return;
const g = new THREE.Group(); g.visible = false; scene.add(g);
const PR = f => new THREE.Color().setHSL(0.57 + 0.36*Math.pow(Math.min(1, Math.max(0, f)), 1.3), 0.95, 0.6);
const Rm = 24; let torus = null;
const tmat = new THREE.MeshBasicMaterial({color: PR(0.3), wireframe: true, transparent: true, opacity: 0.35});
function pos(u, v, r) { const th = 2*Math.PI*u, ph = 2*Math.PI*v; return new THREE.Vector3((Rm + r*Math.cos(ph))*Math.cos(th), (Rm + r*Math.cos(ph))*Math.sin(th), r*Math.sin(ph)); }
function nrm(u, v) { const th = 2*Math.PI*u, ph = 2*Math.PI*v; return new THREE.Vector3(Math.cos(ph)*Math.cos(th), Math.cos(ph)*Math.sin(th), Math.sin(ph)); }
function sprite(text, col, w = 22, sub = '') { const cv = document.createElement('canvas'); cv.width = 640; cv.height = sub ? 120 : 72; const x = cv.getContext('2d');
  x.fillStyle = 'rgba(6,2,20,0.7)'; x.fillRect(0, 0, cv.width, cv.height); x.strokeStyle = col; x.lineWidth = 3; x.strokeRect(2, 2, cv.width - 4, cv.height - 4);
  x.font = 'bold 38px Segoe UI, sans-serif'; x.fillStyle = col; x.fillText(text, 14, 48); if (sub) { x.font = '28px Segoe UI'; x.fillStyle = '#f3eeff'; x.fillText(sub, 14, 98); }
  const t = new THREE.CanvasTexture(cv); const s = new THREE.Sprite(new THREE.SpriteMaterial({map: t, transparent: true, depthWrite: false})); s.scale.set(w, w*cv.height/cv.width, 1); s.userData.cv = cv; return s; }
function retext(s, text, col, sub = '') { const cv = s.userData.cv, x = cv.getContext('2d'); x.clearRect(0, 0, cv.width, cv.height); x.fillStyle = 'rgba(6,2,20,0.7)'; x.fillRect(0, 0, cv.width, cv.height);
  x.strokeStyle = col; x.lineWidth = 3; x.strokeRect(2, 2, cv.width - 4, cv.height - 4); x.font = 'bold 38px Segoe UI, sans-serif'; x.fillStyle = col; x.fillText(text, 14, 48);
  if (sub) { x.font = '28px Segoe UI'; x.fillStyle = '#f3eeff'; x.fillText(sub, 14, 98); } s.material.map.needsUpdate = true; }
// branes: stacks of glowing beads along the outward normal at the fixed points; O3-planes as rings
const stacks = SG.branes.map((b, k) => { const grp = new THREE.Group(); const col = b.n === 1 ? PR(0.05) : PR(0.85);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(2.2, 0.25, 8, 32), new THREE.MeshBasicMaterial({color: new THREE.Color('#ffd6ff')})); grp.add(ring);
  const beads = []; for (let q = 0; q < b.n; q++) { const s = new THREE.Mesh(new THREE.SphereGeometry(1.0, 16, 12), new THREE.MeshBasicMaterial({color: col})); grp.add(s); beads.push(s); }
  const lab = sprite(b.label, b.n === 1 ? '#4cc3ff' : '#ff4fd8', 20); grp.add(lab); g.add(grp); return {b, grp, ring, beads, lab}; });
// small companion tori (T₁, T₂ of T⁴), the lattice cell and the read-out
const comp = [[-62, 38, 'T₁ (racetrack; Im T₁ = 4.31)'], [62, 38, 'T₂']].map(([x, y, t]) => { const m = new THREE.Mesh(new THREE.TorusGeometry(7, 2.6, 16, 48), new THREE.MeshBasicMaterial({color: PR(0.55), wireframe: true, transparent: true, opacity: 0.25}));
  m.position.set(x, y, 0); g.add(m); const s = sprite(t, '#a07bff', 18); s.position.set(x, y + 12, 0); g.add(s); return m; });
const cellGeo = new THREE.BufferGeometry(); const cellPos = new Float32Array(5*3); cellGeo.setAttribute('position', new THREE.BufferAttribute(cellPos, 3));
const cell = new THREE.Line(cellGeo, new THREE.LineBasicMaterial({color: PR(0.95)})); g.add(cell); const cellLab = sprite('τ = ½ + i·y', '#ff6ec7', 18, ''); g.add(cellLab);
const title = sprite('Inflaton torus of T⁶/(Z₂×Z₂)', '#6fb8ff', 34, ''); title.position.set(0, -44, 26); g.add(title);
const read = sprite('', '#f3eeff', 40, ''); read.position.set(0, -44, 14); g.add(read);
const tilt = sprite(`C = 15·N_eff/(64π⁶·Im S·Im ρ)`, '#ff4fd8', 36, `N_eff = 4 → Im S·Im ρ = ${SG.ImS_Imrho.toFixed(0)}  (g_s ${SG.gs}, Im S ${SG.ImS})`); tilt.position.set(0, 50, 8); g.add(tilt);
const N = SG.N, Y = SG.y; let lastR = -1;
// Measurement lens (PW6, D1268): a future n_s → C and Im S·Im ρ at the leptogenesis T_R; recolours the torus, scales the D3 glow
const MT = SG.meter || []; const lensEl = document.getElementById('lensns'), lensOn = document.getElementById('lenson'), lensRead = document.getElementById('lensread');
function lensAt(ns) { if (MT.length < 2) return null; let i = 0; while (i < MT.length - 2 && MT[i + 1].ns < ns) i++;
  const a = MT[i], b = MT[i + 1], f = Math.min(1, Math.max(0, (ns - a.ns)/(b.ns - a.ns))), L = (k, lg) => lg ? Math.exp(Math.log(a[k]) + f*(Math.log(b[k]) - Math.log(a[k]))) : a[k] + f*(b[k] - a[k]);
  return {ns, C: L('C', 1), P: L('P', 1), r: L('r'), alpha_s: L('alpha_s'), Nstar: L('Nstar')}; }
let lens = null;
function updLens() { if (!lensEl) return; lens = lensOn && lensOn.checked ? lensAt(parseFloat(lensEl.value)) : null; if (!lensRead) return;
  if (!lens) { lensRead.textContent = 'lens off: benchmark Im S·Im ρ = ' + SG.ImS_Imrho.toFixed(0); return; }
  lensRead.textContent = `n_s ${lens.ns.toFixed(4)} → C ${lens.C.toExponential(3)}, Im S·Im ρ ${lens.P.toFixed(0)} · r ${lens.r.toExponential(2)}, α_s ${lens.alpha_s.toExponential(2)}, N* ${lens.Nstar.toFixed(2)}` + (lens.ns > 0.975 ? ' · above the frozen n_s ceiling 0.975' : '') + ' [postulate, exact PW6 table]'; }
lensEl?.addEventListener('input', updLens); lensOn?.addEventListener('change', updLens); updLens();
function yAt(n) { let i = 0; while (i < N.length - 2 && N[i + 1] < n) i++; const f = (n - N[i])/((N[i + 1] - N[i]) || 1); return Y[i] + f*(Y[i + 1] - Y[i]); }
function frameS(t) {
  const T = 18/(speed || 1), ph = (t % T)/T, n = Math.min(SG.Nend, ph*1.12*SG.Nend), y = yAt(n), left = SG.Nend - n;
  const r = Math.min(0.92*Rm, Rm/(0.35 + 0.17*y));
  if (Math.abs(r - lastR) > 0.05) { if (torus) { g.remove(torus); torus.geometry.dispose(); } torus = new THREE.Mesh(new THREE.TorusGeometry(Rm, r, 28, 96), tmat); g.add(torus); lastR = r; }
  torus.rotation.z = 0.08*t; tmat.color.copy(lens ? PR(Math.min(1, Math.max(0, (1200 - lens.P)/650))) : PR(0.2 + 0.6*Math.min(1, y/16)));
  const a = k => Math.abs(amp[ix[k]] || 0), glow = (1 + 1.5*Math.min(1, a('stuck_d3') + a('bhk_tilt') + 0.5*a('serapis_e')))*(lens ? lens.C/1.25e-6 : 1);
  stacks.forEach(({b, grp, ring, beads, lab}, k) => { const [u, v] = b.at; const p = pos(u, v, r), nn = nrm(u, v); grp.position.set(0, 0, 0);
    const rot = new THREE.Matrix4().makeRotationZ(0.08*t); const P = p.clone().applyMatrix4(rot), Nn = nn.clone().applyMatrix4(rot);
    ring.position.copy(P); ring.lookAt(P.clone().add(Nn));
    beads.forEach((s, q) => { s.position.copy(P.clone().add(Nn.clone().multiplyScalar(2.2*(q + 1)))); s.scale.setScalar(glow*(0.8 + 0.25*Math.sin(3*t + q + k))); });
    lab.position.copy(P.clone().add(Nn.clone().multiplyScalar(2.2*(b.n + 2) + 3))); });
  comp.forEach((m, k) => { m.rotation.x = 0.3*t*(k ? 1 : -1); m.rotation.y = 0.2*t; });
  const s = 9, ys = Math.min(30, 6*Math.log(1 + y)*1.6), ox = -70, oy = -20;
  [[0, 0], [1, 0], [1.5, ys/s], [0.5, ys/s], [0, 0]].forEach(([xx, yy], k) => cellPos.set([ox + s*xx, oy + s*yy, 0], 3*k)); cellGeo.attributes.position.needsUpdate = true;
  cellLab.position.set(ox + 10, oy - 6, 0); retext(cellLab, `τ = ½ + i·${y.toFixed(3)}`, '#ff6ec7');
  const stage = n < SG.Nend - SG.Nstar ? 'before horizon exit' : n < SG.Nend - 0.5 ? `${left.toFixed(1)} e-folds left` : 'at ρ: inflation over';
  retext(read, `y = Im τ = ${y.toFixed(2)}  ·  N = ${n.toFixed(1)} / ${SG.Nend.toFixed(1)}`, '#f3eeff'); read.userData.stage = stage;
  retext(title, `Inflaton torus · ${stage}`, '#6fb8ff');
  const P = lens ? lens.P : SG.ImS_Imrho; if (Math.abs((tilt.userData.P || 0) - P) > 0.5) { tilt.userData.P = P;
    retext(tilt, `C = 15·N_eff/(64π⁶·Im S·Im ρ)`, '#ff4fd8', lens ? `lens n_s ${lens.ns.toFixed(4)} → Im S·Im ρ = ${P.toFixed(0)}, C ${lens.C.toExponential(2)}` : `N_eff = 4 → Im S·Im ρ = ${P.toFixed(0)}  (g_s ${SG.gs}, Im S ${SG.ImS})`); }
}
tabs.strings = 't-strings';
const _sv2 = setView;
setView = function (v) { if (v === 'strings') { view = v; Object.entries(tabs).forEach(([k, id]) => document.getElementById(id)?.setAttribute('aria-selected', String(k === v)));
    weave.visible = false; land.visible = false; scene.children.forEach(c => { if (c !== g && c.type === 'Group' && c !== weave && c !== land) c.visible = false; });
    g.visible = true; document.getElementById('hud').hidden = true; const lc = document.getElementById('lenscard'); if (lc) lc.hidden = false; setCam(true); persp.position.set(0, -120, 70); ctl.target.set(0, 0, 0); return; }
  g.visible = false; const lc = document.getElementById('lenscard'); if (lc) lc.hidden = true; _sv2(v); };
document.getElementById('t-strings')?.addEventListener('click', () => setView('strings'));
function loopS(now) { requestAnimationFrame(loopS); if (view === 'strings') frameS(now/1000); }
requestAnimationFrame(loopS);
})();
