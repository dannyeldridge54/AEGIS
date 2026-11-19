# PREREG_P3D6 — P3-D (6D at horizon exit) exact-shape test, locked D1589, 2026-11-19 11:33 CT

Question: does the dimension at horizon exit set r as D1588 says (r = 8/((D−2)N²)), once the tilt is included?

Model (PROXY, stated before running): the P3-S potential V = (⅔·y∂_y ln E(τ,3/2))²·[1 + C(E − E(ρ))] on x = ½, but with
the 6D canonical normalisation y = e^{ψ} (β₆ = 2) instead of 10D's y = e^{√2 φ} (β₁₀ = 2√2). The SL(2) function stands in for the
6D codon near the end of inflation (6D codon slice has no clean end without non-perturbative terms — D1588 caveat). Script =
species32/run.py with SQ2 → 1 only (field_tests/scripts/p3d6/run.py). Engine F (self-consistent N*, TR = 8.94e8).

Grid (fixed): C ∈ {0, 2e-7, 4e-7, 8e-7, 1.6e-6, 3.2e-6}. One run each, no reruns.

Report: n_s, r, α_s, N* per C; r interpolated (linear in C between bracketing rows) at n_s = 0.9706.
Pass rule for D1588's estimate: r(n_s = 0.9706) within ±30 % of 1.1e-3 ⇒ CONSISTENT; otherwise D1588's tilted estimate is WRONG
(the untilted formula is checked separately at C = 0: r within ±10 % of 7.9e-4).
If n_s = 0.9706 is not bracketed, report "not bracketed" — no grid extension without a DEVIATIONS file written first.
