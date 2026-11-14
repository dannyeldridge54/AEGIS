# PREREG D325: does the Green–Schwarz shield fix (GM μ + weights + δ_GS = −27) spoil inflation? (locked before computing)

Locked 14 Nov 2026, ~06:25 CT (cloud). AI-assisted.

Setup (D325): the GS dilaton enters as K ⊃ −ln(ℓ), ℓ = S + S̄ − δ′ ln(T + T̄), with δ′ = 27/16π² = 0.171 and ℓ = 2/g² = 3.98 (α_GUT = 1/25)
held fixed by the heavy dilaton. That turns −3 ln(T+T̄) into an effective −3α ln(T+T̄) with α = 1 − s·δ′/(3ℓ), where s = ±1 (the sign is not
fixed by our normalisation), i.e. α = 0.98567 or 1.01433.

Computation: theory/review/gs_alpha_ns_d325.py. Take the D285b TWIST-K slow-roll code (n = 125, μ = 1, N* = 57). Multiply V by (x/x_ref)^{3(1−α)}
(the e^K change; x_ref only rescales V) and use the canonical field φ with x = e^{√(2/(3α)) φ}. Report n_s and r for α = 1 (baseline), 0.98567
and 1.01433.

Rule: |Δn_s| ≤ 0.004 from the α = 1 baseline for BOTH signs → the GS fix is compatible with inflation. |Δn_s| > 0.004 for both signs → it
spoils inflation. Mixed → the sign decides; record which sign is needed, and the fix becomes conditional on that sign.
No reruns to chase a result; fixes go in PREREG_D325_GS_ALPHA_DEVIATIONS.md.
