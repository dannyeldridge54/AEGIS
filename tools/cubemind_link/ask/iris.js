/* Iris — animated chart generator for CubeMind Ask (PREREG_CM_IRIS).
   Draws engine chart specs {title,x_label,y_label,logy,series[{name,x,y}]} as animated art.
   The renderer never changes a number: readouts interpolate the FULL engine series.
   Speed rung: M4 decimation (<= 4 pts / device px column; LTTB kept for reference, see DEVIATIONS), one Float32Array projection,
   pre-rendered series layer; each frame is two blits + a clip + a few sparks (O(1) in N). */
(function (G) {
  'use strict';
  const PAL = ['#b18cff', '#e0b24a', '#4cc3ff', '#ff6fa8', '#7ee787', '#ff9f5a'];

  // ---- LTTB (largest-triangle-three-buckets); keeps endpoints; extremes re-inserted ----
  function lttb(x, y, n) {
    const N = x.length;
    if (n >= N || n < 3) return Array.from({ length: N }, (_, i) => i);
    const out = [0], every = (N - 2) / (n - 2);
    let a = 0;
    for (let i = 0; i < n - 2; i++) {
      let s = Math.floor((i + 1) * every) + 1, e = Math.min(Math.floor((i + 2) * every) + 1, N);
      let ax = 0, ay = 0; const len = e - s;
      for (let j = s; j < e; j++) { ax += x[j]; ay += y[j]; }
      ax /= len || 1; ay /= len || 1;
      const rs = Math.floor(i * every) + 1, re = Math.floor((i + 1) * every) + 1;
      let best = -1, bi = rs;
      for (let j = rs; j < re; j++) {
        const ar = Math.abs((x[a] - ax) * (y[j] - y[a]) - (x[a] - x[j]) * (ay - y[a]));
        if (ar > best) { best = ar; bi = j; }
      }
      out.push(bi); a = bi;
    }
    out.push(N - 1);
    let imax = 0, imin = 0;
    for (let i = 1; i < N; i++) { if (y[i] > y[imax]) imax = i; if (y[i] < y[imin]) imin = i; }
    for (const k of [imax, imin]) if (!out.includes(k)) out.push(k);
    return out.sort((p, q) => p - q);
  }

  // ---- M4 decimation (DEV-1): per device-px column keep first, last, min, max ----
  function m4(PX, y) {
    const N = PX.length, out = []; if (!N) return out;
    let c = Math.floor(PX[0]), f = 0, l = 0, mn = 0, mx = 0;
    const flush = () => { const k = [f, mn, mx, l].sort((a, b) => a - b); for (const i of k) if (out[out.length - 1] !== i) out.push(i); };
    for (let i = 1; i < N; i++) {
      const ci = Math.floor(PX[i]);
      if (ci !== c) { flush(); c = ci; f = l = mn = mx = i; continue; }
      l = i; if (y[i] < y[mn]) mn = i; if (y[i] > y[mx]) mx = i;
    }
    flush(); return out;
  }

  // ---- number formatting / ticks ----
  const fmt = v => {
    if (v === 0) return '0';
    const a = Math.abs(v);
    if (a >= 1e5 || a < 1e-3) { const e = Math.floor(Math.log10(a)), m = v / 10 ** e; return (+m.toFixed(2)) + 'e' + e; }
    return (+v.toPrecision(4)).toString();
  };
  function niceTicks(a, b, n) {
    const span = b - a || 1, step0 = span / n, p = 10 ** Math.floor(Math.log10(step0));
    const step = [1, 2, 2.5, 5, 10].map(m => m * p).find(s => s >= step0) || p * 10;
    const t = []; for (let v = Math.ceil(a / step) * step; v <= b + step * 1e-9; v += step) t.push(+v.toPrecision(12));
    return t;
  }
  function rng(seed) { let s = seed >>> 0 || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

  function prepare(spec, W, H, dpr) {
    const M = { l: 92 * dpr, r: 24 * dpr, t: 54 * dpr, b: 58 * dpr };
    const PW = W - M.l - M.r, PH = H - M.t - M.b, logy = !!spec.logy;
    const ser = spec.series.map(s => {   // DEV-3: clean (finite, non-null, y>0 for logy) and sort by x; empty series kept as placeholders
      const pts = [];
      for (let i = 0; i < Math.min(s.x.length, s.y.length); i++) {
        if (s.x[i] == null || s.y[i] == null || s.x[i] === '' || s.y[i] === '') continue; const xv = +s.x[i], yv = +s.y[i];
        if (!Number.isFinite(xv) || !Number.isFinite(yv) || (logy && !(yv > 0))) continue; pts.push([xv, yv]);
      }
      pts.sort((a, b) => a[0] - b[0]);
      const rawX = pts.map(p => p[0]), rawY = pts.map(p => p[1]);
      return { name: s.name, X: rawX.slice(), Y: rawY.map(v => logy ? Math.log10(v) : v), rawX, rawY, logy };
    });
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    ser.forEach(s => { for (let i = 0; i < s.X.length; i++) { const a = s.X[i], b = s.Y[i]; if (a < x0) x0 = a; if (a > x1) x1 = a; if (b < y0) y0 = b; if (b > y1) y1 = b; } });
    if (!isFinite(x0)) { x0 = 0; x1 = 1; y0 = 0; y1 = 1; }
    if (x1 === x0) x1 = x0 + 1; if (y1 === y0) { y0 -= 0.5; y1 += 0.5; }
    const pad = (y1 - y0) * 0.06; y0 -= logy ? 0 : (y0 >= 0 && y0 - pad < 0 ? y0 : pad); y1 += pad;
    const px = v => M.l + PW * (v - x0) / (x1 - x0), py = v => M.t + PH * (1 - (v - y0) / (y1 - y0));
    ser.forEach(s => {
      s.idx = m4(Float64Array.from(s.X, px), s.Y);
      const P = new Float32Array(s.idx.length * 2);
      s.idx.forEach((k, j) => { P[2 * j] = px(s.X[k]); P[2 * j + 1] = py(s.Y[k]); });
      s.P = P;
    });
    return { M, PW, PH, W, H, dpr, x0, x1, y0, y1, px, py, logy, ser };
  }

  function drawBase(g, L, spec, seed) {
    const { M, W, H, PW, PH, dpr } = L;
    const bg = g.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, '#0d0820'); bg.addColorStop(1, '#05030b');
    g.fillStyle = bg; g.fillRect(0, 0, W, H);
    const r = rng(seed); g.fillStyle = '#ffffff';
    for (let i = 0; i < 90; i++) { g.globalAlpha = 0.05 + 0.25 * r() ** 3; g.fillRect(r() * W, r() * H, dpr * (r() < 0.9 ? 1 : 2), dpr * (r() < 0.9 ? 1 : 2)); }
    g.globalAlpha = 1;
    g.font = `${12 * dpr}px Segoe UI, system-ui, sans-serif`; g.fillStyle = '#8f86b8'; g.strokeStyle = 'rgba(177,140,255,0.10)'; g.lineWidth = dpr;
    const xt = niceTicks(L.x0, L.x1, 6);
    g.textAlign = 'center';
    xt.forEach(v => { const X = L.px(v); g.beginPath(); g.moveTo(X, M.t); g.lineTo(X, M.t + PH); g.stroke(); g.fillText(fmt(v), X, M.t + PH + 18 * dpr); });
    g.textAlign = 'right';
    if (L.logy) {
      for (let e = Math.ceil(L.y0); e <= Math.floor(L.y1); e++) { const Y = L.py(e); g.beginPath(); g.moveTo(M.l, Y); g.lineTo(M.l + PW, Y); g.stroke(); g.fillText('1e' + e, M.l - 8 * dpr, Y + 4 * dpr); }
    } else niceTicks(L.y0, L.y1, 5).forEach(v => { const Y = L.py(v); g.beginPath(); g.moveTo(M.l, Y); g.lineTo(M.l + PW, Y); g.stroke(); g.fillText(fmt(v), M.l - 8 * dpr, Y + 4 * dpr); });
    g.strokeStyle = '#3a2c62'; g.lineWidth = 1.5 * dpr; g.beginPath(); g.moveTo(M.l, M.t); g.lineTo(M.l, M.t + PH); g.lineTo(M.l + PW, M.t + PH); g.stroke();
    g.textAlign = 'left'; g.fillStyle = '#ece6ff'; g.font = `600 ${15 * dpr}px Segoe UI, system-ui, sans-serif`; g.fillText(spec.title || '', M.l, 24 * dpr);
    g.fillStyle = '#a69ccc'; g.font = `${12 * dpr}px Segoe UI, system-ui, sans-serif`;
    g.textAlign = 'center'; g.fillText(spec.x_label || '', M.l + PW / 2, H - 14 * dpr);
    g.save(); g.translate(18 * dpr, M.t + PH / 2); g.rotate(-Math.PI / 2); g.fillText((spec.y_label || '') + (L.logy ? '  (log)' : ''), 0, 0); g.restore();
    g.textAlign = 'right';
    let li = 0; L.ser.forEach((s, k) => { if (!s.X.length) return; g.fillStyle = PAL[k % PAL.length]; g.fillText(s.name + '  ●', M.l + PW, 22 * dpr + 15 * dpr * li++); });
    g.textAlign = 'left';
  }

  function drawSeries(g, L) {
    const { M, PH, dpr } = L, base = M.t + PH;
    L.ser.forEach((s, k) => {
      const c = PAL[k % PAL.length], P = s.P, n = P.length / 2;
      if (!n) return;
      if (n === 1) { g.fillStyle = c; g.beginPath(); g.arc(P[0], P[1], 4 * dpr, 0, 7); g.fill(); return; }
      const grad = g.createLinearGradient(0, M.t, 0, base); grad.addColorStop(0, c + '55'); grad.addColorStop(1, c + '00');
      g.beginPath(); g.moveTo(P[0], base); for (let j = 0; j < n; j++) g.lineTo(P[2 * j], P[2 * j + 1]); g.lineTo(P[2 * n - 2], base); g.closePath(); g.fillStyle = grad; g.fill();
      const path = () => { g.beginPath(); g.moveTo(P[0], P[1]); for (let j = 1; j < n; j++) g.lineTo(P[2 * j], P[2 * j + 1]); };
      g.lineJoin = 'round'; g.lineCap = 'round';
      path(); g.strokeStyle = c + '33'; g.lineWidth = 9 * dpr; g.stroke();
      path(); g.strokeStyle = c + '77'; g.lineWidth = 4.5 * dpr; g.stroke();
      path(); g.strokeStyle = c; g.lineWidth = 2 * dpr; g.stroke();
    });
  }

  function headAt(s, X) { // position of series at plot-x X (on decimated path; for the tracer only)
    const P = s.P, n = P.length / 2; if (!n) return null; if (X <= P[0]) return [P[0], P[1]]; if (X >= P[2 * n - 2]) return [P[2 * n - 2], P[2 * n - 1]];
    let lo = 0, hi = n - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (P[2 * m] <= X) lo = m; else hi = m; }
    const t = (X - P[2 * lo]) / ((P[2 * hi] - P[2 * lo]) || 1); return [P[2 * lo] + t * (P[2 * hi] - P[2 * lo]), P[2 * lo + 1] + t * (P[2 * hi + 1] - P[2 * lo + 1])];
  }

  // value of the FULL engine series at data-x (linear interpolation) — used for readouts (I4)
  function valueAt(s, x) {
    if (!s) return NaN; const X = s.rawX, Y = s.rawY, n = X.length; if (!n || !Number.isFinite(x)) return NaN;
    if (x <= X[0]) return Y[0]; if (x >= X[n - 1]) return Y[n - 1];
    let lo = 0, hi = n - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (X[m] <= x) lo = m; else hi = m; }
    const t = (x - X[lo]) / ((X[hi] - X[lo]) || 1);
    if (s.logy) return 10 ** (Math.log10(Y[lo]) + t * (Math.log10(Y[hi]) - Math.log10(Y[lo])));   // DEV-3: match the drawn log curve
    return Y[lo] + t * (Y[hi] - Y[lo]);
  }

  function render(cv, spec, opts = {}) {
    const dpr = opts.dpr || Math.min(2, G.devicePixelRatio || 1);
    const cw = cv.clientWidth || 800, ch = cv.clientHeight || 340;
    const W = cv.width = Math.round(cw * dpr), H = cv.height = Math.round(ch * dpr);
    const t0 = performance.now();
    const L = prepare(spec, W, H, dpr);
    const mk = () => { const c = document.createElement('canvas'); c.width = W; c.height = H; return c; };
    const base = mk(), layer = mk();
    drawBase(base.getContext('2d'), L, spec, (spec.title || '').length * 7919 + 13);
    drawSeries(layer.getContext('2d'), L);
    const prepMs = performance.now() - t0;
    const g = cv.getContext('2d');
    const reduce = opts.instant || (G.matchMedia && G.matchMedia('(prefers-reduced-motion: reduce)').matches);
    const DUR = opts.duration || 1800, stag = 140, R = rng(99);
    let sparks = [], raf = 0, start = 0, done = false, hover = null, frameTimes = [];
    const { M, PW, PH } = L;

    function compose(frac) {
      g.drawImage(base, 0, 0);
      if (frac >= 1) { g.drawImage(layer, 0, 0); return; }
      g.save(); g.beginPath(); g.rect(0, 0, M.l + PW * frac, H); g.clip(); g.drawImage(layer, 0, 0); g.restore();
    }
    function overlay() {
      if (!hover) return; const X = hover;
      const xd = L.x0 + (X - M.l) / PW * (L.x1 - L.x0);
      g.strokeStyle = 'rgba(236,230,255,0.35)'; g.lineWidth = dpr; g.setLineDash([4 * dpr, 4 * dpr]); g.beginPath(); g.moveTo(X, M.t); g.lineTo(X, M.t + PH); g.stroke(); g.setLineDash([]);
      const lines = ['x = ' + fmt(xd)];
      L.ser.forEach((s, k) => { if (!s.X.length) return; const v = valueAt(s, xd); lines.push(s.name + ' = ' + fmt(v)); const Y = L.py(L.logy ? Math.log10(v) : v); if (isFinite(Y)) { g.fillStyle = PAL[k % PAL.length]; g.beginPath(); g.arc(X, Y, 4 * dpr, 0, 7); g.fill(); } });
      g.font = `${12 * dpr}px Consolas, monospace`; const w = Math.max(...lines.map(t => g.measureText(t).width)) + 16 * dpr, h = lines.length * 16 * dpr + 10 * dpr;
      const bx = Math.min(X + 12 * dpr, M.l + PW - w), by = M.t + 8 * dpr;
      g.fillStyle = 'rgba(13,8,32,0.92)'; g.strokeStyle = '#3a2c62'; g.fillRect(bx, by, w, h); g.strokeRect(bx, by, w, h);
      g.fillStyle = '#ece6ff'; lines.forEach((t, i) => g.fillText(t, bx + 8 * dpr, by + 18 * dpr + i * 16 * dpr));
    }
    function frame(now) {
      const f0 = performance.now();
      if (!start) start = now;
      const el = now - start, lastStag = stag * (L.ser.length - 1);
      const frac = Math.min(1, el / DUR), e = 1 - (1 - frac) ** 3;
      compose(e);
      if (e < 1) L.ser.forEach((s, k) => {
        const fk = Math.min(1, Math.max(0, (el - stag * k) / (DUR - lastStag || DUR))), ek = 1 - (1 - fk) ** 3;
        const hh = headAt(s, M.l + PW * Math.min(e, ek)); if (!hh) return; const [hx, hy] = hh;
        for (let i = 0; i < 2; i++) sparks.push({ x: hx, y: hy, vx: (R() - 0.7) * 1.6 * dpr, vy: (R() - 0.5) * 1.6 * dpr, life: 1, c: PAL[k % PAL.length] });
        const rg = g.createRadialGradient(hx, hy, 0, hx, hy, 14 * dpr); rg.addColorStop(0, '#ffffff'); rg.addColorStop(0.25, PAL[k % PAL.length]); rg.addColorStop(1, 'rgba(0,0,0,0)');
        g.fillStyle = rg; g.beginPath(); g.arc(hx, hy, 14 * dpr, 0, 7); g.fill();
      });
      sparks = sparks.filter(p => (p.life -= 0.035) > 0);
      sparks.forEach(p => { p.x += p.vx; p.y += p.vy; g.globalAlpha = p.life * 0.8; g.fillStyle = p.c; g.fillRect(p.x, p.y, 2 * dpr, 2 * dpr); });
      g.globalAlpha = 1;
      overlay();
      frameTimes.push(performance.now() - f0);
      if (e < 1 || sparks.length) raf = requestAnimationFrame(frame); else { done = true; if (opts.onDone) opts.onDone(api); }
    }
    function finish() { cancelAnimationFrame(raf); sparks = []; done = true; compose(1); overlay(); }
    function replay() { cancelAnimationFrame(raf); start = 0; sparks = []; done = false; frameTimes = []; raf = requestAnimationFrame(frame); }
    cv.onmousemove = ev => { const r = cv.getBoundingClientRect(), X = (ev.clientX - r.left) * dpr; hover = X >= M.l && X <= M.l + PW ? X : null; if (done) { compose(1); overlay(); } };
    cv.onmouseleave = () => { hover = null; if (done) compose(1); };
    const api = { replay, finish, layout: L, prepMs, frameTimes: () => frameTimes, valueAt: (k, x) => valueAt(L.ser[k], x), png: () => cv.toDataURL('image/png') };
    if (reduce) finish(); else replay();
    return api;
  }

  G.Iris = { render, lttb, m4, valueAt, PAL };
})(window);
