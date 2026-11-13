"""D118: candidate fix for D116. Give chi an inflaton-dependent mass that SATURATES:
W > (h/2) (1 - exp(-2 pi (T - T0))) chi^2   (a single-instanton factor of the same T; chi = 0 during inflation, so V(T) unchanged)
m_chi(x) = h |1 - exp(-2 pi (x - x0))|: zero at x0 (instant preheating as before), ~ linear just after, -> h on the tail, with the
leftover field dependence ~ exp(-2 pi x). Match D105's slope g = dm/dphi = 0.1 at x0. Units M_P = 1. AI-assisted, estimate."""
import math
c = math.sqrt(2 / 3); MP = 2.435e18; rho = 2.5e-47; L16 = 16 * math.pi ** 2; x_frozen = 73.0
for x0 in (0.02, 0.05, 0.1):
    h = 0.1 / (2 * math.pi * c * x0)                          # g = 2 pi h c x0 = 0.1 at the crossing
    m = lambda x: h * abs(1 - math.exp(-2 * math.pi * (x - x0)))
    # distance travelled when m_chi reaches the D105 decay mass 0.052
    lo, hi = x0, 50.0
    for _ in range(100):
        mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if m(mid) < 0.052 else (lo, mid)
    dphi = math.log(lo / x0) / c
    print(f"x0 {x0}: h {h:.2f} M_P (saturated chi mass), decay mass 0.052 M_P reached after dphi {dphi:.2f} M_P (D105 linear: 0.52);"
          f" during inflation |m_chi| <= {h*(math.exp(2*math.pi*x0)-1):.3f} M_P vs H 6e-6")
    for lab, L in (("TeV", 1e3), ("1e10 GeV", 1e10), ("0.05 M_P", 0.05 * MP)):
        dm2 = L ** 4 / (L16 * MP ** 2)                                     # GeV^2, SM-induced chi/chi~ splitting
        dV_tail = 2 * (h * MP) ** 2 * math.exp(-2 * math.pi * (x_frozen - x0)) * dm2 / L16    # field-dependent part only
        print(f"   SM loops to {lab:>8}: field-dependent dV on the tail ~ 10^{math.log10(dV_tail/rho):.0f} x rho_DE")
