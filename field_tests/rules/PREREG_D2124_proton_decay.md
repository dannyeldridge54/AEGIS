# PREREG D2124: checklist item 14, proton decay (ping-pong: referee R14-1…R14-3 folded in). Locked before computing.

**Fields** (Table 28):
- F_L = (4,2,1): F1 = ab (1 copy, U(1) charges Q = (1,−1,0,0,0)) and F2, F3 = ab′ (2 copies, Q = (1,1,0,0,0)).
- F̄_R = (4̄,1,2): R1 = ac (1 copy, Q = (−1,0,1,0,0)) and R2, R3 = ac′ (2 copies, Q = (−1,0,−1,0,0)).
- Z4 generator k = (0,1,1,1,1) (D2120b).

**Enumeration rule:** a superpotential F⁴ term is ε_SU(4) × (a totally antisymmetric tensor in the SU(2) ⊗ flavour index). By Schur–Weyl, the SU(2) singlet needs flavour irrep S_(2,2). So the allowed flavour contents are the weights of S_(2,2)(C³), computed in code.

| Test | What is computed |
|---|---|
| T1 | dim-5 F_L⁴ (contains QQQL) and F̄_R⁴ (contains UDDE ⊃ UUDE): every allowed flavour content, with its Z4 charge, its ΔQ vector, and whether it is Z4-allowed |
| T2 | dim-6 Kähler operators F_L F_L F̄_R† F̄_R† (contain QQu^c†e^c†): every flavour content, with its Z4 charge and ΔQ |
| T3 | dim-4 RPV: show that every LLE/LQD/UDD-type PS operator violates B−L (SU(4)-forbidden), and that the Z2 = 2k gives matter parity (charge 2 on F and F̄, 0 on the Higgs) |
| T4 (ESTIMATE) | required coefficient suppression for τ ≥ 1e34 yr: (i) dim-6, Γ ≈ α_X² m_p⁵ / M_s⁴ with M_s = 8e12 GeV and α_X = 1/24; (ii) dim-5 with gaugino dressing, Γ ≈ (α₃/4π)² m_p⁵ / (M_s² m_SUSY²) with m_SUSY = 1 TeV. Report the required e^{−S} for each |

**Verdict:**
- PASS if every Z4-allowed baryon-violating structure that involves the light generations is absent.
- CONDITIONAL if some are allowed but would need instanton suppression e^{−S} below the T4 requirement. State S_min.
- Generation identification (ESTIMATE): F1/R1 carry the perturbative Yukawa, so they are taken as the 3rd (heaviest) generation, and F2,3/R2,3 as the light generations.
