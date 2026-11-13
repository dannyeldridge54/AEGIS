"""Development 92 (exploratory): the twist ANGLE as dark energy, with the size half stabilised. AI-assisted.
Matter couples to the angle y only through its rate of change (Nieh-Yan, shift symmetry), so a rolling angle gives no
fifth force. Take the size heavy today and the angle's leftover potential V = L4 (1 + cos(phi_y / f)) (pNGB quintessence,
Frieman-Hill-Stebbins-Waga), f = the angle's width, 1.56 M_P (canonical; fixed by the period 8, D-step 3).
Thawing from rest at phi_y/f = theta_i (measured from the top), L4 tuned to Omega_DE = 0.69; CPL fit over z < 2."""
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
Om, Or = 0.31, 9.1e-5; ODE = 1 - Om - Or; f = 1.56
def run(th, L4):
    V = lambda p: L4 * (1 + math.cos(p / f)); dV = lambda p: -L4 * math.sin(p / f) / f
    def rhs(N, y):
        p, v = y; a = math.exp(N); H2 = (Om * a ** -3 + Or * a ** -4 + V(p) / 3) / (1 - v * v / 6)
        eps = (1.5 * Om * a ** -3 + 2 * Or * a ** -4 + 0.5 * v * v * H2) / H2
        return [v, -(3 - eps) * v - dV(p) / H2]
    return solve_ivp(rhs, [math.log(1e-4), 0], [th * f, 0], rtol=1e-9, atol=1e-12, dense_output=True), V
def ode(th, L4):
    s, V = run(th, L4); p, v = s.y[:, -1]; H2 = (Om + Or + V(p) / 3) / (1 - v * v / 6)
    return (v * v * H2 / 6 + V(p) / 3) / H2 - ODE
for th in (0.1, 0.3, 0.6, 1.0, 1.5, 2.0, 2.4, 2.8):
    try:
        L4 = brentq(lambda L: ode(th, L), 1e-2, 1e3)
    except ValueError:
        print(f"theta_i {th}: no solution"); continue
    s, V = run(th, L4); a = np.linspace(1 / 3, 1, 300); w = []
    for N in np.log(a):
        p, v = s.sol(N); A = math.exp(N); H2 = (Om * A ** -3 + Or * A ** -4 + V(p) / 3) / (1 - v * v / 6)
        K = v * v * H2 / 6; w.append((K - V(p) / 3) / (K + V(p) / 3))
    w0, wa = np.linalg.lstsq(np.vstack([np.ones(300), 1 - a]).T, np.array(w), rcond=None)[0]
    print(f"start angle {th:.1f} rad from the top: w0 {w0:.3f}, wa {wa:.3f}")
