"""Development 78b: w0, wa with the full tail shape (not the exponential approximation). AI-assisted.
The field starts at rest at x_f (from tail_freeze.run for heat share f) deep in the matter era and thaws on
V = V0 g(phi)/g(phi_f), g = exp(-2n x/(x + m2)) / (1 + x/mu), x = e^{c phi}; V0 tuned to Omega_DE = 0.69. CPL fit as before."""
import math, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, "theory/darkenergy")
from tail_freeze import run
c = math.sqrt(2 / 3); n, m2, mu = 125.0, 1.0, 1.0
Om, Or = 0.31, 9.1e-5; ODE = 1 - Om - Or
lng = lambda p: -2 * n * math.exp(c * p) / (math.exp(c * p) + m2) - math.log(1 + math.exp(c * p) / mu)


def dlng(p):
    x = math.exp(c * p); return -c * x * (2 * n * m2 / (x + m2) ** 2 + 1 / (x + mu))


def solve(pf):
    Vf = lambda V0, p: V0 * math.exp(lng(p) - lng(pf))
    def go(V0):
        def rhs(N, y):
            p, v = y; a = math.exp(N); V = Vf(V0, p)
            H2 = (Om * a ** -3 + Or * a ** -4 + V / 3) / (1 - v * v / 6)
            eps = (1.5 * Om * a ** -3 + 2 * Or * a ** -4 + 0.5 * v * v * H2) / H2
            return [v, -(3 - eps) * v - V * dlng(p) / H2]
        return solve_ivp(rhs, [math.log(1e-4), 0], [pf, 0], rtol=1e-9, atol=1e-12, dense_output=True)
    def ode(V0):
        s = go(V0); p, v = s.y[:, -1]; V = Vf(V0, p); H2 = (Om + Or + V / 3) / (1 - v * v / 6)
        return (v * v * H2 / 6 + V / 3) / H2 - ODE
    V0 = brentq(ode, 1e-2, 1e4); s = go(V0); a = np.linspace(1 / 3, 1, 300); w = []
    for N in np.log(a):
        p, v = s.sol(N); A = math.exp(N); V = Vf(V0, p)
        H2 = (Om * A ** -3 + Or * A ** -4 + V / 3) / (1 - v * v / 6); K = v * v * H2 / 6; w.append((K - V / 3) / (K + V / 3))
    w0, wa = np.linalg.lstsq(np.vstack([np.ones(300), 1 - a]).T, np.array(w), rcond=None)[0]
    return w0, wa, w[-1], math.exp(c * s.y[0, -1])


if __name__ == "__main__":
  for f in (1e-4, 4e-4, 8e-4, 1.3e-3, 2e-3, 4e-3):
      xf = run(mu, n=n, m2=m2, f=f)[0]
      try:
          w0, wa, wt, xt = solve(math.log(xf) / c)
          print(f"heat share {f * 100:.3f}%: x_f {xf:.0f} -> today x {xt:.0f}; w0 {w0:.3f}, wa {wa:.3f} (w today {wt:.3f})", flush=True)
      except ValueError:
          print(f"heat share {f * 100:.3f}%: x_f {xf:.0f}; no solution with Omega_DE 0.69 (too steep)", flush=True)
