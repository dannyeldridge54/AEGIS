# PREREG D2110: Seed v6 step 2, the full positive control on T⁶/(Z₂×Z₆′×ΩR) with discrete torsion, AAA lattice, η_ΩR = −1 (so η_(k) = −1). Locked before computing.

**Source:** the arXiv LaTeX of 1209.3010, downloaded with Danny's OK at 09:08 via his browser. Taken from it:
- Eq. 9 (X, Y, cyclic reading per D2109);
- the fractional cycle Π = ¼(Π_bulk + Σ Π_Z₂);
- χ_ab = ¼(X_aY_b − Y_aX_b − Σ_k Σ_α [x_a y_b − y_a x_b]);
- **the complete exceptional-wrapping table** (tab:exceptional-wrappings-Z2Z6, 9 parity rows × 4 (σʲ; σᵏ) columns), transcribed into tools/seed/z2z6p.py;
- the orientifold images (tab:OR-on-cycles, AAA): X′ = X + Y, Y′ = −Y; x′_α′ = −η(x + y), y′_α′ = ηy, with α′ = α for 1–3 and 4 ↔ 5;
- the AAA twisted tadpoles (tab:twistedRR-AAA+ABB).

**Transcription note:** the source's block-3 α₁ = 1 + σᵏ(4 − 2σᵏ) collides with α₃ at (0; 1). It is read as 1 + σᵏ(4 − 2σʲ), which reproduces the cell's listed α's in all four columns. Recorded here, before the run.

**Ambiguity:** (j, k) for sector i, (P1) cyclic (i+1, i+2) or (P2) increasing order. Both are run; the one that passes is adopted.

**Control (must pass):** Table 27 (stacks a–e with their Z₂ eigenvalues, τ, σ):
1. **every** AAA twisted tadpole cancels, along with the bulk one (= 32);
2. the chiral intersections match Table 28: ab = 1, ab′ = 2, ac = −1, ac′ = −2, bc = 1, bd = 1, bd′ = −3, be′ = −1, cd = −1, cd′ = 3, ce′ = 1; all other pairs among a–e and their images zero. An overall sign convention flip is allowed if applied uniformly.

**Verdict:** PASS means v6 is validated and may spin outward. FAIL means the transcription or convention is owed (reported; nothing used).
