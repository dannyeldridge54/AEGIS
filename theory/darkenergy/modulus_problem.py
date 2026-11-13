"""Development 94 (estimate): if the size half x is held in a valley today (D92-93), what does its oscillation do?
x freezes after kination at x_f (Hubble friction) and starts oscillating about the valley at x_s when H ~ m_x.
Oscillation energy fraction at that moment ~ dphi^2/6 (dphi = sqrt(3/2) ln(x_s/x_f), Planck units); it then grows like a
relative to radiation (behaves as matter). A light modulus (m_x << MeV) never decays: its relic Omega = fraction * T_osc/T_eq
(times O(1)). AI-assisted, order of magnitude."""
import math
MP = 2.435e18; g = 106.75; Teq = 0.8e-9                         # GeV
for m_eV in (4e-3, 1.0, 1e6, 1e14):
    m = m_eV * 1e-9; Tosc = (m * MP / (1.66 * math.sqrt(g))) ** 0.5
    for dphi in (1.0, 1e-3):
        frac = dphi ** 2 / 6; Om = frac * Tosc / Teq
        print(f"m_x {m_eV:.0e} eV: starts at T ~ {Tosc:.1e} GeV; amplitude {dphi:g} M_P -> relic ~ {Om:.0e} x critical")
    need = math.sqrt(6 * 0.26 * Teq / Tosc)
    print(f"   amplitude must be below {need:.1e} M_P (x_s/x_f within {need / math.sqrt(1.5):.0e}) unless it decays")
