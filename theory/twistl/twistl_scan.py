"""D162 (exploratory, built after seeing the n_s data — any version of it must be locked and tested on future data only).
Idea: stay on rung 3 (K = -3 ln(T+Tbar) for T's own kinetic term — the geometry is kept, unlike TWIST-P) and let S's Kahler metric
carry a LOGARITHMIC factor, as a loop / running-coupling correction would: K_SS -> K_SS * L(x),
  L(x) = 1 + b / (1 + ln(1 + 1/x))      (-> 1 + b/ln(1/x) on the plateau, -> 1 + b on the tail: tail shape unchanged)
V = V_twist(x) / L(x). Because ln(1/x) = -c phi, the plateau now approaches flat as 1/phi (a polynomial attractor, k = 1) while T's
geometry is untouched. Polynomial k=1 attractor: n_s ~ 1 - 4/(3N). Computes n_s, r for several b. AI-assisted."""
import math, sys, numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
sys.path.insert(0, "/home/claude/aegis/theory/inflation"); import cliff_v2 as C
lnVp, _ = C.version("exp", 4 / math.pi); c = C.c
def obs(b, dN_extra=1.2):
    L = lambda x: 1 + b / (1 + math.log(1 + 1 / x))
    lnV = lambda x: lnVp(math.log(x) / c) - math.log(L(x))
    dl = lambda x, h=1e-6: (lnV(x * (1 + h)) - lnV(x * (1 - h))) / (2 * h)      # d lnV / d ln x
    eps = lambda x: 0.5 * (c * dl(x)) ** 2                                      # x = e^{c phi}: dlnV/dphi = c dlnV/dlnx
    lx = np.linspace(math.log(1e-12), math.log(10), 30000); e = [eps(math.exp(v)) for v in lx]
    i = next(k for k in range(len(lx)) if e[k] >= 1); xe = math.exp(brentq(lambda v: eps(math.exp(v)) - 1, lx[i - 1], lx[i]))
    Nof = lambda x: quad(lambda v: -1 / (c * c) / min(dl(math.exp(v)), -1e-300), math.log(x), math.log(xe), limit=400)[0]
    def eta(x, h=1e-4):
        f = lambda z: c * dl(z)
        return c * (f(x * (1 + h)) - f(x * (1 - h))) / (2 * h) + f(x) ** 2
    N = 56.0
    for _ in range(60):
        x = math.exp(brentq(lambda v: Nof(math.exp(v)) - N, math.log(1e-10), math.log(xe) - 1e-9))
        V0 = C.AS * 24 * math.pi ** 2 * eps(x) / math.exp(lnV(x))
        Nn = 66.89 - math.log(C.KSTAR / C.H0c) + 0.25 * math.log((V0 * math.exp(lnV(x))) ** 2 / (1.5 * V0 * math.exp(lnV(xe)))) - math.log(C.G) / 12 + dN_extra
        if abs(Nn - N) < 1e-7: break
        N = Nn
    x = math.exp(brentq(lambda v: Nof(math.exp(v)) - N, math.log(1e-10), math.log(xe) - 1e-9))
    return N, 1 - 6 * eps(x) + 2 * eta(x), 16 * eps(x), x
for b in [float(v) for v in sys.argv[1:]] or (0.0, 0.03, 0.1, 0.3, 1.0, 3.0):
    N, ns, r, x = obs(b); print(f"b {b}: N* {N:.1f}, n_s {ns:.4f}, r {r:.2e}, x* {x:.1e}", flush=True)
