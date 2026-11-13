"""Development 105 (estimate): with the Standard Model outside the supersymmetric sector (D104), is the tail quantum-stable?
And can chi reach the SM only gravitationally? Units M_P = 1. AI-assisted, order of magnitude."""
import math
rho = 7.3e-121; H0sq = rho / 3; g = 0.1; dphi = 19.0
L16 = 16 * math.pi ** 2
# (a) supersymmetric-sector loops today: chi multiplet split by Hubble-induced masses ~ H0^2
mchi2 = (g * dphi) ** 2
dV = mchi2 * H0sq / L16
print(f"(a) chi multiplet, splitting ~H0^2: dV/rho_DE {dV / rho:.1e}, slope shift {2 * dV / dphi / (math.sqrt(2 / 3) * rho):.1e} of the tail slope")
mS2 = 8 * 3e4 * 450 * H0sq
print(f"(a) helper field S (m_S^2 ~ 8 zeta x H0^2, goldstino partner): dV/rho_DE {(mS2 ** 2 / (4 * L16)) / rho:.1e}")
# (b) the SM vacuum energy reaching x through chi
for lab, L in (("TeV", 4.1e-16), ("1e10 GeV", 4.1e-9), ("GUT 1e16", 4.1e-3)):
    ren = (0.05 ** 2) * L ** 6 / (mchi2 * L16 ** 2)                     # renormalisable h = 0.05, chi integrated out
    grav = (L ** 4 / L16) * (L / 1.0) ** 2 * (L ** 2 / mchi2) / L16     # Planck-suppressed only
    print(f"(b) SM cutoff {lab}: x-dependent vacuum energy via chi: h-coupled {ren / rho:.0e} x rho_DE, gravity-only {grav / rho:.0e} x rho_DE")
# (c) chi decaying gravitationally: Gamma ~ m^3/(8 pi M_P^2), m = g dphi; decays when Gamma dphi/phidot = 1
phidot = 3.0e-6
d = (8 * math.pi * phidot / g ** 3) ** 0.25
f = g ** 2.5 * d / (4 * math.pi ** 3 * math.sqrt(phidot))
print(f"(c) gravitational chi decay: decays after dphi {d:.2f} M_P (m_chi {g * d:.3f} M_P), heat share ~{f * 100:.1f}%")
