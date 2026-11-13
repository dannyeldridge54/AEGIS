"""TWIST-P check in full two-field supergravity: (1) V along real T equals the Twist's; (2) S stays heavy at the CMB point and today.
K = -3 ln(u - e^{beta/u} g SS + zeta e^{2 beta/u} (SS)^2) + beta/u, u = T + Tbar, g = 1 + u/2mu. AI-assisted."""
import sys, mpmath as mp
sys.path.insert(0, "/home/claude/aegis/theory/inflation")
import s_mass_d127 as SM
mp.mp.dps = 50
def Kp(beta):
    def K(T, Tb, S, Sb):
        u = T + Tb; e = mp.exp(beta / u)
        return -3 * mp.log(u - e * S * Sb * (1 + u / 2) + SM.ZETA * e ** 2 * (S * Sb) ** 2) + beta / u
    return K
W = lambda T, S: mp.sqrt(3) * S * T * SM.cl(T)
K0, _ = SM.setup(True)
for beta, xs in ((mp.mpf("0.001"), "2.3e-4"), (mp.mpf("0.01"), "5.4e-4"), (mp.mpf("0.1"), "1.55e-3")):
    for x in (xs, "0.01", "89"):
        X = mp.mpf(x); K = Kp(beta); s = mp.mpf("1e-7")
        v0, kss = SM.V(K, W, X, mp.mpf(0)); vold, _ = SM.V(K0, W, X, mp.mpf(0))
        vp, _ = SM.V(K, W, X, s); vm, _ = SM.V(K, W, X, -s)
        ms = (vp - 2 * v0 + vm) / (s * s) / (2 * kss) / (v0 / 3)
        print(f"beta {float(beta)}, x {x}: V/V_twist {float(v0/vold):.6f}, m_S^2/H^2 {float(ms):.4g}")
