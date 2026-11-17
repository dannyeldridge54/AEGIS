# PREREG JMF9 — Janus-MF on a curved field space vs PyTransport NC (large list 3)

Locked 2026-11-17 18:00 CT, before the curved-space Janus-MF code is written or run.
Equations (fetched, arXiv 1511.09148, Kaiser et al.): Eq. 14 background D_t φ̇^I + 3H φ̇^I + G^{IJ}V_J = 0; Eq. 15 D_t A^I = Ȧ^I + Γ^I_{JK}A^J φ̇^K;
Eq. 16 H² = (σ̇²/2 + V)/3, Ḣ = −σ̇²/2 (M_P = 1), σ̇² = G_IJ φ̇^I φ̇^J; Eq. 18 D_t²Q^I + 3H D_t Q^I + (k²/a² δ + M)^I_J Q^J = 0;
Eq. 19 M^I_J = G^{IK} D_J D_K V − R^I_{LMJ} φ̇^L φ̇^M − (1/a³) D_t(a³ φ̇^I φ̇_J / H); Eq. 24 R = (H/σ̇) Q_σ.
Implementation plan (fixed): e-fold time; the transport is done in the coordinate basis with Christoffels from the metric (sympy, exact), the
covariant derivative of Q written out with Γ; P_R from the projection of the Q two-point matrix on the unit adiabatic vector with the metric
(w_I = G_IJ φ'^J/σ'), P_R = w·P_Q·w / σ'² (reduces to the flat JMF form when G = δ).
Self-check before comparison (must pass or the code is fixed via DEVIATIONS first): with G = δ the new code reproduces spectra_mf's n_s on DQuad to ≤ 1e-6.
Model: PyTransport example DoubleQuadNC, V = ½m1²φ1² + ½m2²φ2², G = diag(M², M² sin²φ1), compiled here as PyTransJNC_DQuad (gravipy from GitHub source).
Parameter point (fixed): m1 = 1e-5·√(something not tuned) → use PyTransport's own example values if the example script gives them; otherwise
m1 = 1e-5, m2 = 1e-5/9 · 9 ... NO: fixed choice = PyTransport example values; if absent, (m1, m2, M) = (1e-5, 0.9e-5, 20) with φ0 = (6.0, 1.0) — written into the DEVIATION if absent values force the fallback.
Nstar = 55 e-folds before the end (ε = 1). n_s from P_R over ln k ∈ [−0.4, 0.4], 9 points (as JMF6).
Claim: |n_s^Janus-MF-NC − n_s^PyT| ≤ 2e-4 → JANUS-MF VALIDATED ON CURVED FIELD SPACE; else NOT VALIDATED (fixes only via DEVIATIONS, no reruns to chase).
Also reported: PyTransport tol 1e-8 vs 1e-10.
