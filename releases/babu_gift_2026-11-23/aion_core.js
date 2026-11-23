// Aion core (same algorithm as aion.py). Danny Lee Eldridge / the Weave, D2188. Free to use.
const A = (() => {
  const C = (re, im = 0) => ({ re, im }), add = (a, b) => C(a.re + b.re, a.im + b.im), mul = (a, b) => C(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re),
    sc = (a, s) => C(a.re * s, a.im * s), ab = a => Math.hypot(a.re, a.im), ex = t => C(Math.cos(t), Math.sin(t));
  const NUFIT6 = { NO: { s12: .307, s23: .561, s13: .02195, d: 177, dm21: 7.49e-5, dm3l: 2.534e-3 }, IO: { s12: .308, s23: .562, s13: .02224, d: 285, dm21: 7.49e-5, dm3l: -2.510e-3 } };
  const ALPHA = 1 / 137.036, GF = 1.1663788e-5, MEG2 = 1.5e-13, DESI = 0.0642;
  function fRatios(o, p) {
    const t12 = Math.sqrt(p.s12 / (1 - p.s12)), t13 = Math.sqrt(p.s13 / (1 - p.s13)), c23 = Math.sqrt(1 - p.s23), s23 = Math.sqrt(p.s23), c13 = Math.sqrt(1 - p.s13), e = ex(-p.d * Math.PI / 180);
    if (o === 'NO') return [add(C(t12 * c23 / c13), sc(e, t13 * s23)), add(C(t12 * s23 / c13), sc(e, -t13 * c23))];
    return [sc(e, -s23 / t13), sc(e, c23 / t13)];
  }
  function hBR(r) { const et = ab(r[0]) ** 2, em = ab(r[1]) ** 2, w = [em + et, em + 1, et + 1], s = w[0] + w[1] + w[2]; return w.map(x => x / s); }
  function masses(o, p) { if (o === 'NO') return [0, Math.sqrt(p.dm21), Math.sqrt(p.dm3l)]; const m2 = Math.sqrt(-p.dm3l); return [Math.sqrt(m2 * m2 - p.dm21), m2, 0]; }
  function Ue(p) { // first row of PDG U: c12c13, s12c13, s13 e^{-i d}
    const c12 = Math.sqrt(1 - p.s12), s12 = Math.sqrt(p.s12), c13 = Math.sqrt(1 - p.s13), s13 = Math.sqrt(p.s13);
    return [C(c12 * c13), C(s12 * c13), sc(ex(-p.d * Math.PI / 180), s13)];
  }
  function mbb(o, p, a) { const u = Ue(p), m = masses(o, p), ph = [C(1), ex(a), C(1)]; let s = C(0); for (let i = 0; i < 3; i++) s = add(s, sc(mul(mul(u[i], u[i]), ph[i]), m[i])); return ab(s); }
  function mbbBand(o, p, n = 721) { let lo = 1e9, hi = 0; for (let i = 0; i < n; i++) { const v = mbb(o, p, 2 * Math.PI * i / (n - 1)); lo = Math.min(lo, v); hi = Math.max(hi, v); } return [lo, hi]; }
  function ceiling(r, mhTeV) { const mh = mhTeV * 1e3, ff2 = MEG2 * 48 * Math.PI * GF * GF * mh ** 4 / ALPHA; return Math.sqrt(Math.sqrt(ff2) / ab(r[0])); }
  function run(o, p) { const r = fRatios(o, p), m = masses(o, p), b = mbbBand(o, p); return { r, abs: [ab(r[0]), ab(r[1])], br: hBR(r), mbb: b, sum: m[0] + m[1] + m[2], m, ceil: [0.5, 1, 2, 5].map(x => [x, ceiling(r, x)]) }; }
  return { NUFIT6, DESI, MEG2, fRatios, hBR, masses, mbb, mbbBand, ceiling, run };
})();
if (typeof module !== 'undefined') module.exports = A;
