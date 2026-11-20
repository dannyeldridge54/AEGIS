/* AEGIS Control Panel — lesson timeline, 3D loom, waveforms, tool cards (item M, first scaffold). */
(async function () {
  const $ = s => document.querySelector(s);
  let L;
  try { L = await (await fetch('lessons.json')).json(); }
  catch (e) { L = window.AEGIS_LESSONS || { steps: [] }; }
  const steps = L.steps;

  /* ---------- tabs ---------- */
  document.querySelectorAll('nav button').forEach(b => b.onclick = () => {
    document.querySelectorAll('nav button').forEach(x => x.setAttribute('aria-selected', x === b));
    document.querySelectorAll('main section').forEach(s => s.hidden = s.id !== 'tab-' + b.dataset.tab);
    if (b.dataset.tab === 'lesson') resize();
  });

  /* ---------- lesson ---------- */
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const tagName = { established: 'established', weave: 'Weave', open: 'open' };
  $('#steps').innerHTML = steps.map((s, i) => `<button data-i="${i}">${esc(s.t)} · ${esc(s.title)}</button>`).join('');
  function show(i) {
    const s = steps[i]; if (!s) return;
    $('#lesson').innerHTML = `<div class="mono dim">${esc(s.t)} · step ${i + 1}/${steps.length} · tool: ${esc(s.tool)}</div><h1>${esc(s.title)}</h1>` +
      s.lines.map(([t, x]) => `<div class="line"><span class="tag t-${t}">${tagName[t]}</span><span>${esc(x)}</span></div>`).join('') +
      `<div class="eq">${esc(s.eq)}</div>`;
    document.querySelectorAll('#steps button').forEach((b, j) => b.classList.toggle('on', j === i));
  }
  function stepAt(p) { let k = 0; steps.forEach((s, i) => { if (p >= s.phase - 1e-9) k = i; }); return k; }
  $('#steps').onclick = e => { const b = e.target.closest('button'); if (!b) return; const i = +b.dataset.i; $('#t').value = Math.round(steps[i].phase * 1000); show(i); };
  $('#t').oninput = () => show(stepAt($('#t').value / 1000));
  show(stepAt($('#t').value / 1000));

  /* ---------- 3D loom ---------- */
  const cv = $('#loom'), R = new THREE.WebGLRenderer({ canvas: cv, antialias: true });
  R.setPixelRatio(Math.min(2, devicePixelRatio));
  const scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(45, 2, 0.1, 200);
  cam.position.set(0, 2.6, 12.5);
  const ctl = new THREE.OrbitControls(cam, cv); ctl.enableDamping = true; ctl.autoRotate = !matchMedia('(prefers-reduced-motion: reduce)').matches; ctl.autoRotateSpeed = 0.4;
  const comp = new THREE.EffectComposer(R); comp.addPass(new THREE.RenderPass(scene, cam));
  const bloom = new THREE.UnrealBloomPass(new THREE.Vector2(512, 512), 1.2, 0.5, 0.05); comp.addPass(bloom);
  const X0 = -7, X1 = 7, N = 600;
  function strand(phase, c0, c1, rad) {
    const pts = [], cols = [], a = new THREE.Color(c0), b = new THREE.Color(c1);
    for (let i = 0; i <= N; i++) {
      const u = i / N, x = X0 + (X1 - X0) * u, r = rad * (0.35 + 0.65 * Math.sin(Math.PI * u) ** 0.6), th = u * Math.PI * 14 + phase;
      pts.push(x, r * Math.cos(th), r * Math.sin(th)); const c = a.clone().lerp(b, u); cols.push(c.r, c.g, c.b);
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
    const l = new THREE.Line(g, new THREE.LineBasicMaterial({ vertexColors: true })); scene.add(l); return l;
  }
  const strands = [strand(0, '#2f8bff', '#7a5cff', 1.6), strand(Math.PI, '#d43cff', '#ff6ec7', 1.6),
                   strand(Math.PI / 2, '#ff4d6d', '#3ddc97', 0.9), strand(-Math.PI / 2, '#3ddc97', '#4d7cff', 0.9)];
  // rungs of the ladder (cross-bars between the two main strands)
  for (let k = 0; k < 40; k++) {
    const u = k / 39, x = X0 + (X1 - X0) * u, r = 1.6 * (0.35 + 0.65 * Math.sin(Math.PI * u) ** 0.6), th = u * Math.PI * 14;
    const g = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(x, r * Math.cos(th), r * Math.sin(th)), new THREE.Vector3(x, -r * Math.cos(th), -r * Math.sin(th))]);
    scene.add(new THREE.Line(g, new THREE.LineBasicMaterial({ color: 0x3a3380, transparent: true, opacity: 0.55 })));
  }
  const knot = (x, col, s) => { const m = new THREE.Mesh(new THREE.SphereGeometry(s, 32, 16), new THREE.MeshBasicMaterial({ color: col })); m.position.set(x, 0, 0); scene.add(m); return m; };
  knot(X0, 0x6fb8ff, 0.32); knot(X1, 0xd43cff, 0.32);   // ρ (start) and i (end)
  const now = knot(0, 0xffffff, 0.2);
  const stars = new THREE.BufferGeometry(), sp = [];
  for (let i = 0; i < 1500; i++) sp.push((Math.random() - .5) * 120, (Math.random() - .5) * 80, -20 - Math.random() * 60);
  stars.setAttribute('position', new THREE.Float32BufferAttribute(sp, 3)); scene.add(new THREE.Points(stars, new THREE.PointsMaterial({ color: 0x6a64b0, size: 0.12 })));
  function resize() { const w = cv.clientWidth, h = cv.clientHeight; if (!w) return; R.setSize(w, h, false); comp.setSize(w, h); cam.aspect = w / h; cam.updateProjectionMatrix(); }
  addEventListener('resize', resize); resize();
  let t0 = performance.now();
  (function loop(t) {
    const p = $('#t').value / 1000, u = p, x = X0 + (X1 - X0) * u, r = 1.6 * (0.35 + 0.65 * Math.sin(Math.PI * u) ** 0.6), th = u * Math.PI * 14 + (t - t0) / 900;
    now.position.set(x, r * Math.cos(th), r * Math.sin(th));
    strands.forEach((s, i) => s.rotation.x = Math.sin((t - t0) / 4000 + i) * 0.05);
    ctl.update(); comp.render(); requestAnimationFrame(loop);
  })(t0);

  /* ---------- waveforms ---------- */
  function wave(id, f, col, xr) {
    const c = $(id), d = devicePixelRatio || 1, w = c.clientWidth * d, h = c.clientHeight * d; c.width = w; c.height = h;
    const g = c.getContext('2d'); g.lineWidth = 2 * d; const grad = g.createLinearGradient(0, 0, w, 0); col.forEach((cc, i) => grad.addColorStop(i / (col.length - 1), cc)); g.strokeStyle = grad;
    const ys = []; for (let i = 0; i <= 300; i++) ys.push(f(xr[0] + (xr[1] - xr[0]) * i / 300));
    const lo = Math.min(...ys), hi = Math.max(...ys); g.beginPath();
    ys.forEach((y, i) => { const X = i / 300 * w, Y = h - 8 * d - (y - lo) / (hi - lo || 1) * (h - 16 * d); i ? g.lineTo(X, Y) : g.moveTo(X, Y); }); g.stroke();
  }
  function drawWaves() {
    wave('#w1', lk => (0.9706 - 1) * lk, ['#2f8bff', '#7a5cff'], [-4, 0]);                      // log P vs log k (tilted)
    wave('#w2', t => Math.exp(-t / 6) * Math.cos(t * 2.2), ['#d43cff', '#ff6ec7'], [0, 30]);     // settling oscillation
    wave('#w3', z => -1 + 0.21 * Math.exp(-1.6 * z), ['#3ddc97', '#4d7cff'], [3, 0]);              // w(z) thawing toward today
  }
  drawWaves(); addEventListener('resize', drawWaves);

  /* ---------- tool cards ---------- */
  const TOOLS = [
    ['Janus', 'Inflation & CMB', 'Computes n_s, r, α_s for each inflation model with exact Mukhanov–Sasaki spectra; compares with Planck/ACT/SPT and BICEP limits.', 'n_s 0.9706 (fitted), r 5.4e-4 (prediction)', 'V(τ₁) on the SERAPIS-Λ plateau'],
    ['Hyperion', 'BBN, neutrinos, dark matter, stars', 'Big Bang nucleosynthesis with PRIMAT theory errors, relic neutrinos, galaxy J-factors and neutron-star structure.', 'Y_p 0.247, D/H 2.45e-5, relic ν 336 /cm³', 'Y_p(ω_b, ΔN_eff)'],
    ['CERN+1', 'Colliders', 'Wino production and disappearing-track reach for LHC runs; compares with the ATLAS limit (670 GeV).', 'wino 1 TeV: σ 2.4 fb, reach 740 GeV', 'σ(pp → χ⁺χ⁻)'],
    ['Mapper', 'Sky & observing', 'Finder charts, targets and the observing planner; carries science targets from the galaxy level.', 'targets from the Galaxy level', '—'],
    ['Weave Control', 'All levels together', 'One model driving every toolkit level by level, with pulls against data and the Evidence Atlas.', 'strict score: 1 pass, 2 tension, 1 fail, 1 open', 'run(params) → levels + scorecard'],
    ['Quarks (slip ladder)', 'Flavour', 'Twin slip-ladder: down quarks on rung 1, up quarks ~8 (5–14), leptons at the knot; CKM from the split; θ̄ = 0.', 'best χ² 5.8; misses m_s/m_b, V_cb, V_ub', 'ε_m = 0.0251 e^{i50°}/(m + 1/16)']];
  $('#toolcards').innerHTML = TOOLS.map(([n, a, w, d, e]) => `<div class="card tool"><h3>${esc(n)}</h3><div class="kv">${esc(a)}</div><p>${esc(w)}</p><p class="kv">our data: ${esc(d)}</p><div class="eq">${esc(e)}</div></div>`).join('');
})();
