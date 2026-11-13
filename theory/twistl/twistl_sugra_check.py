"""TWIST-L check in full two-field supergravity at the CMB point: S mass and angle mass with the log factor in S's metric.
K = -3 ln(u - g E L SS + zeta (E L)^2 (SS)^2), L(u) = 1 + b/(1 + ln(1 + 2/u)) (u = 2x), W = sqrt3 m S T. AI-assisted."""
import sys, mpmath as mp
sys.path.insert(0, "/home/claude/aegis/theory/kahler_cliff"); sys.argv = sys.argv[:1] + ["1e9"]
import importlib.util
spec = importlib.util.spec_from_file_location("kc", "/home/claude/aegis/theory/kahler_cliff/kahler_cliff_d159.py")
src = open("/home/claude/aegis/theory/kahler_cliff/kahler_cliff_d159.py").read().split("Ko, Wo = SM.setup(True)")[0]
ns = {}; exec(src, ns); V, E, ZETA = ns["V"], ns["E"], ns["ZETA"]; mp.mp.dps = 80
Wn = lambda T, S: mp.sqrt(3) * S * T
for b, x in ((1.0, "1.1e-4"), (3.0, "7.9e-5"), (5.0, "6.2e-5"), (10.0, "4.2e-5")):
    L = lambda u: 1 + b / (1 + mp.log(1 + 2 / u))
    def K(T, Tb, S, Sb):
        u = T + Tb; e = E(u) * L(u); return -3 * mp.log(u - (1 + u / 2) * e * S * Sb + ZETA * e ** 2 * (S * Sb) ** 2)
    X = mp.mpf(x); hT = X * mp.mpf("1e-15"); hS = mp.mpf("1e-15"); s = mp.mpf("1e-9")
    v, kss = V(K, Wn, X, mp.mpf(0), hT, hS); vp, _ = V(K, Wn, X, s, hT, hS); vm, _ = V(K, Wn, X, -s, hT, hS)
    ms = (vp - 2 * v + vm) / (s * s) / (2 * kss) / (v / 3)
    hy = X * mp.mpf("1e-6"); my = (V(K, Wn, mp.mpc(X, hy), mp.mpf(0), hT, hS)[0] - 2 * v + V(K, Wn, mp.mpc(X, -hy), mp.mpf(0), hT, hS)[0]) / (hy * hy) / (2 * 3 / (4 * X * X)) / (v / 3)
    print(f"b {b}, CMB point x {x}: m_S^2/H^2 {float(ms):.3g}, m_y^2/H^2 {float(my):+.3f}")
