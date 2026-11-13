"""Development 98: the remaining inflation observables at the Twist's own N* (reshaped cliff, m2 = 4/pi, kination N*).
Running alpha_s = dn_s/dlnk, tensor tilt n_t = -r/8 (single-field consistency), squeezed non-Gaussianity
f_NL^local = (5/12)(1 - n_s) (Maldacena), and the inflation energy scale. AI-assisted."""
import math, sys
from scipy.integrate import quad
from scipy.optimize import brentq
sys.path.insert(0, "theory/inflation"); sys.argv = sys.argv[:1]
import cliff_v2 as C
lnV, _ = C.version("exp", 4 / math.pi); I = C.inflation(lnV)
eps = lambda p: 0.5 * C.DL(p) ** 2
eta = lambda p: (C.DL(p + 1e-5) - C.DL(p - 1e-5)) / 2e-5 + C.DL(p) ** 2
Nof = lambda p: quad(lambda q: -1 / C.DL(q), p, I["pend"], limit=200)[0]
ns = lambda p: 1 - 6 * eps(p) + 2 * eta(p)
for N in (I["N"], I["N"] + 1.94):
    p = brentq(lambda q: Nof(q) - N, -25, I["pend"] - 1e-6)
    h = 0.02; pa, pb = brentq(lambda q: Nof(q) - (N + h), -25, p), brentq(lambda q: Nof(q) - (N - h), p, I["pend"] - 1e-6)
    a_s = -(ns(pa) - ns(pb)) / (2 * h)                        # dln k = -dN
    r = 16 * eps(p); V = 2.1e-9 * 24 * math.pi ** 2 * eps(p)   # V* in M_P^4
    print(f"N* {N:.1f}: n_s {ns(p):.4f}, alpha_s {a_s:.2e}, r {r:.4f}, n_t {-r / 8:.2e}, f_NL {5 / 12 * (1 - ns(p)):.3f}, "
          f"V*^(1/4) {V ** 0.25 * 2.435e18:.2e} GeV, H* {math.sqrt(V / 3) * 2.435e18:.2e} GeV")
