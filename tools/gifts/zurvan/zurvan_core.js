// Zurvan core (same algorithm as zurvan.py). Danny Lee Eldridge / the Weave, D2187. Free to use.
const Z = (() => {
  const PI2 = Math.PI * Math.PI;
  const eig2 = (a, b, c) => { const s = 0.5 * (a + b), d = Math.sqrt(0.25 * (a - b) ** 2 + c * c); return [s - d, s + d]; };
  const WARN = new Set();
  const cw = (m2, Q2, n) => { if (m2 === 0) return 0; if (m2 < 0) { WARN.add('a field-dependent mass^2 <= 0 was met (tachyonic sfermion); |m^2| was used, so that term is not reliable'); m2 = Math.abs(m2) + 1e-12; } return n / (64 * PI2) * m2 * m2 * (Math.log(m2 / Q2) - 1.5); };
  const M2 = (p, k) => (p[k + '_2'] !== undefined ? p[k + '_2'] : p[k] ** 2);
  const NOT_INCLUDED = 'first/second-family sfermions, tau sneutrino, charginos/neutralinos, Higgs bosons, W/Z, QCD/gluino corrections to y_t, and all two-loop terms (DEW4SLHA has the 2-loop gluino ones)';
  function sectors(p, vu, vd) {
    const g = p.g, gp = p.gp, gz2 = (g * g + gp * gp) / 2, sw2 = gp * gp / (g * g + gp * gp), D = gz2 * (vd * vd - vu * vu), mu = p.mu, o = {};
    let m = p.yt * vu, LL = M2(p, 'mQ3') + m * m + (0.5 - 2 / 3 * sw2) * D, RR = M2(p, 'mtR') + m * m + (2 / 3 * sw2) * D, LR = p.yt * (p.At * vu - mu * vd), e = eig2(LL, RR, LR);
    o.stop1 = [[e[0], 6]]; o.stop2 = [[e[1], 6]]; o.top = [[m * m, -12]];
    m = p.yb * vd; LL = M2(p, 'mQ3') + m * m + (-0.5 + sw2 / 3) * D; RR = M2(p, 'mbR') + m * m + (-sw2 / 3) * D; LR = p.yb * (p.Ab * vd - mu * vu); e = eig2(LL, RR, LR);
    o.sbottom1 = [[e[0], 6]]; o.sbottom2 = [[e[1], 6]]; o.bottom = [[m * m, -12]];
    m = p.ytau * vd; LL = M2(p, 'mL3') + m * m + (-0.5 + sw2) * D; RR = M2(p, 'meR3') + m * m + (-sw2) * D; LR = p.ytau * (p.Atau * vd - mu * vu); e = eig2(LL, RR, LR);
    o.stau1 = [[e[0], 2]]; o.stau2 = [[e[1], 2]]; o.tau = [[m * m, -4]];
    return o;
  }
  function sigmas(p, h = 1e-4) {
    const Q2 = p.Q ** 2, V = (n, u, d) => sectors(p, u, d)[n].reduce((s, [m2, k]) => s + cw(m2, Q2, k), 0), r = {};
    for (const n of Object.keys(sectors(p, p.vu, p.vd))) {
      const du = h * p.vu, dd = h * p.vd;
      r[n] = [(V(n, p.vu + du, p.vd) - V(n, p.vu - du, p.vd)) / (2 * du) / (2 * p.vu), (V(n, p.vu, p.vd + dd) - V(n, p.vu, p.vd - dd)) / (2 * dd) / (2 * p.vd)];
    }
    return r;
  }
  function deltaEW(p) {
    WARN.clear();
    const t2 = p.tanb ** 2, den = t2 - 1, S = sigmas(p), C = { mu: -(p.mu ** 2), H_u: -p.mHu2 * t2 / den, H_d: p.mHd2 / den };
    for (const [k, [su, sd]] of Object.entries(S)) { C['Sigma_u^u(' + k + ')'] = -su * t2 / den; C['Sigma_d^d(' + k + ')'] = sd / den; }
    const mZ2 = (p.g ** 2 + p.gp ** 2) / 2 * (p.vu ** 2 + p.vd ** 2), ord = Object.entries(C).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));
    const Cs = {}; for (const [k, v] of Object.entries(C)) { const kk = k.replace(/stop[12]/, 'stops').replace(/sbottom[12]/, 'sbottoms').replace(/stau[12]/, 'staus'); Cs[kk] = (Cs[kk] || 0) + v; }
    const os = Object.entries(Cs).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));
    const warns = [...(p.warnings || [])], resid = Object.values(C).reduce((a, b) => a + b, 0) - mZ2 / 2;
    if (Math.abs(resid) > mZ2 / 2) warns.push('inputs do not satisfy the EWSB condition: sum of C_i - mZ^2/2 = ' + resid.toExponential(3) + ' GeV^2 (should be ~0); Delta_EW from inconsistent inputs is illustrative only');
    const deg = [];
    for (const [a, b] of [['stop1', 'stop2'], ['sbottom1', 'sbottom2'], ['stau1', 'stau2']]) for (const sd of ['u^u', 'd^d']) {
      const c1 = C['Sigma_' + sd + '(' + a + ')'], c2 = C['Sigma_' + sd + '(' + b + ')'], big = Math.max(Math.abs(c1), Math.abs(c2));
      if (big > mZ2 / 2 && Math.abs(c1 + c2) < 0.1 * big) deg.push('Sigma_' + sd + '(' + a + ',' + b + ')'); }
    if (deg.length) warns.push('near-degenerate pair(s) ' + deg.join(', ') + ': the individual terms are large and cancel in the sum; the pair-summed Delta_EW is the meaningful headline here');
    return { mZ_used: Math.sqrt(mZ2), EWSB_residual: resid, degenerate_pairs: deg, warnings: warns.concat([...WARN].sort()), headline: deg.length ? 'pairs_summed' : 'per_term', not_included: NOT_INCLUDED, Delta_EW: 2 * Math.abs(ord[0][1]) / mZ2, largest: ord[0][0], Delta_EW_pairs_summed: 2 * Math.abs(os[0][1]) / mZ2, largest_pairs_summed: os[0][0],
      contributions: ord.map(([k, v]) => [k, v, 2 * Math.abs(v) / mZ2]), summed: os.map(([k, v]) => [k, v, 2 * Math.abs(v) / mZ2]) };
  }
  function readSLHA(text) {
    const B = {}, S = {}, W = [], seen = new Set(); let cur = null;
    for (const raw of text.split(/\r?\n/)) {
      const line = raw.split('#')[0].trim(); if (!line) continue; const w = line.split(/\s+/);
      if (w[0].toUpperCase() === 'BLOCK') { cur = w[1].toUpperCase(); if (seen.has(cur)) { W.push('block ' + cur + ' appears more than once (several scales); only the first was used'); cur = null; continue; } seen.add(cur); B[cur] = {}; const qi = w.findIndex(x => x.toUpperCase().startsWith('Q=')); if (qi > 0) { const q = w[qi].slice(2) || w[qi + 1]; S[cur] = parseFloat(q); } continue; }
      if (w[0].toUpperCase() === 'DECAY') { cur = null; continue; } if (!cur) continue;
      const n = w.map(Number); if (n.some(isNaN)) continue;
      if (n.length >= 3 && /^(YU|YD|YE|AU|AD|AE|TU|TD|TE|STOPMIX|SBOTMIX|STAUMIX)$/.test(cur)) B[cur][n[0] + ',' + n[1]] = n[2]; else if (n.length >= 2) B[cur][n[0]] = n[1];
    }
    return [B, S, W];
  }
  function paramsFromSLHA(text) {
    const [B, S, W] = readSLHA(text);
    for (const need of ['MSOFT', 'HMIX', 'YU']) if (!B[need]) throw new Error('SLHA block ' + need + ' is missing');
    const ms = B.MSOFT, hm = B.HMIX, g = B.GAUGE || {};
    const sq = k => { const m = ms[k]; if (m < 0) W.push('MSOFT ' + k + ' is negative: read as m^2 = -(' + Math.abs(m) + ')^2'); return Math.sign(m) * m * m; };
    const tri = (f, Ab, Tb, Yb) => { const a = (B[Ab] || {})['3,3'], y = (B[Yb] || {})['3,3'] || 0, t = (B[Tb] || {})['3,3'];
      if (a !== undefined) return a; if (t !== undefined && y) return t / y;
      if (f === 't') throw new Error('neither AU nor TU block found: the stop trilinear A_t is unknown'); W.push('no ' + Ab + ' or ' + Tb + ' block: A_' + f + ' set to 0'); return 0; };
    if (!B.GAUGE) W.push("no GAUGE block: g = 0.65, g' = 0.36 assumed");
    if (B.YU['3,3'] === undefined) throw new Error('YU(3,3) missing: the top Yukawa is unknown');
    const tanb = hm[2] || (B.MINPAR || {})[3], v = (hm[3] || 246.2) / Math.SQRT2, be = Math.atan(tanb);
    let Q = S.MSOFT || S.HMIX; if (!Q) Q = Math.sqrt(Math.abs(B.MASS[1000006] * B.MASS[2000006]));
    const gt = (b, k, d = 0) => ((B[b] || {})[k] ?? d);
    return { Q, tanb, vu: v * Math.sin(be), vd: v * Math.cos(be), mu: hm[1], mHu2: ms[22], mHd2: ms[21], mQ3_2: sq(43), mtR_2: sq(46), mbR_2: sq(49), mL3_2: sq(33), meR3_2: sq(36),
      yt: B.YU['3,3'], yb: gt('YD', '3,3'), ytau: gt('YE', '3,3'), At: tri('t', 'AU', 'TU', 'YU'), Ab: tri('b', 'AD', 'TD', 'YD'), Atau: tri('tau', 'AE', 'TE', 'YE'), g: g[2] || 0.65, gp: g[1] || 0.36, warnings: W };
  }
  // RPV decaying wino (D2186b): Gamma ~ 3 alpha eps^2 lambda^2 m^5 /(128 pi^2 m_soft^4), lambda = f_a/M_P
  function faMin(m, ms, tmax, leptonic) {
    const hbar = 6.582119569e-25, mP = 2.435e18, alpha = leptonic ? 1 / 30 : 1 / 128, eps = leptonic ? 1 : 173 / ms;
    return Math.sqrt(hbar * 128 * PI2 * ms ** 4 / (3 * alpha * eps * eps * m ** 5 * tmax)) * mP;
  }
  return { sectors, sigmas, deltaEW, readSLHA, paramsFromSLHA, faMin };
})();
if (typeof module !== 'undefined') module.exports = Z;
