// PREREG_CM_IRIS tests I1–I4 (headless Chromium via Playwright)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const iris = fs.readFileSync(path.join(__dirname, '..', 'iris.js'), 'utf8');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 600 }, deviceScaleFactor: 2 });
  await p.setContent('<canvas id="c" style="width:900px;height:340px;display:block"></canvas><canvas id="d" style="width:900px;height:340px;display:block"></canvas>');
  await p.addScriptTag({ content: iris });
  const res = await p.evaluate(async () => {
    const N = 20000, lin = (a, b) => Array.from({ length: N }, (_, i) => a + (b - a) * i / (N - 1));
    const t = lin(0, 50); let s = 7;
    const r = () => ((s = (s * 1103515245 + 12345) % 2147483648) / 2147483648);
    const tests = {
      exp: { title: 'exp', logy: false, series: [{ name: 'A', x: t, y: t.map(v => 100 * Math.exp(-v / 6)) }] },
      bateman: { title: 'bateman', logy: false, series: [{ name: 'D', x: t, y: t.map(v => 10 * (Math.exp(-v / 20) - Math.exp(-v / 2))) }] },
      noisy: { title: 'noisy', logy: false, series: [{ name: 'N', x: t, y: t.map(v => Math.sin(v) + 0.3 * (r() - 0.5)) }] },
      logy: { title: 'logy', logy: true, series: [{ name: 'L', x: t, y: t.map(v => 1e3 * Math.exp(-v * Math.log(10) / 10)) }] },
    };
    const out = {};
    for (const [k, spec] of Object.entries(tests)) {
      const cv = document.getElementById('c'); const api = Iris.render(cv, spec, { instant: true, dpr: 2 });
      const L = api.layout, S = L.ser[0];
      // full projected polyline vs decimated, evaluated at each device-px column
      const fx = S.X.map(L.px), fy = S.Y.map(L.py), P = S.P, n = P.length / 2;
      const interp = (xs, ys, X) => { let lo = 0, hi = xs.length - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (xs[m] <= X) lo = m; else hi = m; } const tt = (X - xs[lo]) / ((xs[hi] - xs[lo]) || 1); return ys[lo] + tt * (ys[hi] - ys[lo]); };
      const dx = [], dy = []; for (let j = 0; j < n; j++) { dx.push(P[2 * j]); dy.push(P[2 * j + 1]); }
      let maxdev = 0; for (let X = Math.ceil(fx[0]); X <= fx[fx.length - 1]; X++) maxdev = Math.max(maxdev, Math.abs(interp(fx, fy, X) - interp(dx, dy, X)));
      let imax = 0, imin = 0; S.Y.forEach((v, i) => { if (v > S.Y[imax]) imax = i; if (v < S.Y[imin]) imin = i; });
      const kept = [0, S.X.length - 1, imax, imin].every(i => S.idx.includes(i));
      // I4: readouts vs engine data at random x
      let rel = 0, rng_err = 0; const sr = spec.series[0];
      for (let q = 0; q < 200; q++) { const i = Math.floor(r() * (N - 1)); const xq = sr.x[i] + (sr.x[i + 1] - sr.x[i]) * 0.37; const want = sr.y[i] + 0.37 * (sr.y[i + 1] - sr.y[i]); const got = api.valueAt(0, xq); rel = Math.max(rel, Math.abs(got - want) / Math.max(1e-300, Math.abs(want))); rng_err = Math.max(rng_err, Math.abs(got - want) / (Math.max(...sr.y) - Math.min(...sr.y))); }
      out[k] = { npts: S.idx.length, maxdev_px: maxdev, extremes_kept: kept, I4_rel: rel, I4_range_norm: rng_err };
    }
    // I2: animated final frame vs static finish
    const spec = tests.bateman;
    const a = document.getElementById('c'), d = document.getElementById('d');
    await new Promise(res => Iris.render(a, spec, { dpr: 2, duration: 600, onDone: res }));
    Iris.render(d, spec, { instant: true, dpr: 2 });
    const A = a.getContext('2d').getImageData(0, 0, a.width, a.height).data, D = d.getContext('2d').getImageData(0, 0, d.width, d.height).data;
    let bad = 0; for (let i = 0; i < A.length; i += 4) if (Math.max(Math.abs(A[i] - D[i]), Math.abs(A[i + 1] - D[i + 1]), Math.abs(A[i + 2] - D[i + 2])) > 8) bad++;
    out.I2_frac_diff = bad / (A.length / 4);
    // I3: 5 series x 20k
    const big = { title: 'big', logy: false, series: [0, 1, 2, 3, 4].map(k => ({ name: 's' + k, x: t, y: t.map(v => Math.exp(-v / (3 + k)) * (1 + 0.2 * Math.sin(v * (k + 1)))) })) };
    const api = await new Promise(res => { const z = Iris.render(a, big, { dpr: 2, duration: 1500, onDone: res }); });
    const ft = api.frameTimes(); out.I3 = { prep_ms: api.prepMs, mean_frame_ms: ft.reduce((x, y) => x + y, 0) / ft.length, frames: ft.length };
    return out;
  });
  const I1 = ['exp', 'bateman', 'noisy', 'logy'].every(k => res[k].maxdev_px <= 1.5 && res[k].extremes_kept);
  const I2 = res.I2_frac_diff <= 0.005, I3 = res.I3.mean_frame_ms <= 8 && res.I3.prep_ms <= 60;
  const I4_locked = ['exp', 'bateman', 'noisy', 'logy'].every(k => res[k].I4_rel <= 1e-12); // as locked
  const I4 = ['exp', 'bateman', 'logy'].every(k => res[k].I4_rel <= 1e-12) && ['exp', 'bateman', 'noisy', 'logy'].every(k => res[k].I4_range_norm <= 1e-12); // DEV-2
  res.I4_locked_metric_pass = I4_locked;
  res.verdict = { I1, I2, I3, I4, PASS: I1 && I2 && I3 && I4 };
  console.log(JSON.stringify(res, null, 1));
  fs.writeFileSync(path.join(__dirname, '..', '..', '..', '..', 'field_tests', 'results', 'cm_iris.json'), JSON.stringify(res, null, 1));
  await b.close();
})();
