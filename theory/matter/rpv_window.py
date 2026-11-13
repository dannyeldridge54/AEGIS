"""Backlog Q (exploratory, order-of-magnitude): is R-parity violation (D53 route A) safe for the matter asymmetry?
Superpartners at m ~ 1e11-1e13 GeV (near m_3/2), radiation era, g* = 106.75 (+ superpartners, ignored: order 1).
(1) No washout: the L-violating RPV rate Gamma ~ lam^2 T / (16 pi) must stay below H(T) = 1.66 sqrt(g) T^2/M_P at
    T ~ m (below m the 2-body processes are Boltzmann-suppressed) -> lam < lam_max.
(2) No relic: the lightest superpartner (thermal relic with annihilation ~ 1/m^2, Y ~ 20 m / M_P... order of magnitude)
    starts to dominate at T_dom ~ m Y; it must decay before then: lam^2 m/(16 pi) > H(T_dom) -> lam > lam_min.
Generic estimates in the style of Campbell, Davidson, Ellis & Olive (washout bounds on B/L violation); AI-assisted."""
import math
MP = 2.435e18; g = 106.75
H = lambda T: 1.66 * math.sqrt(g) * T ** 2 / MP
for m in (1e11, 1e12, 1e13):
    lam_max = math.sqrt(16 * math.pi * H(m) / m)
    Y = 20 * m / MP; Tdom = m * Y
    lam_min = math.sqrt(16 * math.pi * H(Tdom) / m)
    print(f"m = {m:.0e} GeV: no-washout lam < {lam_max:.1e}; no-relic lam > {lam_min:.1e} (LSP would dominate at T ~ {Tdom:.0e} GeV)"
          f" -> window {'OPEN' if lam_min < lam_max else 'CLOSED'} ({lam_max / lam_min:.0e} wide)")
