# PREREG A3c (track X, Hyperion; manual Djl 17 Nov 05:52 CT): neutron stars — common surface rule + data comparisons (written before running)
Follows A3b (D1058: NOT VALIDATED only on N4, radii 1.2–1.8e-5 apart because ns.tov_tidal stopped at ρ = 1e4 g/cm³ and compact.tov at P = 0).
Code: tools/janus_astro/ns.py as committed with this lock (tov_tidal gains rho_surf, default unchanged 1e4 g/cm³); script theory/janus_astro/a3c_check.py (= a3b_check.py with N4 run at rho_surf = 1e-3 g/cm³, i.e. effectively P → 0, plus the data comparisons below).
Validation: N1–N3 exactly as PREREG_A3b; N4 with the common surface rule, M and R relative ≤ 1e-5. Pass N1–N4 → A3c VALIDATED.
Data comparisons (the EoS against measurements; reported as consistent / inconsistent, not code verdicts), numbers sourced:
- GW170817: Λ_1.4 = 190 (+390/−120), 90% (arXiv:1805.11581) → consistent if 70 ≤ Λ_1.4 ≤ 580.
- PSR J0740+6620 (Dittmann et al. 2024, arXiv:2406.14467): M = 2.08 ± 0.07 M_⊙, R = 12.92 (−1.13/+2.09) km at 68% → M_max ≥ 2.01; R at min(2.08, M_max) inside [11.79, 15.01] (68%) and inside the doubled interval [10.66, 17.10] (≈ 95%, stated approximation).
- PSR J0614−3329 (arXiv:2506.14883): M = 1.44 M_⊙, R = 10.29 (+1.01/−0.86) km at 68% → R(1.44) inside [9.43, 11.30] (68%) and [8.57, 12.31] (doubled).
Output field_tests/results/janus_astro_a3c.txt. No reruns to chase; DEVIATIONS first.
