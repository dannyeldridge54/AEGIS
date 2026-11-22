# PREREG D2084: two-loop scoring of the D2083 unified PS model's α_s hit. Locked before computing.

**Formulas (textbook; Martin–Vaughn and Machacek–Vaughn; GUT-normalised α₁ = (5/3)α_Y):**
dα_i⁻¹/dt = −b_i/(2π) − Σ_j b_ij α_j/(8π²), with t = ln μ.

| | b_i | b_ij |
|---|---|---|
| **SM** (M_Z → M_SUSY) | (41/10, −19/6, −7) | [[199/50, 27/10, 44/5], [9/10, 35/6, 12], [11/10, 9/2, −26]] |
| **MSSM** (M_SUSY → M_s) | (33/5, 1, −3) | [[199/25, 27/5, 88/5], [9/5, 25, 24], [11/5, 9, 14]] |

Yukawa two-loop terms are neglected (stated; their known effect is small and lowers α_s by O(0.001)).

**Inputs at M_Z (MS-bar):** α_em⁻¹ = 127.95 and sin²θ_W = 0.23122, so α₂⁻¹ = 29.585 and α_Y⁻¹ = 98.37.

**Model:** the D2083 unified model has g_a = g_b = g_c at M_s, so α₁ = α₂ = α₃ at M_s (PS: α_Y⁻¹ = (5/3)α⁻¹).

**Method:** shoot on α₃(M_Z): integrate up, set M_s where α₁ = α₂, and require α₃(M_s) = α₁(M_s).

**Threshold band:** a single M_SUSY ∈ {0.5, 1, 3, 10} TeV. 3 TeV is closest to v4's spectrum (wino 0.69, gluino 4.9 TeV). Every value is reported.

**Control (must pass):** one-loop only with M_SUSY = M_Z gives α_s = 0.1167 ± 0.0005 (D2083).

**Score:** the pull of the two-loop α_s against 0.1180 ± 0.0009, at each M_SUSY. The hit stands as a hit only if |pull| ≤ 2 at M_SUSY = 3 TeV.
