# PREREG JMF4 — JANUS-MF on NON-separable 2-field potentials vs MultiModeCode
Locked 2026-11-17 before any JMF4 number. Code under test: tools/janus_calc/mfms.py (unchanged since D1162). Reference: MultiModeCode exact
n_s, r (same build and parsing as JMF3, with JMF3's DEVIATIONS D1/D3 settings from the start: get_runningofrunning and use_deltaN_SR off —
side outputs that need V''' and do not feed the exact n_s, r).
Potentials [MMC modpk_potential.f90, read from source]:
 N1 (case 11, quadratic + quartic interaction): V = ½Σ m_i²φ_i² + (1/24) φ_1² Σ λ_i φ_i², m² = (1e-11, 9e-11), λ = (1e-12, 1e-12),
    φ_init (12, 12). [φ_1 is the lightest field, as MMC's minloc picks.] Coupling is O(1) of the mass term at φ_init — genuinely non-separable.
 N2 (case 12, off-diagonal mass matrix): V = ½Σ m_i²φ_i² + Σ_{i≠j} ε φ_iφ_j = ½m_1²φ_1² + ½m_2²φ_2² + 2εφ_1φ_2, m² = (1e-11, 9e-11),
    ε = 1e-12, φ_init (12, 12).
Janus-MF gets V, grad and exact Hessian (written out by hand in the script); pivot 55 e-folds before ε = 1.
Claims: C1 |n_s^J − n_s^MMC| ≤ 2e-4, C2 |r/r_MMC − 1| ≤ 2e-3 for each model. All four → JANUS-MF VALIDATED ON NON-SEPARABLE; any fail → NOT.
A model with no result from either code is LISTED (verdict PARTIAL). Hessians also checked against a finite difference before scoring
(max rel diff ≤ 1e-5, else the model is LISTED as a script error). Wall limit 40 min. Results: field_tests/results/janus_jmf4.txt (+ stamp).
