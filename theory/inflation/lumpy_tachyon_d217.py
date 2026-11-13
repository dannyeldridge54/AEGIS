"""D217: the Twist-specific risk for inhomogeneous starts — the helper S is tachyonic deep on the plateau (m_S^2/H^2 = -2 + 8 zeta x,
D136/D114), so only patches starting above x_b = 1/(4 zeta) can inflate. How much plateau (in M_P and e-folds) is stable, and how
does it depend on zeta? AI-assisted. Twist potential along real T (D195): ln V = -ln(1 + u/2) - 2n(1 - e^{-pi u/8}), u = 2x = e^{sqrt(2/3) phi}."""
import math
from scipy.integrate import quad
n = 125; k = math.sqrt(2 / 3)
dlnV = lambda u: -(1 / (2 + u)) * u * k - 2 * n * (math.pi / 8) * u * math.exp(-math.pi * u / 8) * k   # d lnV/d phi (u' = k u)
u_end = 0.01768
def efolds(u_start):                       # N = int dphi / |d lnV/dphi| from u_start up to u_end (phi = ln u / k)
    return quad(lambda lu: (1 / k) / abs(dlnV(math.exp(lu))), math.log(u_start), math.log(u_end), limit=400)[0]
u_cmb = 2.69e-4
print(f"check: N from the CMB point u* = {u_cmb:.3g} to the end = {efolds(u_cmb):.1f} (should be ~55.7)")
for zeta in (3e4, 3e5, 3e6, 3e8):
    xb = 1 / (4 * zeta); ub = 2 * xb
    dphi_above = (math.log(u_cmb / ub)) / k
    print(f"zeta {zeta:.0e}: tachyon edge x_b = {xb:.2e}; stable plateau above the CMB point = {dphi_above:.2f} M_P; "
          f"max e-folds from the edge = {efolds(ub):.3g}")
