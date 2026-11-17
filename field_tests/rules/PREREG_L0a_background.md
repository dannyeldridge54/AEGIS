# PREREG L0a (track L): Janus-LT background and distances vs CAMB (written before running)
Janus-LT: tools/janus_lt/background.py as committed with this lock (first-principles constants from scipy.constants; massless neutrinos N_eff = 3.044; CPL dark energy).
Reference: CAMB 2.0.5 (pip), set_cosmology(H0, ombh2, omch2, mnu = 0, num_massive_neutrinos = 0, nnu = 3.044, TCMB = 2.7255, omk = 0), dark_energy_model 'ppf' with w, wa; results = get_background (no perturbations).
Grid: 50 cosmologies, seed 2026: H0 ∈ U[60, 80], ombh2 ∈ U[0.020, 0.024], omch2 ∈ U[0.10, 0.14], w0 ∈ U[−1.3, −0.6], wa ∈ U[−1.5, 0.5] with w0 + wa < −0.1; redshifts z ∈ {0.1, 0.3, 0.51, 0.71, 0.93, 1.32, 2.33, 1100}.
Quantities: H(z), D_M(z) (comoving transverse = radial, flat).
Pass (fixed now): max relative |Δ| ≤ 1e-4 for H and D_M over all 50 × 8 → L0a VALIDATED; ≤ 1e-3 → PARTIAL (report the largest deviations and where); else NOT VALIDATED. Also report median errors and timings.
Script theory/janus_lt/l0a_check.py; output field_tests/results/janus_lt_l0a.txt. Cloud (background only, seconds per cosmology).
