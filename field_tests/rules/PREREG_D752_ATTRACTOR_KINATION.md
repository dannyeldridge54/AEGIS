# PREREG D752: can a plain attractor (n_s = 1 − 2/N*) reach the SERAPIS band through a longer (kination) reheating, given the gravitational-wave ΔN_eff bound?
Locked 2026-11-16 before computing. Script: theory/modular/attractor_kination_d752.py. Output: field_tests/results/attractor_kination_d752.txt.
## Inputs (fixed now; estimates labelled)
- Instant-reheating N* from the D719 matching equation with V*^{1/4} = 4.8e15 GeV, ρ_end = V*/2, ln(k/a₀H₀) = 5.404, g* = 106.75.
- A kination phase (w = 1) from ρ_end down to ρ_k adds ΔN* = (1/12)·ln(ρ_end/ρ_k).
- The GW spectrum is blue during kination (Ω_GW ∝ f¹), so the peak enhancement over the flat value is (ρ_end/ρ_k)^{1/3}.
- Flat value Ω_GW,flat ≈ 3.6e-16·(r/0.1) with r = 5e-4 (from memory, labelled; uncertain by ×3).
- ΔN_eff < 0.2 gives ∫Ω_GW d ln f ≲ 1.1e-6 (from memory, labelled). The bound is applied to the peak, which is conservative by an O(1) log factor.
## Decision rule
Report the maximum ρ_end/ρ_k, the maximum ΔN*, the maximum attractor n_s = 1 − 2/N*_max, and the separation from the band edge 0.970 for σ(n_s) = 0.0016 (SO+SPHEREx, 1σ reading) and 0.0008 (95% reading).
- If n_s,max < 0.970: the GW bound rules out reaching the SERAPIS band with a plain attractor plus kination. State the forecast separation at n_s = 0.972.
- Also report the variation for an Ω_GW,flat ×3 or ÷3 uncertainty.
