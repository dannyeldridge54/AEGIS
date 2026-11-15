# PREREG D643 (W6): soft masses vs matter modular weight, and gaugino masses at τ = i
Locked before computation, 2026-11-15. Script theory/modular/matter_weights_d643.py; output results/matter_weights_d643.txt.
1. Same set-up as D639 (W = W0 + fS, f² = 2W0², τ = i, Λ = 0). Visible K ⊃ |Q|²/(−i(τ−τ̄))^k for k ∈ {0, 1/3, 2/3, 1, 4/3, 2}. Report m_Q²/m3/2² (exact). Expectation (analytic): 1 − k. Tachyonic for k > 1.
2. Gaugino masses from F_τ: M_1/2 = F^τ ∂_τ f / (2 Re f). For a modular-invariant threshold f ⊃ b·L(τ), L = −ln(2y|η|⁴), compute ∂_τ L at τ = i numerically (expect 0 by stationarity; D574A) → no tree-level gaugino mass from F_τ.
3. Arithmetic (estimates, labelled): m3/2 = 1.05–1.2e11 GeV → AMSB gaugino ~ b g² m3/2/16π² (b = 1–3 ... |b| ≤ 33/5, g² ≈ 0.5 at 1e10 GeV); generic one-loop scalar m ~ m3/2/4π; pure two-loop AMSB scalar ~ g² m3/2/16π². Compare with the high-scale-SUSY Higgs bound M_S ≲ 2e10 GeV.
Verdict: if (1) gives 1 − k and (2) gives 0, the soft-mass statement in the paper is: tree scalar masses vanish exactly for weight-1 matter, are positive for k < 1 (∝ (1−k)m3/2²) and tachyonic for k > 1; gauginos are loop-induced; the loop scale is quoted as a range.
