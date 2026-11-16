# PREREG D961: exact effect of Project H's vacuum rescaling (lambda') on SERAPIS-E's N*, n_s and r (locked version of the D956 estimate)
Model: SERAPIS-E in the Project H form V = P3(lambda' Ehat)(1 + C Ehat) (D947; the residual O(C) term is neglected, D947), paper convention Ehat, C = 1.15e-6 fixed.
Reheating channel (D722, sourced in the notes): Gamma = g22^2 m/16pi with g22 = 1.33 M1/M_P fixed by the heavy-neutrino mass, so Gamma ∝ m ∝ sqrt(lambda') at fixed plateau height; T_R ∝ Gamma^{1/2} ∝ lambda'^{1/4}. Baseline T_R0 = 6.7e9 GeV (D722, M1 = m) at lambda' = 1.
Runs: lambda' in {1 (published shape), 1/E(rho,2) = 0.1729, 0.05}; for each, N* solved self-consistently with the toolkit matching equation (nstar.py) using exact-MS r and the exact V*/V_end of that potential; then exact n_s, r at N*.
Reported: N*, n_s, r for each lambda'; Delta n_s and Delta r/r relative to lambda' = 1.
PASS (fixed now, as in the plan): |Delta n_s| < 1e-3 and |Delta r/r| < 5% for lambda' = 0.1729 (the largest value the full-mass route allows, D947). lambda' = 0.05 reported only.
FAIL otherwise: Project H then carries a stated n_s shift; frozen predictions unchanged either way.
Script theory/flux/projH_vacuum_d961.py; output field_tests/results/projH_vacuum_d961.txt.
