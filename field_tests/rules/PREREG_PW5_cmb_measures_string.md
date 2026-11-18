# PREREG PW5 — postulate 5 (pattern from W1/W2: C and N* move n_s the same way but r opposite ways): CMB data measure the string product Im S·Im ρ
Postulate (node string_meter, status postulate/forecast): with C = 15 N_eff/(64π⁶ Im S·Im ρ) (BHK, NA11), a measurement of (n_s, r) determines ln C — hence ln(Im S·Im ρ) — and the reheating temperature, through the measured response matrix at the A1 point.
Inputs (measured, W1 D1257 at C 1.15e-6, T_R 1e7; W2 D1258): ∂n_s/∂ln C from w_C (Δn_s ±1.18e-3 for ±10 %), ∂(ln r)/∂ln C from w_C (±2.85 %); ∂n_s/∂log₁₀T_R and ∂ln r/∂log₁₀T_R from w_T (7.75e-4, ∓2.14 %).
Forecast noise: SO+SPHEREx σ(n_s) = 0.0016 (D751); LiteBIRD optimistic σ(r) = 5e-5 (D749a) → σ(ln r) = 5e-5/4.82e-4.
Compute: Fisher matrix F = Jᵀ N⁻¹ J for (ln C, log₁₀T_R); marginal σ(ln C) = σ(ln Im S·Im ρ), σ(log₁₀T_R); also the n_s-only case with T_R fixed.
Pre-stated expectation: n_s only (T_R fixed): σ(ln C) ≈ 13 %; with r (LiteBIRD optimistic): σ(ln C) ≤ 20 % after marginalising T_R, σ(log₁₀T_R) ≤ 3 decades.
Check (internal consistency): the response ratio (Δln r/Δn_s) for C must equal the slope of the PW1/A1 parallelogram's C-edges, and for T_R its T_R-edges, within 10 %.
Results: field_tests/results/pw5_cmb_measures_string.txt.
