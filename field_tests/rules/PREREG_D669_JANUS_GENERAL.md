# PREREG D669: the Janus relation for a general plateau with an exponential ramp (DpL tick 2, Danny "Ddl" 11:33 CT)
Locked before computation, 2026-11-15. Script theory/modular/janus_general_d669.py; output results/janus_general_d669.txt.
Claim (derived by hand, leading order): for V ≈ 1 − A e^{−pφ} + δ e^{qφ}, with κ = q/p and tilt fraction x = qδe^{qφ*}/(pAe^{−pφ*}),
  1 − n_s = 2pA′(1 − κx), r = 8A′²(1+x)², α_s = −2p²A′²(1+x)(1+κ²x)  (A′ = pAe^{−pφ*}),
  ⇒ ϱ ≡ p√(r/2)/(1 − n_s), x = (ϱ − 1)/(1 + κϱ), α_s = −½(1 − n_s)²(1+x)(1+κ²x)/(1 − κx)².
SERAPIS: p = 2√2, κ = 1/2 (reproduces D635). Kallosh–Linde power-law singular T-model (2512.02969): V = tanh^{2γ}(φ/√(6α))[1 + δcosh^{2β}(φ/√(6α))] → p = √(2/3α), κ = β.
Test (exact first-order slow-roll numerics, ∫V/V′ e-fold count from ε_V = 1, no asymptotic expansion):
- KL model α = 1/3, γ = 1, β = 1 (κ = 1, p = √2), δ ∈ {3e-6, 1e-5, 3e-5}, N* ∈ {50, 55}: compute n_s, r, α_s; predict α_s from (n_s, r) with the general relation; report the error.
- Same for κ = 1/2 (β = 1/2) at α = 1/3 as a second check.
PASS if the general relation's α_s error ≤ 15% at all points (leading-order accuracy, cf. 11–13% for SERAPIS before offsets). Also report the plain attractor value −(1−n_s)²/2 for contrast. No tuning.
