# PREREG D489 — golden / silver ratio test on the Twist's outputs (Danny 20:26 CT: "look for golden ratio silver ratio overlaps"), locked BEFORE looking.
Set (fixed now; model OUTPUTS only, inputs like m₂ = 4/π, μ = 1 excluded): n_s 0.9736, r 0.0046, N* 57.2, x_E 29.6, x_E2 135.14, ζ_max 0.0274, Λ₂/Λ 0.23,
|c| 0.3728, ΔN_eff 0.065, 0.081, β 0.277, c_γ 1.7, 4.1, m_KK/T 6.12, S 242, 267, τ_inst 39, 43, m₃/₂ 1.7, 4.7, ε (Route A) 3.04e-7, α_s 7.7e-4,
M_s/M_P 1.43e-4, x_min 29.36, T_ret/T_cap ratio 237/1.5e11.
Test: all pairwise ratios R = max/min (and each value itself if > 1). Count R within 1% of φ = 1.6180, φ² = 2.6180, δ_S = 1 + √2 = 2.4142, δ_S² = 5.8284.
Null: same count for 2000 random sets of the same size, log-uniform over the same overall range (seeded, rng 20261114). p = fraction of random sets with ≥ observed count.
Verdict: "OVERLAP SIGNIFICANT" if p < 0.01; "NO MORE THAN CHANCE" otherwise. Any individual hits are listed but not interpreted.
