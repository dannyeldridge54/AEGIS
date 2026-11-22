# PREREG D2119: fixes for referee round 1 (negative pole; report R1-1 … R1-11). Locked before computing.

**R1-2 (normalisation, CONFIRMED by quote):** p.tex line ~1816 says 4π/g² = 2π Re f. So the thresholds enter as δ(α⁻¹) = 2π Re δf. This is now the **primary** normalisation; norm = 1 is kept only as a comparison.

**R1-3 (reading):** the two-typo reading, where the expression equals its stated asymptote, is the minimal consistent one. That is **variant A, now primary**. Variant B is demoted to a comparison.

**R1-1 (method):** the solutions form a 1-parameter curve. Minimise ctrl = max|δ|/T over that curve with SLSQP: residuals = 0, v_i ≥ 1, 0 < g_s < 1, from 40 random starts per case.
- Cases: {A, B} × {reduced, non-reduced} × {2π, 1}.
- Locked criterion unchanged: controlled if min ctrl < 0.3.
- Every reported point is re-verified with fsolve (residual < 1e-10).
- **K7 verdict = the case (A, reduced, 2π)**, with the others reported.

**R1-4 / R1-5 (uniqueness):** rescan with the P2 convention, the 5,000 cap removed, and the signature extended to (ab, ab′, ac, ac′, bc, bc′, self-χ, sorted hidden N, Σ|χ_vis-hid|, per-stack vis–hid |χ|). Report distinct visible triples separately from raw counts.

**R1-9:** commit the K4 output under P2 as JSON.

**R1-10 (ESTIMATE):** ΔN_eff in three cases:
1. vectors only (g = 12);
2. vectors plus hidden-only chiral fermions;
3. everything massless: vectors, gauginos, and hidden-only chiral multiplets (d adjoints, dd′ and ee′ sym/anti, de′).

Use g*s(T_dec) = 228.75 + g_hidden. Compare each with the 0.3 bound.

**R1-6, R1-7, R1-8, R1-11:** wording and disclosure fixes in the paper and the notes.

All verdicts stand as computed. No reruns.
