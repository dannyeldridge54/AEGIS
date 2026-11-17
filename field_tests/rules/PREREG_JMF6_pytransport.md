# PREREG JMF6 — Janus-MF vs PyTransport (an independent transport-method code) on separable AND non-separable 2-field models
Locked 2026-11-17 before any PyTransport spectrum is computed (only a background smoke test has run). Reference: PyTransport 2.0 (jronayne/PyTransport
@603669c, arXiv 1609.00381), build-only patches in tools/janus_calc/pytransport_build.patch; each model compiled from its SYMBOLIC potential (so V and its
derivatives cannot disagree). Method follows the package's own Examples/DoubleQuad/SimpleExample.py: backEvolve(..., exit at end of inflation) from
slow-roll initial velocity, tols 1e-8; pivot k* = kexitN(N_end − 55); ICsBE with NB = 6 e-folds sub-horizon; sigEvolve ζζ at the end of inflation;
n_s from SimpleExample line 104's convention n_s = d ln⟨ζζ⟩/d ln k + 4, evaluated by a quadratic fit of ln⟨ζζ⟩ over 9 points on ln k ∈ ln k* ± 0.4
(same stencil as Janus-MF). Convergence check reported, not a claim: tols 1e-10.
Models and Janus-MF values (already recorded): Q1, Q3, Q9 = JMF2 quadratics (m₁² = 1e-11, R = 1, 3, 9, φ_init (12, 12); Janus-MF n_s 0.963378, 0.945477,
0.927750; MMC 0.963372, 0.945477, 0.927745). N2' = ½m₁²φ₁² + ½m₂²φ₂² + εφ₁φ₂ (1e-11, 9e-11, ε = 1e-12; φ_init (12, 12); Janus-MF 0.946212).
N1 = ½Σm_i²φ_i² + (1/24)φ₁²Σλ_iφ_i² (m² 1e-11, 9e-11; λ 1e-12, 1e-12; φ_init (12.5, 12.5); Janus-MF 0.954583).
Claims: C0 (reference sanity) |n_s^PyT − n_s^MMC| ≤ 2e-4 on Q1, Q3, Q9; C1 |n_s^PyT − n_s^Janus-MF| ≤ 2e-4 on all five models.
C0 and C1 → JANUS-MF VALIDATED ON NON-SEPARABLE (independent reference); C0 fails → INCONCLUSIVE (reference not reproducing MMC); C0 passes and C1 fails
on N1 or N2' → NOT VALIDATED. r is not compared (PyTransport's example tensor route is not used here). Results: field_tests/results/janus_jmf6.txt (+ stamp).
