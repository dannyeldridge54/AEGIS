"""Development 88 (estimate): gravitinos from the hot plasma at T_RH ~ 3e14 GeV, and how m_3/2 moves with x. AI-assisted.
Thermal yield (Bolz-Brandenburg-Buchmuller form, gluino mass ~ m_3/2, heavy-gravitino limit): Y ~ 1e-12 (T_RH/1e10 GeV),
order of magnitude. Decay width Gamma ~ m^3/(4 pi M_P^2) x O(1); decays when H = Gamma (radiation era).
In the Twist m_3/2 = |W0| e^{K/2} with K = -3 ln(2x): m_3/2 ~ x^{-3/2}, so it depends on where x sits (D80)."""
import math
MP = 2.435e18; g = 106.75
TRH = 3e14; Y = 1e-12 * TRH / 1e10
for m in (1e11, 1e12, 1e13):
    G = m ** 3 / (4 * math.pi * MP ** 2); Td = (G * MP / (1.66 * math.sqrt(g))) ** 0.5
    frac = m * Y / (0.75 * Td)
    print(f"m_3/2 {m:.0e} GeV: Y {Y:.0e}, decays at T ~ {Td:.1e} GeV, energy share at decay ~ {frac:.1e} (<1: never dominates; long before BBN)")
for xr, xt in ((0.01, 450), (1.0, 450)):
    print(f"m_3/2 ratio reheating (x={xr}) / today (x={xt}): {(xt / xr) ** 1.5:.1e}")
