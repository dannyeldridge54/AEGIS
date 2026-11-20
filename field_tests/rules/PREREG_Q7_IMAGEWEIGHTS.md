# PREREG_Q7_IMAGEWEIGHTS — BIG LOOP Q7: basin weight per image of i on the level-4 cover (locked D1674, 2026-11-20 00:25 UTC)
Argument: the Zhinü flow is SL(2,Z)-equivariant, flow(hτ₀) = h·flow(τ₀). A start uniform on the Γ(4) cover is a uniform start in F (D1610: 69% → i, 31% → ρ-type) composed with a uniform coset h ∈ SL(2,Z)/Γ(4) ≅ S₄. An i-ending start ends at h·i, whose residual Z₂ is hSh⁻¹.
Computation: over all 24 group elements h (S₄ triplet of D1668), count how often hSh⁻¹ equals each of the 6 conjugates, and the fraction landing on TM1-type conjugates (charged leptons at ω, fixed by ST).
Prediction to check: each conjugate appears 4 times (the centraliser of S has order 4), so P(TM1 | i-ending) = 1/2 and P(TM1) = 0.69 × ½ ≈ 0.345.
Script: field_tests/scripts/s4img/weights.py
