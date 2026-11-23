// CM-IRIS DEV-3 edge checks E1-E5 and I1b (sub-pixel fidelity). Reported separately from the locked I1-I4.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const iris = fs.readFileSync(path.join(__dirname, '..', 'iris.js'), 'utf8');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.setContent('<canvas id="c" style="width:900px;height:340px;display:block"></canvas>'); await p.addScriptTag({ content: iris });
  const r = await p.evaluate(() => {
    const cv = document.getElementById('c'), R = (spec) => Iris.render(cv, spec, { instant: true, dpr: 2 }), o = {};
    let a = R({ title: 'dec', series: [{ name: 'd', x: [10, 8, 6, 4, 2], y: [1, 2, 3, 4, 5] }] });
    o.E1_decreasing = [9, 5, 3].map(x => a.valueAt(0, x)).every((v, i) => Math.abs(v - [1.5, 3.5, 4.5][i]) < 1e-12);
    a = R({ title: 'nan', series: [{ name: 'n', x: [0, 1, NaN, 3, 4], y: [0, 1, 2, 3, 4] }] }); o.E2_nan_x = Math.abs(a.valueAt(0, 3.5) - 3.5) < 1e-12;
    a = R({ title: 'null', series: [{ name: 'n', x: [0, 1, 2, 3, 4], y: [0, 1, null, 3, 4] }] }); o.E3_null_y = Math.abs(a.valueAt(0, 2) - 2) < 1e-12;
    a = R({ title: 'log', logy: true, series: [{ name: 'neg', x: [0, 1], y: [-1, -2] }, { name: 'ok', x: [0, 1, 2], y: [1, 100, 10000] }] });
    o.E4_logy_index = Math.abs(a.valueAt(1, 0.5) - 10) < 1e-9 && Number.isNaN(a.valueAt(0, 0.5));
    a = R({ title: 'one', series: [{ name: 'p', x: [1], y: [2] }] }); const d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
    let lit = 0; for (let i = 0; i < d.length; i += 4) if (d[i] > 150 && d[i + 2] > 200 && d[i + 1] < 170) lit++; o.E5_single_point_visible = lit > 10;
    // I1b: sub-pixel deviation on a noisy 20k series
    const N = 20000, t = Array.from({ length: N }, (_, i) => 50 * i / (N - 1)); let sd = 7; const rr = () => ((sd = (sd * 1103515245 + 12345) % 2147483648) / 2147483648);
    a = R({ title: 'noisy', series: [{ name: 'N', x: t, y: t.map(v => Math.sin(v) + 0.3 * (rr() - 0.5)) }] });
    const L = a.layout, S = L.ser[0], fx = S.X.map(L.px), fy = S.Y.map(L.py), P = S.P, n = P.length / 2, dx = [], dy = [];
    for (let j = 0; j < n; j++) { dx.push(P[2 * j]); dy.push(P[2 * j + 1]); }
    const ip = (xs, ys, X) => { let lo = 0, hi = xs.length - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (xs[m] <= X) lo = m; else hi = m; } const q = (X - xs[lo]) / ((xs[hi] - xs[lo]) || 1); return ys[lo] + q * (ys[hi] - ys[lo]); };
    // compare per-column vertical EXTENT (what the rasteriser paints) of full vs decimated polyline
    let worst = 0; const c0 = Math.ceil(fx[0]), c1 = Math.floor(fx[fx.length - 1]);
    const ext = (xs, ys, c) => { let lo = Infinity, hi = -Infinity; for (let k = 0; k <= 8; k++) { const v = ip(xs, ys, c + k / 8); lo = Math.min(lo, v); hi = Math.max(hi, v); }
      for (let i = 0; i < xs.length; i++) if (xs[i] >= c && xs[i] < c + 1) { lo = Math.min(lo, ys[i]); hi = Math.max(hi, ys[i]); } return [lo, hi]; };
    for (let c = c0; c < c1; c++) { const A = ext(fx, fy, c), B = ext(dx, dy, c); worst = Math.max(worst, Math.abs(A[0] - B[0]), Math.abs(A[1] - B[1])); }
    o.I1b_column_extent_dev_px = worst;
    return o;
  });
  r.page_errors = errs; r.PASS = r.E1_decreasing && r.E2_nan_x && r.E3_null_y && r.E4_logy_index && r.E5_single_point_visible && r.I1b_column_extent_dev_px <= 1.5 && !errs.length;
  console.log(JSON.stringify(r, null, 1)); fs.writeFileSync(path.join(__dirname, '..', '..', '..', '..', 'field_tests', 'results', 'cm_iris_dev3.json'), JSON.stringify(r, null, 1)); await b.close();
})();
