"""Development 80 arithmetic: one-loop vacuum energy m^4/(64 pi^2) of a particle whose mass depends on x, vs rho_DE. AI-assisted."""
import math
rho = (2.25e-12) ** 4  # GeV^4: dark energy density, (2.25 meV)^4
print(f"rho_DE = {rho:.1e} GeV^4")
for lab, m in (("electron", 0.511e-3), ("muon", 0.106), ("TeV superpartner", 1e3), ("gravitino 1e5 GeV", 1e5)):
    d = m ** 4 / (64 * math.pi ** 2); print(f"  one loop of a {lab} whose mass depends on x: ~ {d:.1e} GeV^4 = 10^{math.log10(d / rho):.0f} x rho_DE")
mmax = (rho * 64 * math.pi ** 2 * 0.1) ** 0.25
print(f"  heaviest particle allowed an x-dependent mass (10% of rho_DE): ~ {mmax * 1e12:.1f} meV")
