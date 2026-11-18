// Spectrum display (Danny 2026-11-18: "an optional weave of full RGB spectrum node to node, left to right").
// Optional: the "Spectrum" button cycles Off → Spectrum → Spectrum flow. Every thread is coloured along its own length by
// position across the weave — red on the left through orange, yellow, green, cyan, blue to violet on the right — so each
// wire runs the spectrum from its start node to its end node. Nodes and the fabric take the hue of where they sit.
// "Flow" slides the spectrum left → right in time. Off restores the original lane colours exactly.
(function () {
  if (typeof threads === 'undefined' || typeof knobs === 'undefined') return;
  const bar = document.querySelector('.stagebar'); if (!bar) return;
  const btn = document.createElement('button'); btn.className = 'btn'; btn.id = 'bspectrum'; btn.setAttribute('role', 'switch');
  btn.setAttribute('aria-checked', 'false'); btn.title = 'Colour every wire node to node by the full RGB spectrum, left (red) to right (violet)';
  btn.textContent = 'Spectrum: off'; bar.appendChild(btn);
  const X0 = -105, X1 = 105, HMAX = 0.83;   // red (0) → violet (0.83) across the weave
  const hue = (x, shift) => { let u = (x - X0)/(X1 - X0); u = Math.min(1, Math.max(0, u)); return ((u*HMAX + shift) % 1 + 1) % 1; };
  const tmp = new THREE.Color();
  // remember originals so Off is exact
  const orig = { threads: threads.map(th => ({ mat: th.l.material, c: th.c.clone() })), cores: knobs.map(k => k.userData.core.material.color.clone()),
                 fabric: fabric.map(l => Float32Array.from(l.geometry.attributes.color.array)) };
  const specMats = threads.map(th => new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending, depthWrite: false }));
  threads.forEach(th => { const n = th.l.geometry.attributes.position.count; if (!th.l.geometry.attributes.color) th.l.geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(n*3), 3)); });
  let mode = 0;   // 0 off, 1 spectrum, 2 flow
  function paint(shift) {
    threads.forEach((th, k) => {
      const pos = th.l.geometry.attributes.position, colr = th.l.geometry.attributes.color;
      for (let i = 0; i < pos.count; i++) { tmp.setHSL(hue(pos.getX(i), shift), 1, 0.58); colr.setXYZ(i, tmp.r, tmp.g, tmp.b); }
      colr.needsUpdate = true;
      const mid = pos.getX(Math.floor(pos.count/2)); th.c.setHSL(hue(mid, shift), 1, 0.62);   // particles riding the wire
    });
    knobs.forEach(g => { g.userData.core.material.color.setHSL(hue(g.position.x, shift), 1, 0.6); });
    fabric.forEach(l => { const b = l.userData.base, colr = l.geometry.attributes.color;
      for (let i = 0; i < b.length; i++) { tmp.setHSL(hue(b[i][0], shift), 1, 0.45); colr.setXYZ(i, tmp.r, tmp.g, tmp.b); } colr.needsUpdate = true; });
  }
  function restore() {
    threads.forEach((th, k) => { th.l.material = orig.threads[k].mat; th.c.copy(orig.threads[k].c); });
    knobs.forEach((g, i) => g.userData.core.material.color.copy(orig.cores[i]));
    fabric.forEach((l, i) => { l.geometry.attributes.color.array.set(orig.fabric[i]); l.geometry.attributes.color.needsUpdate = true; });
  }
  function set(m) {
    mode = m; btn.setAttribute('aria-checked', String(m > 0)); btn.classList.toggle('on', m > 0);
    btn.textContent = ['Spectrum: off', 'Spectrum: on', 'Spectrum: flow'][m];
    if (m === 0) { restore(); return; }
    threads.forEach((th, k) => { th.l.material = specMats[k]; }); paint(0);
    try { localStorage.setItem('janus.spectrum', String(m)); } catch (e) {}
  }
  btn.onclick = () => { set((mode + 1) % 3); if (mode === 0) { try { localStorage.setItem('janus.spectrum', '0'); } catch (e) {} } };
  let t0 = performance.now(), lastPaint = 0;
  (function tick(now) {
    requestAnimationFrame(tick);
    if (mode === 2 && now - lastPaint > 33) { paint(((now - t0)/1000)*0.06); lastPaint = now; }   // ~30 Hz; full cycle ≈ 17 s
    else if (mode === 1 && now - lastPaint > 500) { paint(0); lastPaint = now; }               // follow the wave-moved nodes
  })(performance.now());
  try { const m = parseInt(localStorage.getItem('janus.spectrum') || '0', 10); if (m > 0) set(m); } catch (e) {}
})();
