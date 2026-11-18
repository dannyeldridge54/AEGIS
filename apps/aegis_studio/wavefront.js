// Wavefront display (Danny 2026-11-18: "one that does singular front to back and shows the wave going through, shapes forming
// geometry"). Optional: "Wavefront" button. One wavefront of a single colour sweeps the weave from front to back. As it passes a
// node, that node fires and the geometry around it forms: its nearest neighbours close into a hexagon (6 around it, the A2 tile),
// a square (4, the τ = i tile) or a triangle (3), with spokes from the centre, then fade. Each pass takes the next colour.
(function () {
  if (typeof knobs === 'undefined' || typeof weave === 'undefined') return;
  const bar = document.querySelector('.stagebar'); if (!bar) return;
  const btn = document.createElement('button'); btn.className = 'btn'; btn.id = 'bwavefront'; btn.setAttribute('role', 'switch');
  btn.setAttribute('aria-checked', 'false'); btn.title = 'One wavefront sweeps front to back; geometry forms around each node it passes';
  btn.textContent = 'Wavefront: off'; bar.appendChild(btn);
  const Y0 = -112, Y1 = 66, PASS_S = 9, FADE_S = 2.8, HUES = [0.53, 0.83, 0.12, 0.33, 0.0, 0.66];
  // neighbours from the resting layout
  const base = knobs.map(g => g.position.clone()); const N = base.length;
  const nbr = base.map((p, i) => base.map((q, j) => [j, i === j ? 1e9 : Math.hypot(p.x - q.x, p.y - q.y)]).sort((a, b) => a[1] - b[1]).slice(0, 6));
  const group = new THREE.Group(); group.visible = false; weave.add(group);
  const frontGeo = new THREE.BufferGeometry(); const FN = 140; frontGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(FN*3), 3));
  const frontMat = new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false });
  const front = new THREE.Line(frontGeo, frontMat); group.add(front);
  const glowGeo = new THREE.PlaneGeometry(220, 2.2); const glowMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.05, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
  const glow = new THREE.Mesh(glowGeo, glowMat); group.add(glow);
  let on = false, t0 = 0, pass = 0, prevY = Y0, live = [];
  const col = new THREE.Color();
  function shape(i, hue) {
    const c = knobs[i].position, ns = nbr[i].filter(([, d]) => d < 34).map(([j]) => j);
    const k = ns.length >= 6 ? 6 : ns.length >= 4 ? 4 : ns.length >= 3 ? 3 : 0; if (!k) return;
    const ring = ns.slice(0, k).map(j => knobs[j].position).sort((a, b) => Math.atan2(a.y - c.y, a.x - c.x) - Math.atan2(b.y - c.y, b.x - c.x));
    const pts = []; ring.forEach(p => pts.push(p.x, p.y, p.z + 0.5)); pts.push(ring[0].x, ring[0].y, ring[0].z + 0.5);   // the polygon
    ring.forEach(p => pts.push(c.x, c.y, c.z + 0.5, p.x, p.y, p.z + 0.5));                                            // spokes
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(pts), 3));
    col.setHSL(hue, 1, 0.6);
    const poly = new THREE.Line(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(pts.slice(0, (k + 1)*3)), 3)),
      new THREE.LineBasicMaterial({ color: col.clone(), transparent: true, opacity: 1, blending: THREE.AdditiveBlending, depthWrite: false }));
    const spokes = new THREE.LineSegments(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(pts.slice((k + 1)*3)), 3)),
      new THREE.LineBasicMaterial({ color: col.clone(), transparent: true, opacity: 0.6, blending: THREE.AdditiveBlending, depthWrite: false }));
    const fill = new THREE.Mesh(new THREE.CircleGeometry(1, k), new THREE.MeshBasicMaterial({ color: col.clone(), transparent: true, opacity: 0.18, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
    const rad = ring.reduce((s, p) => s + Math.hypot(p.x - c.x, p.y - c.y), 0)/k; fill.position.set(c.x, c.y, c.z + 0.3); fill.scale.setScalar(0.01); fill.userData.rad = rad;
    group.add(poly, spokes, fill); live.push({ parts: [poly, spokes, fill], born: performance.now()/1000, k });
  }
  function frame(now) {
    requestAnimationFrame(frame); if (!on) return;
    const t = now/1000, u = ((t - t0)/PASS_S) % 1, p = Math.floor((t - t0)/PASS_S), hue = HUES[p % HUES.length];
    const y = Y0 + (Y1 - Y0)*u;
    if (p !== pass) { pass = p; prevY = Y0; }
    col.setHSL(hue, 1, 0.62); frontMat.color.copy(col); glowMat.color.copy(col);
    const a = frontGeo.attributes.position;
    for (let i = 0; i < FN; i++) { const x = -110 + 220*i/(FN - 1); a.setXYZ(i, x, y + 1.2*Math.sin(x*0.08 + t*3), 1.5 + 1.2*Math.sin(x*0.05 - t*2)); }
    a.needsUpdate = true; glow.position.set(0, y, 0.8);
    for (let i = 0; i < N; i++) { const ny = knobs[i].position.y; if (ny > prevY && ny <= y) shape(i, hue); }   // the front passes node i
    prevY = y;
    live = live.filter(s => {
      const age = t - s.born, f = Math.max(0, 1 - age/FADE_S);
      s.parts[0].material.opacity = f; s.parts[1].material.opacity = 0.6*f;
      const fill = s.parts[2]; fill.material.opacity = 0.08*f; fill.scale.setScalar(fill.userData.rad*Math.min(1, age*3));   // the tile grows into place
      if (f <= 0) { s.parts.forEach(o => { group.remove(o); o.geometry.dispose(); o.material.dispose(); }); return false; }
      return true;
    });
  }
  requestAnimationFrame(frame);
  function set(v) {
    on = v; group.visible = v; btn.setAttribute('aria-checked', String(v)); btn.classList.toggle('on', v); btn.textContent = v ? 'Wavefront: on' : 'Wavefront: off';
    if (v) { t0 = performance.now()/1000; pass = 0; prevY = Y0; }
    try { localStorage.setItem('janus.wavefront', v ? '1' : '0'); } catch (e) {}
  }
  btn.onclick = () => set(!on);
  try { if (localStorage.getItem('janus.wavefront') === '1') set(true); } catch (e) {}
})();
