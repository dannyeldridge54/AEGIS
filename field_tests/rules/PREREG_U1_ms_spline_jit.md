# PREREG U1 — upgrade loop, counterpart 1: compiled exact Mukhanov–Sasaki for SERAPIS-E (spline potential, analytic dV)
Locked before building/running. Motivation: TK1 (D1254) — tools/serapis_calc/ms.spectra costs ~63 s per k and its α_s is step-dependent noise (finite-difference dV on a spline inside the mode equation).
Build: tools/serapis_calc/ms_jit.py gains build_spline(model, C) — the SAME pipeline potential (cubic spline of E(τ,2) − E(ρ,2) on 4000 points, V = e/(e+1)(1 + C e), analytic dV from the spline derivative) evaluated inside numba; integration by the existing ms_jit integrator (DP45, rtol 1e-12, atol 1e-30, a normalised at the pivot, exact de Sitter BD start at k/aH = 200). build(Vexpr, y) is unchanged (refactored only through a shared _make(V, dV)).
Tests (all at the TK1 points: C 1.0e-6 / 1.15e-6, N* 50.7 and the TK1 e2e N*):
 T1 equivalence vs ms.spectra (TK1 rows): |Δn_s| ≤ 3e-6, |Δr/r| ≤ 1e-4.
 T2 speed: ≥ ×20 faster per 5-k spectrum than ms.spectra (63 s per k ⇒ ~315 s), first call (compile) excluded.
 T3 α_s stability: α_s from step sets ±0.025, ±0.05, ±0.1 (5 k each) agree within 2e-5.
 T4 α_s vs Janus core spectra3: |Δα_s| ≤ 3e-5 (pre-stated expectation: the third-order flow is accurate to ~1e-5 in α_s for this plateau).
Verdict per test; U1 adopted (serapis_ms tool switches to the compiled path) only if T1–T3 PASS. Results: field_tests/results/u1_ms_spline_jit.txt.
