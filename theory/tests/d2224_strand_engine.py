"""D2224 strand engine: d2221 engine (MS->DR, top decoupling) with non-universal M12 thresholds delta12 = a1^-1 - a2^-1, delta32 = a3^-1 - a2^-1 at M12.
D2221 (A): top decoupled below m_t (one-loop betas). From D2220: (from D1944 engine, PREREG_D2220_AS_DRBAR): MS->DR conversion at m_scalar added.
D1944: theory error on alpha_s. weave_rg2 neglects the two-loop top-Yukawa term and labels itself '+-0.004'.
Here: the same two-loop gauge running (same betas, thresholds, spectrum) PLUS the top-Yukawa two-loop term and one-loop y_t running.
d(alpha_i^-1)/dt += d_i y_t^2 / (32 pi^3); SM d = (17/10, 3/2, 2), MSSM d = (26/5, 6, 4) with y_t -> y_t / sin(beta) above m_scalar.
Three readings of the theory error (the three vectors): (1) the Yukawa term computed here; (2) the spectrum scale (gluino +-20 %, Jacobian D1937);
(3) the engine's own label (+-0.004, now replaced by (1) if (1) is smaller)."""
import json, math, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
MZ = 91.1876; aem, s2 = 127.95, 0.23122
mw, mg, ms = 686.5, 4926.4, 4.7e5; tanb = 2.0; sb = tanb / math.sqrt(1 + tanb ** 2)
SM1, MS1 = np.array([41 / 10, -19 / 6, -7]), np.array([33 / 5, 1, -3])
SM2 = np.array([[199 / 50, 27 / 10, 44 / 5], [9 / 10, 35 / 6, 12], [11 / 10, 9 / 2, -26]])
MS2 = np.array([[199 / 25, 27 / 5, 88 / 5], [9 / 5, 25, 24], [11 / 5, 9, 14]])
dSM, dMS = np.array([17 / 10, 3 / 2, 2]), np.array([26 / 5, 6, 4])
def run(a3, mu1, yuk, conv=True):
    def rhs(t, x):
        mu = math.exp(t); al = 1 / x[:3]; y = x[3]
        if mu >= ms: b1, b2, d, yy = MS1, MS2, dMS, y / sb
        else:
            b1, b2 = SM1.copy(), SM2.copy()
            if mu < 172.6: b1 = b1 - np.array([17 / 30, 1 / 2, 2 / 3])   # D2221: 5-flavour below m_t
            if mu >= mw: b1 = b1 + [0, 4 / 3, 0]; b2 = b2.copy(); b2[1, 1] += 64 / 3
            if mu >= mg: b1 = b1 + [0, 0, 2]; b2 = b2.copy(); b2[2, 2] += 48
            d, yy = dSM, y
        g = [4 * math.pi * a for a in al]          # g_i^2
        dx = -b1 / (2 * math.pi) - b2 @ al / (8 * math.pi ** 2) + (d * yy ** 2 / (32 * math.pi ** 3) if yuk else 0)
        # one-loop SM y_t running (GUT-normalised g1^2 = 5/3 g'^2 already in alpha_1)
        dy = y / (16 * math.pi ** 2) * (4.5 * y ** 2 - 8 * g[2] - 2.25 * g[1] - 17 / 20 * g[0])
        return list(dx) + [dy]
    yt0 = 0.94                                     # MSbar-like top Yukawa at M_Z (estimate, y_t(m_t) ~ 0.94)
    x = [0.6 * (1 - s2) * aem, s2 * aem, 1 / a3, yt0]
    pts = [math.log(MZ)] + [math.log(m) for m in sorted((172.6, mw, mg, ms)) if m < mu1] + [math.log(mu1)]
    for t0, t1 in zip(pts, pts[1:]):
        x = solve_ivp(rhs, (t0 + 1e-12, t1), x, rtol=1e-10, atol=1e-12).y[:, -1]
        if conv and abs(t1 - math.log(ms)) < 1e-9: x = x.copy(); x[:3] = x[:3] - np.array([0, 2, 3]) / (12 * math.pi)   # MS-bar -> DR-bar (Martin-Vaughn)
    return x

def m12(a3, d12):
    lo, hi = 1e10, 1e20   # D2224 DEV-2
    for _ in range(70):
        mid = math.sqrt(lo * hi); x = run(a3, mid, True, True); lo, hi = (mid, hi) if x[0] - x[1] > d12 else (lo, mid)
    return mid, run(a3, mid, True, True)
def alpha_s(d12=0.0, d32=0.0):
    f = lambda a3: (lambda r: r[1][2] - r[1][1] - d32)(m12(a3, d12))
    a = brentq(f, 0.06, 0.40, xtol=1e-7); return a, m12(a, d12)[0]
