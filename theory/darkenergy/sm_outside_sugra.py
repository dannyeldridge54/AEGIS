"""Development 104 (estimate): the Standard Model outside the supersymmetric sector — what x-dependence survives?
Set-up: the SM is not supersymmetric and couples minimally to the Einstein-frame metric; it meets the twist field only through
gravity, the Nieh-Yan torsion term (derivative coupling to the axial current), and the reheating field chi (Yukawa h to SM
fermions). chi's mass is g |phi - phi0| (D62), so a one-loop chi exchange shifts SM fermion masses by
  d ln m_f / d phi ~ h^2 / (8 pi^2 (phi - phi0)),   phi - phi0 ~ 19 M_P today.
Nucleon: ~5% from quark masses (sigma terms) + Lambda_QCD's heavy-quark thresholds (c, b, t: 2/27 each -> 0.22) -> beta_N ~
0.27 d ln m_q/d phi. Equivalence-principle estimate eta ~ 1e-2 beta_N^2 (composition differences ~1%). AI-assisted, order of magnitude."""
import math
dphi = 19.0
for h in (0.03, 0.1, 0.3, 1.0):
    d = h * h / (8 * math.pi ** 2 * dphi); bN = 0.27 * d; eta = 1e-2 * bN ** 2
    print(f"h {h}: d ln m_f/d phi {d:.1e}; beta_N {bN:.1e} (Cassini 3.4e-3: {'ok' if bN < 3.4e-3 else 'no'}); "
          f"eta ~ {eta:.0e} (MICROSCOPE 1e-15: {'ok' if eta < 1e-15 else 'no'})")
print("gravity-only loops: suppressed by the field's near-exact shift symmetry today (V ~ 1e-120 M_P^4) -> negligible")
print("supersymmetry breaking felt by the SM: none at tree level; the SUSY sector's breaking today is F_S ~ sqrt(rho_DE) ~ meV")
