# PREREG D1944 — α_s theory error: the top-Yukawa two-loop term (locked 21 Nov 2026 before running; repo at 6efba6cf)
Script: theory/tests/d1944_as_yukawa.py. It uses the same two-loop gauge running as weave_rg2, plus the top-Yukawa two-loop term:
- d = (17/10, 3/2, 2) in the SM and (26/5, 6, 4) in the MSSM;
- y_t → y_t/sin β above the scalars;
- one-loop y_t running from y_t(M_Z) = 0.94 (estimate);
- spectrum: wino 686.5 GeV, gluino 4926.4 GeV, scalars 4.7e5 GeV, tan β = 2.
**Validation:** with the Yukawa term off, the script must reproduce 0.1142 ± 5e-4. Otherwise VOID.
**Theory-error readings:** (1) the computed Yukawa shift; (2) gluino ± 20 % (Jacobian D1937); (3) the engine's label ± 0.004. The quoted theory error is the quadrature of (1) and (2); the label is replaced by the computation.
**Verdict:** PASS if |pull| ≤ 2 using σ_exp ⊕ σ_theory. Otherwise FAIL. The experimental-only pull is reported as well.
This applies under the single-stack assumption (D1942).
