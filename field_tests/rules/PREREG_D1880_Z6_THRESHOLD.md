# PREREG D1880 — Δ₃ from the two N=2 sectors of the Z₆-II fold (locked 21 Nov 2026 before computing; repo at 69a5080e)
Z₆-II twist (1/6, 1/3, −1/2): θ³ fixes torus 2 (Z₃-twisted ⇒ U₂ = ρ; subgroup {1,θ³}, |G_t|/|G| = 1/3); θ² fixes torus 3 (Z₂-twisted, U₃ = i in the Weave; subgroup {1,θ²,θ⁴}, |G_t|/|G| = 1/2).
Threshold per torus (D1816 form, U only): shift per unit b = −ln(Im U|η(U)|⁴)/(4π): ρ → 1.034/4π; i → −4 ln(Γ(1/4)/(2π^{3/4}))/(4π). Residual (D1820 closure, re-derived): R = −0.237 (1 − X/2.88), X = Σ_t w_t [(b₂−b₃)_t + 0.714 (b₂−b₁)_t], w_t = (shift_t/0.0822) × g_t.
Variants: (A) g_t = 1 (D1816 normalisation); (B) g_t = DKL factors 1/3 (ρ) and 1/2 (i).
Content per torus (N=2 sector): split-stack vectors V ∈ {absent, (0,−4,−6)}; h_d ∈ {0,1,2} doublet hypers, each (0.6, 1, 0); h_t ∈ {0,1,2} triplet hypers, each (0.4, 0, 1). 18 options per torus, 324 combinations.
Pass: |R| ≤ 0.05. Report pass fraction (chance level) and the minimal passing combos (fewest hypers) per variant.
Verdict: PASS if variant B has a passing combo with ≤ 2 hypers total; PARTIAL if only variant A does; FAIL otherwise.
