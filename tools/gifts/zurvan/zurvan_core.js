// Zurvan core (same algorithm as zurvan.py). Danny Lee Eldridge / the Weave, D2187. Free to use.
const Z = (() => {
  const PI2 = Math.PI * Math.PI;
  const eig2 = (a, b, c) => { const s = 0.5 * (a + b), d = Math.sqrt(0.25 * (a - b) ** 2 + c * c); return [s - d, s + d]; };
  const cw = (m2, Q2, n) => { if (m2 <= 0) m2 = Math.abs(m2) + 1e-12; return n / (64 * PI2) * m2 * m2 * (Math.log(m2 / Q2) - 1.5); };
  function sectors(p, vu, vd) {
    const g = p.g, gp = p.gp, gz2 = (g * g + gp * gp) / 2, sw2 = gp * gp / (g * g + gp * gp), D = gz2 * (vd * vd - vu * vu), mu = p.mu, o = {};
    let m = p.yt * vu, LL = p.mQ3 ** 2 + m * m + (0.5 - 2 / 3 * sw2) * D, RR = p.mtR ** 2 + m * m + (2 / 3 * sw2) * D, LR = p.yt * (p.At * vu - mu * vd), e = eig2(LL, RR, LR);
    o.stop1 = [[e[0], 6]]; o.stop2 = [[e[1], 6]]; o.top = [[m * m, -12]];
    m = p.yb * vd; LL = p.mQ3 ** 2 + m * m + (-0.5 + sw2 / 3) * D; RR = p.mbR ** 2 + m * m + (-sw2 / 3) * D; LR = p.yb * (p.Ab * vd - mu * vu); e = eig2(LL, RR, LR);
    o.sbottom1 = [[e[0], 6]]; o.sbottom2 = [[e[1], 6]]; o.bottom = [[m * m, -12]];
    m = p.ytau * vd; LL = p.mL3 ** 2 + m * m + (-0.5 + sw2) * D; RR = p.meR3 ** 2 + m * m + (-sw2) * D; LR = p.ytau * (p.Atau * vd - mu * vu); e = eig2(LL, RR, LR);
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
    const t2 = p.tanb ** 2, den = t2 - 1, S = sigmas(p), C = { mu: -(p.mu ** 2), H_u: -p.mHu2 * t2 / den, H_d: p.mHd2 / den };
    for (const [k, [su, sd]] of Object.entries(S)) { C['Sigma_u^u(' + k + ')'] = -su * t2 / den; C['Sigma_d^d(' + k + ')'] = sd / den; }
    const mZ2 = (p.mZ || 91.1876) ** 2, ord = Object.entries(C).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));
    const Cs = {}; for (const [k, v] of Object.entries(C)) { const kk = k.replace(/stop[12]/, 'stops').replace(/sbottom[12]/, 'sbottoms').replace(/stau[12]/, 'staus'); Cs[kk] = (Cs[kk] || 0) + v; }
    const os = Object.entries(Cs).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));
    return { Delta_EW: 2 * Math.abs(ord[0][1]) / mZ2, largest: ord[0][0], Delta_EW_pairs_summed: 2 * Math.abs(os[0][1]) / mZ2, largest_pairs_summed: os[0][0],
      contributions: ord.map(([k, v]) => [k, v, 2 * Math.abs(v) / mZ2]), summed: os.map(([k, v]) => [k, v, 2 * Math.abs(v) / mZ2]) };
  }
  function readSLHA(text) {
    const B = {}, S = {}; let cur = null;
    for (const raw of text.split(/\r?\n/)) {
      const line = raw.split('#')[0].trim(); if (!line) continue; const w = line.split(/\s+/);
      if (w[0].toUpperCase() === 'BLOCK') { cur = w[1].toUpperCase(); B[cur] = B[cur] || {}; const qi = w.findIndex(x => x.toUpperCase().startsWith('Q=')); if (qi > 0) { const q = w[qi].slice(2) || w[qi + 1]; S[cur] = parseFloat(q); } continue; }
      if (w[0].toUpperCase() === 'DECAY') { cur = null; continue; } if (!cur) continue;
      const n = w.map(Number); if (n.some(isNaN)) continue;
      if (n.length >= 3 && /^(YU|YD|YE|AU|AD|AE|STOPMIX|SBOTMIX|STAUMIX)$/.test(cur)) B[cur][n[0] + ',' + n[1]] = n[2]; else if (n.length >= 2) B[cur][n[0]] = n[1];
    }
    return [B, S];
  }
  function paramsFromSLHA(text) {
    const [B, S] = readSLHA(text), ms = B.MSOFT, hm = B.HMIX, g = B.GAUGE || {};
    const tanb = hm[2] || (B.MINPAR || {})[3], v = (hm[3] || 246.2) / Math.SQRT2, be = Math.atan(tanb);
    let Q = S.MSOFT || S.HMIX; if (!Q) Q = Math.sqrt(Math.abs(B.MASS[1000006] * B.MASS[2000006]));
    const gt = (b, k, d = 0) => ((B[b] || {})[k] ?? d);
    return { Q, tanb, vu: v * Math.sin(be), vd: v * Math.cos(be), mu: hm[1], mHu2: ms[22], mHd2: ms[21], mQ3: ms[43], mtR: ms[46], mbR: ms[49], mL3: ms[33], meR3: ms[36],
      yt: gt('YU', '3,3'), yb: gt('YD', '3,3'), ytau: gt('YE', '3,3'), At: gt('AU', '3,3'), Ab: gt('AD', '3,3'), Atau: gt('AE', '3,3'), g: g[2] || 0.65, gp: g[1] || 0.36 };
  }
  // RPV decaying wino (D2186b): Gamma ~ 3 alpha eps^2 lambda^2 m^5 /(128 pi^2 m_soft^4), lambda = f_a/M_P
  function faMin(m, ms, tmax, leptonic) {
    const hbar = 6.582119569e-25, mP = 2.435e18, alpha = leptonic ? 1 / 30 : 1 / 128, eps = leptonic ? 1 : 173 / ms;
    return Math.sqrt(hbar * 128 * PI2 * ms ** 4 / (3 * alpha * eps * eps * m ** 5 * tmax)) * mP;
  }
  return { sectors, sigmas, deltaEW, readSLHA, paramsFromSLHA, faMin };
})();
if (typeof module !== 'undefined') module.exports = Z;
