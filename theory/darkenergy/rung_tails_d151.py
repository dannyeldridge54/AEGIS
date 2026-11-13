"""D151: dark-energy tail slope on each seven-disk rung (tail V ~ 1/x, x = e^{c phi}, c = sqrt(2/(3 alpha))) -> lambda = c.
Thawing exponential quintessence from rest, Omega_m 0.31: w0, wa (CPL fit z < 2). AI-assisted."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
Om, Or = 0.31, 9.1e-5; ODE = 1 - Om - Or
def thaw(lam):
    def go(V0):
        def rhs(N, y):
            p, v = y; a = math.exp(N); V = V0 * math.exp(-lam * p); H2 = (Om * a ** -3 + Or * a ** -4 + V / 3) / (1 - v * v / 6)
            eps = (1.5 * Om * a ** -3 + 2 * Or * a ** -4 + 0.5 * v * v * H2) / H2; return [v, -(3 - eps) * v + lam * V / H2]
        return solve_ivp(rhs, [math.log(1e-4), 0], [0, 0], rtol=1e-10, atol=1e-13, dense_output=True)
    def f(V0):
        s = go(V0); p, v = s.y[:, -1]; V = V0 * math.exp(-lam * p); H2 = (Om + Or + V / 3) / (1 - v * v / 6); return (v * v * H2 / 6 + V / 3) / H2 - ODE
    V0 = brentq(f, 1e-2, 1e3); s = go(V0); a = np.linspace(1 / 3, 1, 300); w = []
    for N in np.log(a):
        p, v = s.sol(N); A = math.exp(N); V = V0 * math.exp(-lam * p); H2 = (Om * A ** -3 + Or * A ** -4 + V / 3) / (1 - v * v / 6)
        K = v * v * H2 / 6; w.append((K - V / 3) / (K + V / 3))
    return np.linalg.lstsq(np.vstack([np.ones(300), 1 - a]).T, np.array(w), rcond=None)[0]
for k in range(1, 8):
    alpha = k / 3; lam = math.sqrt(2 / (3 * alpha)); w0, wa = thaw(lam)
    print(f"rung 3alpha = {k}: lambda {lam:.3f}: w0 {w0:.3f}, wa {wa:.3f}" + ("   <- the Twist" if k == 3 else ""))
