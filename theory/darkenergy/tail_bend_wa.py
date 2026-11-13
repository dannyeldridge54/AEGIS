"""Development 65 (exploratory): does the bend of the real tail deepen w_a with beta = 0? AI-assisted.
Real tail (D43): V(phi) = V0 / (1 + exp(c (phi - phi_mu))), c = sqrt(2/3): flat for phi << phi_mu, exponential
slope c for phi >> phi_mu. The field starts frozen at phi_i (deep in matter era); d = phi_i - phi_mu sets where on the
bend it sits. Flat universe: radiation + matter + field, V0 tuned so Omega_DE today = 0.69 (h = 0.68).
Background only (no perturbations); check: the exponential limit must match Scherrer-Sen (w0 ~ -0.90 for c = 0.816, Omega 0.69); w(z) fitted with CPL w0 + wa (1 - a) over z < 2, as effective_w.py."""
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
c = math.sqrt(2 / 3); Om, Or = 0.31, 9.1e-5; ODE = 1 - Om - Or


def run(d, V0):
    V = lambda p: V0 / (1 + math.exp(c * (p - 0.0)))
    dV = lambda p: -V0 * c * math.exp(c * p) / (1 + math.exp(c * p)) ** 2
    def rhs(N, y):                                # N = ln a; y = (phi, dphi/dN); units H0 = 1, 3 H0^2 M_P^2 = 1 -> rho in 3H0^2
        p, v = y; a = math.exp(N)
        rm, rr = Om * a ** -3, Or * a ** -4
        H2 = (rm + rr + V(p) / 3) / (1 - v * v / 6)
        eps = (1.5 * rm + 2 * rr + 0.5 * v * v * H2) / H2
        return [v, -(3 - eps) * v - dV(p) / H2]
    s = solve_ivp(rhs, [math.log(1e-4), 0], [d, 0.0], rtol=1e-9, atol=1e-12, dense_output=True)
    return s


def omega_de(d, V0):
    s = run(d, V0); p, v = s.y[:, -1]
    rm, rr = Om, Or; H2 = (rm + rr + V0 / (1 + math.exp(c * p)) / 3) / (1 - v * v / 6)
    return (v * v * H2 / 6 + V0 / (1 + math.exp(c * p)) / 3) / H2, s


for d in (-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0, 8.0):
    V0 = brentq(lambda V0: omega_de(d, V0)[0] - ODE, 1e-3, 1e4)
    _, s = omega_de(d, V0)
    a = np.linspace(1 / 3, 1, 300); N = np.log(a); w = []
    for n in N:
        p, v = s.sol(n); A = math.exp(n); Vp = V0 / (1 + math.exp(c * p))
        H2 = (Om * A ** -3 + Or * A ** -4 + Vp / 3) / (1 - v * v / 6); K = v * v * H2 / 6
        w.append((K - Vp / 3) / (K + Vp / 3))
    w = np.array(w); w0, wa = np.linalg.lstsq(np.vstack([np.ones(300), 1 - a]).T, w, rcond=None)[0]
    slope_now = c * math.exp(c * s.y[0, -1]) / (1 + math.exp(c * s.y[0, -1]))
    print(f"start {d:+.1f} from the bend: w0 {w0:.3f}, wa {wa:.3f}, w today {w[-1]:.3f}, slope seen today {slope_now / c:.2f} x sqrt(2/3)", flush=True)
