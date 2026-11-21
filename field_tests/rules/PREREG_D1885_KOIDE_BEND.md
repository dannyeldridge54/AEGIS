# PREREG D1885 — Koide's bend as a discrete Wilson-line shift of the electron on the turnover (locked 21 Nov 2026 before computing; repo at 1468c0d2)
D1879 needs the electron's coupling (amplitude, since m ∝ |ψ|) lowered by ×6.6 relative to equal corner weights, with μ, τ unchanged.
On T²/Z₃ (τ = ω) a Z₃-compatible Wilson line can only translate a mode by a fixed-point difference, i.e. move it from its own corner to another corner. So the electron's coupling at the Higgs corner becomes the amplitude its Z₃ sector has at a DIFFERENT corner.
Test: tool theory/tests/z3_modes.py, (M, a) ∈ {(3, 1/6), (6, 0), (9, 1/6)}; for each Z₃ eigenmode, ratio r = |ψ(c_other)| / |ψ(c_own)| for the two other fixed points (c_own = the fixed point of largest |ψ|).
Verdict: PASS if some r ∈ [0.117, 0.197] (1/6.6 ± 30 %); FAIL if all r lie outside (expected from D1849's "≈ 0 at the other corners" — stated before computing).
