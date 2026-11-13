"""Development 84 (exploratory): the kination phase after the cliff adds e-folds to N*, raising n_s. AI-assisted.
The locked n_s used N* for instant reheating. After the cliff the inflaton's motion dominates (w = 1) until the
radiation made at reheating (heat share f) takes over. The general N* has the extra term
    dN = 1/4 ln(rho_end / rho(N)) - (N - N_end),   evaluated once radiation dominates (it then stops changing),
which is positive for w > 1/3. Here dN is computed from the actual background (reshaped cliff, m2 = 4/pi, as cliff_v2.py),
then n_s, r are re-evaluated at N* + dN (N* re-solved self-consistently: the term shifts the matching)."""
import math, sys
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
sys.path.insert(0, "theory/inflation"); sys.argv = sys.argv[:1] + sys.argv[1:]
import cliff_v2 as C
c = C.c


def dN_kination(lnV, f, p0):
    V = lambda p: math.exp(lnV(p))
    def rhs(t, z):
        p, dp = z; K = 0.5 * dp * dp; H2 = V(p) / (3 - K); return [dp, -(3 - K) * dp - V(p) * C.DL(p) / H2]
    end = lambda t, z: 0.5 * z[1] ** 2 - 1; end.terminal = True; end.direction = 1
    s = solve_ivp(rhs, [0, 4000], [p0, 0], events=end, rtol=1e-9, atol=1e-12, method="LSODA")
    p, dp = s.y_events[0][0]; H2 = V(p) / (3 - 0.5 * dp * dp); rho_end = 3 * H2
    lnr = math.log(f * 0.5 * H2 * dp * dp); dp *= math.sqrt(1 - f)
    def rhs2(t, z):
        p, dp, lnr = z; rr = math.exp(lnr); K = 0.5 * dp * dp
        Vp = math.exp(lnV(p)) if lnV(p) > -700 else 0.0
        H2 = (Vp + rr) / (3 - K); e = K + (2 / 3) * rr / H2
        return [dp, -(3 - e) * dp - Vp * C.DL(p) / H2, -4.0]
    out = []
    for Nn in (10, 20, 30):
        z = solve_ivp(rhs2, [0, Nn], [p, dp, lnr], rtol=1e-9, atol=1e-12, method="LSODA").y[:, -1]
        pp, dd, lr = z; rr = math.exp(lr); Vp = math.exp(lnV(pp)) if lnV(pp) > -700 else 0.0
        rho = 3 * (Vp + rr) / (3 - 0.5 * dd * dd); out.append(0.25 * math.log(rho_end / rho) - Nn)
    return out


lnV, Fc = C.version("exp", 4 / math.pi); I = C.inflation(lnV)
eps = lambda p: 0.5 * C.DL(p) ** 2
eta = lambda p: (C.DL(p + 1e-5) - C.DL(p - 1e-5)) / 2e-5 + C.DL(p) ** 2
Nof = lambda p: quad(lambda q: -1 / C.DL(q), p, I["pend"], limit=200)[0]
print(f"instant reheating: N* {I['N']:.2f}, n_s {I['ns']:.4f}, r {I['r']:.4f}")
for f in (4e-4, 1.3e-3, 4e-3):
    d = dN_kination(lnV, f, I["pstar"] - 1.0)
    N = I["N"] + d[-1]; p = brentq(lambda q: Nof(q) - N, -25, I["pend"] - 1e-6)
    print(f"heat share {f * 100:.2f}%: kination adds dN = {d[-1]:+.2f} (converged: {d[0]:+.2f}, {d[1]:+.2f}, {d[2]:+.2f}); "
          f"N* {N:.2f}, n_s {1 - 6 * eps(p) + 2 * eta(p):.4f}, r {16 * eps(p):.4f}", flush=True)
