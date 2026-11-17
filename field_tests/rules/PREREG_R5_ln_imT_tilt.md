# PREREG R5 — does the ρ-branch GS match survive with the S'-frame tilt variable ℓ = −ln(2 Im T) instead of L? (D1044 question)
Locked 2026-11-17 before any R5 number. Same code as R1 (r1_gs_tilt.py, D1010) with SL(φ) = ℓ(y) − ℓ(y_ρ), ℓ = −ln(2y), in place of
L − L_ρ (L = −ln(2y|η|⁴)); V = P/(1 − κ SL). Step 1: solve κ* so n_s matches the published SERAPIS-ρ (ε = 6e-5) at N* = 49.49
(bracket κ ∈ [−0.2, 0.2], brentq; if no sign change, record NO κ REPRODUCES n_s). Step 2 at κ*: compare r and α_s at N* = 46.09,
49.49, 55 with the published model. Claim SURVIVES if |Δn_s| ≤ 3e-4 at all three N* (as R1 T1) AND |Δr/r| ≤ 2%, |Δα_s| ≤ 2e-5;
else FAILS (ℓ is not an equivalent tilt variable). κ*/ε reported (changes the required δ_GS/2Re S').
Results: field_tests/results/r5_ln_imT.txt.
