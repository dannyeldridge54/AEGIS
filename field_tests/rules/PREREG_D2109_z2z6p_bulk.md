# PREREG D2109: Seed v6 step 1, the bulk-level positive control on T⁶/(Z₂×Z₆′×ΩR) with discrete torsion, AAA lattice (1209.3010). Locked before computing.

**Formulas (1209.3010, quoted):**
- **Eq. 9:**
  - X = n¹n²n³ − m¹m²m³ − Σ_{i≠j≠k≠i} nⁱmʲmᵏ
  - Y = Σ_{i≠j≠k≠i} (nⁱnʲmᵏ + nⁱmʲmᵏ)
- **SUSY (Table 4, AAA):** Y = 0 (necessary) and 2X + Y > 0.
- **Bulk tadpole (AAA):** Σ_a N_a(2X_a + Y_a) = 4(η_ΩR + 3Σᵢ η_ΩRZ₂⁽ⁱ⁾) = 32 for η_ΩR = −1 (the text's choice for large hidden groups).
- **Text check:** Σ_hidden N_x X_x = 8.

**Model:** Table 27, with N = (4, 2, 2, 2, 2) for (a, b, c, d, e):
- a, b, c = (0,1; 1,0; 1,−1);
- d = (−1,2; 2,−1; 1,−1);
- e = (1,0; 1,0; 1,0).

**Ambiguity:** "Σ_{i≠j≠k≠i}" is read two ways, (R1) cyclic, 3 terms, and (R2) all permutations, 6 terms. The rank normalisation is read two ways too, (N1) N = rank and (N2) N = 2·rank.

**Control:**
- Both readings are computed.
- **PASS** for a reading if every stack satisfies Y = 0 and 2X + Y > 0, **and** the bulk tadpole equals 32, **or** Σ_hidden N X = 8 holds in that reading.
- The reading that passes is adopted for v6. If none passes: FAIL, and the formula reading is owed.

**Also computed:** the 3-cycle length L ∝ √(X² + XY + Y²) for a, b, c (equal means tree-level unification, Eq. 65), and the resulting α_s chain (the D2084/D2100 numbers apply for exact unification).
