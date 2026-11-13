"""Development 86 (estimate): the kination phase tilts inflation's gravitational waves blue at high frequency.
Modes re-entering during a stiff (w = 1) phase gain Omega_GW ~ k^1 relative to the flat radiation-era plateau.
Plateau: Omega_GW h^2 ~ 1.0e-16 (r/0.1) (standard estimate). Kination from the end of inflation until radiation
dominates, a-ratio 1/sqrt(f_eff) (f_eff from D84/D85). Radiation takes over at T_dom = T_RH sqrt(f_eff); today's
frequency of the mode entering then f = 2.65e-8 Hz (T/GeV) (g/106.75)^(1/6)/... (approx). AI-assisted."""
import math
r = 0.0035; plateau = 1.0e-16 * r / 0.1
for lab, feff, TRH in (("heat 0.13%", 4.3e-4, 3e14), ("heat 0.04%", 1.3e-4, 2.1e14)):
    boost = 1 / math.sqrt(feff); Tdom = TRH * math.sqrt(feff); f1 = 2.65e-8 * Tdom; f2 = f1 * boost
    print(f"{lab}: flat plateau Omega_GW h^2 {plateau:.1e} below {f1:.0e} Hz; rises ~ f up to x{boost:.0f} "
          f"= {plateau * boost:.1e} near {f2:.0e} Hz (BBN/N_eff bound ~1e-6; far below any planned detector)")
