// Chronos core (same algorithm as chronos.py, analytic Bateman). Danny Lee Eldridge / the Weave, D2189. Free to use.
const CH = (() => {
  const MIN = 60, H = 3600, D = 86400, Y = 365.25 * 86400;
  const T12 = { 'F-18': 109.77 * MIN, 'C-11': 20.364 * MIN, 'N-13': 9.965 * MIN, 'O-15': 122.24, 'Ga-68': 67.71 * MIN, 'Ge-68': 270.95 * D,
    'Tc-99m': 6.0067 * H, 'Mo-99': 65.976 * H, 'Rb-82': 1.2575 * MIN, 'Sr-82': 25.35 * D, 'Cu-64': 12.701 * H, 'Zr-89': 78.41 * H,
    'Lu-177': 6.647 * D, 'Ac-225': 9.920 * D, 'In-111': 2.8047 * D, 'I-123': 13.2234 * H, 'I-131': 8.0252 * D, 'Y-90': 64.05 * H,
    'Sr-90': 28.79 * Y, 'Cs-137': 30.08 * Y, 'Cs-134': 2.0652 * Y, 'Ba-137m': 2.552 * MIN, 'Co-60': 5.2714 * Y, 'Pu-241': 14.29 * Y,
    'Am-241': 432.6 * Y, 'Ni-56': 6.075 * D, 'Co-56': 77.236 * D };
  const LAM = {}; for (const k in T12) LAM[k] = Math.LN2 / T12[k];
  const CHAINS = { 'Mo-99 -> Tc-99m (generator)': [['Mo-99', 'Tc-99m'], [0.876]], 'Ge-68 -> Ga-68 (generator)': [['Ge-68', 'Ga-68'], [1]],
    'Sr-82 -> Rb-82 (generator)': [['Sr-82', 'Rb-82'], [1]], 'Sr-90 -> Y-90': [['Sr-90', 'Y-90'], [1]], 'Cs-137 -> Ba-137m': [['Cs-137', 'Ba-137m'], [0.946]],
    'Pu-241 -> Am-241 (spent fuel)': [['Pu-241', 'Am-241'], [0.99998]], 'Ni-56 -> Co-56 (supernova)': [['Ni-56', 'Co-56'], [1]] };
  function bateman(nucs, br, N0, t) {
    const n = nucs.length, lam = nucs.map(k => LAM[k]), out = new Array(n).fill(0);
    for (let s = 0; s < n; s++) { if (!N0[s]) continue;
      for (let j = s; j < n; j++) { let pre = N0[s]; for (let m = s; m < j; m++) pre *= br[m] * lam[m];
        let tot = 0; for (let i = s; i <= j; i++) { let den = 1; for (let p = s; p <= j; p++) if (p !== i) den *= (lam[p] - lam[i]); tot += Math.exp(-lam[i] * t) / den; }
        out[j] += pre * tot; } }
    return out;
  }
  const needed = (nuc, A, t) => A * Math.exp(LAM[nuc] * t), timeTo = (nuc, A0, A) => Math.log(A0 / A) / LAM[nuc];
  function genPeak(c) { const [n] = CHAINS[c], lp = LAM[n[0]], ld = LAM[n[1]]; return Math.log(ld / lp) / (ld - lp); }
  function genRatio(c) { const [n, br] = CHAINS[c], lp = LAM[n[0]], ld = LAM[n[1]]; return br[0] * ld / (ld - lp); }
  const ratioAt = (ty, r0 = 1, a = 'Cs-134', b = 'Cs-137') => r0 * Math.exp(-(LAM[a] - LAM[b]) * ty * Y);
  const releaseAge = (r, r0 = 1, a = 'Cs-134', b = 'Cs-137') => Math.log(r0 / r) / (LAM[a] - LAM[b]) / Y;
  const MEV = 1.602176634e-6, NA = 6.02214076e23, MSUN = 1.98892e33, QNI = 1.75, QCO = 3.73;
  function snL(t, M = 0.6, t0 = null) { const [n, br] = CHAINS['Ni-56 -> Co-56 (supernova)'], N = bateman(n, br, [M * MSUN * NA / 56, 0], t);
    const f = t0 == null ? 1 : 1 - Math.exp(-((t0 * D) ** 2) / (t * t)); return (QNI * MEV * LAM['Ni-56'] * N[0] + QCO * MEV * LAM['Co-56'] * N[1]) * f; }
  const knL = (t, M = 0.05, f = 0.5) => M * MSUN * 1e10 * Math.pow(t / D, -1.3) * f;
  return { MIN, H, D, Y, T12, LAM, CHAINS, bateman, needed, timeTo, genPeak, genRatio, ratioAt, releaseAge, snL, knL };
})();
if (typeof module !== 'undefined') module.exports = CH;
