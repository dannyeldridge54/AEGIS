# PREREG JMF8 — Janus-MF with THREE fields vs PyTransport
Locked 2026-11-17 before any JMF8 number. Same method and references as JMF6 (PREREG_JMF6_pytransport): PyTransport from the symbolic potential,
n_s by its example convention on the same 9-point stencil; pivot 55 e-folds before ε = 1. Janus-MF (tools/janus_calc/mfms.py, unchanged) handles n fields.
Models: T1 separable V = ½Σ m_i²φ_i², m² = (1, 9, 25)×1e-11, φ_init (12, 12, 12);
T2 non-separable V = ½Σ m_i²φ_i² + ε(φ₁φ₂ + φ₂φ₃), same masses, ε = 1e-12, φ_init (12, 12, 12).
Claim per model: |n_s^Janus-MF − n_s^PyT| ≤ 2e-4 (as JMF2–JMF6). Both → JANUS-MF VALIDATED FOR THREE FIELDS. Also reported: PyTransport tol 1e-8 vs 1e-10,
Janus-MF r, adiabatic check (Janus-MF P_R at end_back 1 vs 0). Results: field_tests/results/janus_jmf8.txt (+ stamp).
