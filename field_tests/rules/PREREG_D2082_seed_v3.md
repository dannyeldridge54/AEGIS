# PREREG D2082: Seed v3, an exact consistency landscape on T⁶/(Z₂×Z₂) with a tilted 3rd torus, using the D2081 shortcuts. Locked before running.

**Branes.**
- Each brane has integer wrappings (n_i, m_i) with |n|, |m| ≤ L = 3, each pair coprime; on torus 3, m̃ = m − n/2 (the CSU convention).
- Canonical form up to sign flips on two tori and up to the orientifold image.

**SUSY (A1, exact).** The radii are fixed on a rational grid, χ_i ∈ {1/2, 1, 3/2, 2, 3}³ (125 points). With z = Π(n_i + iχ_i m_i), SUSY means Im z = 0 exactly (Fractions) and Re z > 0. This is algebraically the same as θ₁ + θ₂ + θ₃ = 0 for the principal angles, and Re z > 0 picks the brane over the anti-brane.

**Tadpoles (CSU Eq. 2).** Σ N_a (X⁰, X¹, X², X³)_a = (16, −8, −8, −16), with:
- X⁰ = n¹n²n³
- X¹ = n¹m²m̃³
- X² = m¹n²m̃³
- X³ = m¹m²n³

N_a ∈ 2Z⁺ (the stack counts include images, as in CSU).

**Visible pair.**
- Stack A has N_A ∈ {6, 8} (U(3), or U(4) ⊃ U(3) as in CSU's 6+2).
- Stack B has N_B = 4.
- Left quarks: |I_AB| + |I_AB′| = 3, with I = Π(n_a m̃_b − m̃_a n_b).

**Hidden completion (A2/A3, exact count).** Any multiset of SUSY branes with N ∈ 2Z⁺ whose charges complete the residual exactly. It is counted with a memoised DP over (brane index, residual charge, K-parity).

**K-theory (A5, probe form).** For each probe p, one of the four O-plane-parallel CSU filler cycles (A1, A2, B2, C2 types), Σ_a (N_a/2)·I_ap ≡ 0 mod 2.
- **Convention check:** the CSU seed itself must pass. If it fails, the convention is wrong; stop and report.

**Positive control (must pass, or stop).** At χ = (1, 3, 2), which is in the CSU SUSY family χ₁ = χ₃/2, χ₂ = 3χ₃/2:
- the CSU visible pair (C₁ with N = 8, B₁ with N = 4) must be found;
- its hidden-completion count must be ≥ 1, including the CSU fillers (A₁ N = 8, A₂ N = 2, B₂ N = 2, C₂ N = 4).

**Report:**
- per-χ and total counts: SUSY branes, 3-family visible pairs, completed models (tadpole + K);
- the number of inequivalent visible pairs.
- **Look-elsewhere:** the full total of models tried is printed.

**Not filtered (stated):** chiral exotics between the hidden and visible sectors, a massless U(1)_Y, and α_s. α_s is deferred to v4 via the BLS relation, whose model class must be checked first.
