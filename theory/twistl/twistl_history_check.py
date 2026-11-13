"""Tier 2 (1): TWIST-L stability along the whole history (S mass and angle mass), b = 3 and 10, full two-field SUGRA. AI-assisted."""
import sys, mpmath as mp
src = open("/home/claude/aegis/theory/kahler_cliff/kahler_cliff_d159.py").read().split("Ko, Wo = SM.setup(True)")[0]
sys.argv = sys.argv[:1]; ns = {}; exec(src, ns); V, E, ZETA = ns["V"], ns["E"], ns["ZETA"]; mp.mp.dps = 200
Wn = lambda T, S: mp.sqrt(3) * S * T
for b in (3.0, 10.0):
    L = lambda u: 1 + b / (1 + mp.log(1 + 2 / u))
    def K(T, Tb, S, Sb):
        u = T + Tb; e = E(u) * L(u); return -3 * mp.log(u - (1 + u / 2) * e * S * Sb + ZETA * e ** 2 * (S * Sb) ** 2)
    for x in ("1e-4", "0.01", "0.3", "1", "3", "20", "89"):
        X = mp.mpf(x); e = E(2 * X) * L(2 * X); hT = X * mp.mpf("1e-15"); hS = mp.mpf("1e-15") / mp.sqrt(e); s = mp.mpf("1e-9") / mp.sqrt(e)
        v, kss = V(K, Wn, X, mp.mpf(0), hT, hS); vp, _ = V(K, Wn, X, s, hT, hS); vm, _ = V(K, Wn, X, -s, hT, hS)
        ms = (vp - 2 * v + vm) / (s * s) / (2 * kss) / (v / 3)
        hy = X * mp.mpf("1e-6")
        my = (V(K, Wn, mp.mpc(X, hy), mp.mpf(0), hT, hS)[0] - 2 * v + V(K, Wn, mp.mpc(X, -hy), mp.mpf(0), hT, hS)[0]) / (hy * hy) / (2 * 3 / (4 * X * X)) / (v / 3)
        print(f"b {b}, x {x}: m_S^2/H^2 {float(ms):.4g}, m_y^2/H^2 {float(my):+.3f}", flush=True)
