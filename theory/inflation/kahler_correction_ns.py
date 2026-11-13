"""Development 66 (exploratory): can a small quantum correction to the base Kähler potential move n_s? AI-assisted.
Base: K = -3 ln(T + Tbar) (alpha = 1). Leading corrections in no-scale supergravity are often written as
K = -3 ln(T + Tbar + c (T + Tbar)^p) or as a shift of the coefficient 3 -> 3 alpha. The inflaton's kinetic weight is
K_TTbar; the canonical field phi follows d phi = sqrt(2 K_TTbar) dx (real direction). On the plateau the potential in
terms of x is unchanged (V = m^2 |F|^2 / (4x^2) at leading order), so the correction acts only through the field
metric. We compute n_s, r with N* self-consistent (instant reheating form, as twist_inflation_N.py) for:
  (A) alpha = 1 + delta (coefficient 3 -> 3(1+delta)), the simplest deformation, and
  (B) K = -3 ln(2x + c (2x)^2) (a curvature correction that matters where x is large; plateau at small x in the
      mirrored model -> it matters near the cliff, not at the CMB point).
The E-model limit: V = V0 (1 - exp(-sqrt(2/(3 alpha)) phi))^2 on the plateau."""
import math
from scipy.integrate import quad
from scipy.optimize import brentq

AS = 2.1e-9; G = 106.75; H0c = 67.4 / 299792.458; KSTAR = 0.05


def emodel(alpha):
    c = math.sqrt(2 / (3 * alpha))
    f = lambda p: 1 - math.exp(-c * p)
    eps = lambda p: 0.5 * (2 * c * math.exp(-c * p) / f(p)) ** 2
    eta = lambda p: 2 * c * c * math.exp(-c * p) * (2 * math.exp(-c * p) - 1) / f(p) ** 2
    pend = brentq(lambda p: eps(p) - 1, 1e-3, 20)
    Nof = lambda p: quad(lambda x: 1 / math.sqrt(2 * eps(x)), pend, p)[0]
    N = 55.0
    for _ in range(60):
        p = brentq(lambda q: Nof(q) - N, pend + 1e-6, 80)
        e = eps(p); V0 = AS * 24 * math.pi ** 2 * e / f(p) ** 2
        Nn = 66.89 - math.log(KSTAR / H0c) + 0.25 * math.log((V0 * f(p) ** 2) ** 2 / (1.5 * V0 * f(pend) ** 2)) - math.log(G) / 12
        if abs(Nn - N) < 1e-7:
            break
        N = Nn
    p = brentq(lambda q: Nof(q) - N, pend + 1e-6, 80)
    return N, 1 - 6 * eps(p) + 2 * eta(p), 16 * eps(p)


print("(A) coefficient 3 -> 3 alpha (alpha = 1 is the base theory)")
for a in (0.5, 0.8, 0.9, 1.0, 1.1, 1.5, 2.0, 5.0):
    N, ns, r = emodel(a)
    print(f"  alpha {a:4.2f}: N* {N:.1f}, n_s {ns:.4f}, r {r:.4f}")
for tgt in (0.9700, 0.9730):
    try:
        a = brentq(lambda a: emodel(a)[1] - tgt, 0.05, 50)
        print(f"  n_s = {tgt} needs alpha = {a:.2f}")
    except ValueError:
        print(f"  n_s = {tgt}: not reachable for alpha in [0.05, 50]")
