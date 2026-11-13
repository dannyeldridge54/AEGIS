"""TWIST-P (new model, 13 Nov 2026): same superpotential and same potential along real T as the Twist (v5), new Kahler
potential with an extra pole-order-3 term that only matters deep on the plateau:
  K = -3 ln(T + Tbar - e^{beta/(T+Tbar)} g SS + zeta (SS)^2) + beta/(T + Tbar),   g = 1 + (T+Tbar)/2mu
The e^{beta/u} on S's metric cancels the e^{beta/u} from e^K, so V(x) along real T is unchanged; only the kinetic metric changes:
  K_TTbar = 3/(4x^2) + beta/(4x^3)  ->  dphi/dx = sqrt(3/(2x^2) + beta/(2x^3)).
x >> beta: as before (exponential approach, tail slope sqrt(2/3) kept). x << beta: phi ~ 1/sqrt(x), V ~ 1 - a x ~ 1 - c/phi^2: a
polynomial (k = 2) attractor, n_s ~ 1 - 3/(2N). Computes n_s, r, N* for several beta. AI-assisted."""
import math, sys
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
sys.path.insert(0, "/home/claude/aegis/theory/inflation")
import cliff_v2 as C
lnVp, _ = C.version("exp", 4 / math.pi); c = C.c
lnV = lambda x: lnVp(math.log(x) / c)
dlnV_dx = lambda x: C.DL(math.log(x) / c) / (c * x)          # d lnV/dphi_old * dphi_old/dx
AS, G, H0c, KSTAR = C.AS, C.G, C.H0c, C.KSTAR
def obs(beta, dN_extra=0.0):
    J = lambda x: math.sqrt(3 / (2 * x * x) + beta / (2 * x ** 3))     # dphi/dx
    eps = lambda x: 0.5 * (dlnV_dx(x) / J(x)) ** 2
    xs = np.logspace(-9, 1, 20000); e = [eps(x) for x in xs]
    i = next(k for k in range(len(xs)) if e[k] >= 1); xe = brentq(lambda x: eps(x) - 1, xs[i - 1], xs[i])
    Nof = lambda x: quad(lambda L: -J(math.exp(L)) ** 2 * math.exp(L) / dlnV_dx(math.exp(L)), math.log(x), math.log(xe), limit=400)[0]
    def eta(x, h=1e-4):
        f = lambda z: dlnV_dx(z) / J(z)                               # dlnV/dphi
        dfdphi = (f(x * (1 + h)) - f(x * (1 - h))) / (2 * x * h) / J(x)
        return dfdphi + f(x) ** 2
    N = 55.0
    for _ in range(60):
        x = brentq(lambda q: Nof(q) - N, 1e-9, xe * (1 - 1e-9))
        V0 = AS * 24 * math.pi ** 2 * eps(x) / math.exp(lnV(x))
        Nn = 66.89 - math.log(KSTAR / H0c) + 0.25 * math.log((V0 * math.exp(lnV(x))) ** 2 / (1.5 * V0 * math.exp(lnV(xe)))) - math.log(G) / 12 + dN_extra
        if abs(Nn - N) < 1e-7: break
        N = Nn
    x = brentq(lambda q: Nof(q) - N, 1e-9, xe * (1 - 1e-9))
    return dict(N=N, ns=1 - 6 * eps(x) + 2 * eta(x), r=16 * eps(x), xstar=x, xend=xe)
if __name__ == "__main__":
    for beta in (0.0, 1e-4, 1e-3, 1e-2, 0.1, 1.0):
        o = obs(beta); k = obs(beta, 1.2)
        print(f"beta {beta:<7}: instant N* {o['N']:.1f} n_s {o['ns']:.4f} r {o['r']:.2e} (x* {o['xstar']:.2e}) | kination +1.2: "
              f"n_s {k['ns']:.4f} r {k['r']:.2e}", flush=True)
