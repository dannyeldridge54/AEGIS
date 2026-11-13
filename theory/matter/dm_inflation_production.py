"""Development 58 (exploratory): does inflation itself overproduce the gravity-only dark matter (D38)? AI-assisted.
A light (m << H_inf), minimally coupled spectator scalar reaches <X^2> = 3 H^4/(8 pi^2 m^2) during inflation
(Starobinsky-Yokoyama); its energy m^2<X^2>/2 = 3 H^4/(16 pi^2) stays frozen until H = m, then redshifts as matter.
Compare rho_X/s at H = m (radiation era) with the observed dark-matter value rho/s = 0.44 eV.
A fermion (or conformally coupled scalar, xi = 1/6) is conformal when massless: no such condensate; gravitational
production at H ~ m gives n ~ m^3 x O(1e-3), negligible for m << H_inf (estimate, not computed in detail)."""
import math
MP = 2.435e18; g = 106.75; H_inf = 1.2e13; target = 0.44e-9          # GeV
for m in (1e5, 1e6, 1e7):
    rho = 3 * H_inf ** 4 / (16 * math.pi ** 2)
    Tm = math.sqrt(m * MP / (1.66 * math.sqrt(g)))
    s = 2 * math.pi ** 2 / 45 * g * Tm ** 3
    print(f"scalar m = {m:.0e} GeV: rho_X/s = {rho / s:.1e} GeV vs needed {target:.1e} -> overproduced by 10^{math.log10(rho / s / target):.0f}")
print("fermion branch at the derived T_RH (D42, 3-5e14 GeV), scaling D38's fermion light branch m = 1.79e8 (1e14/T_RH)^3:")
for T in (3e14, 4e14, 5e14):
    print(f"  T_RH {T:.0e}: m = {1.79e8 * (1e14 / T) ** 3:.1e} GeV")
