# PREREG D2080: Seed v2. Seeded on the published SUSY three-family model (Cvetič–Shiu–Papadimitriou/Uranga, hep-th/0107143 Table I, T⁶/(Z₂×Z₂), tilted 3rd torus, m̃ = m − n/2), then spun outward. Locked before running.

**Formulas** (quoted from the paper in this session):
- **Tadpoles:** Σ N n¹n²n³ = 16, Σ N n¹m²m̃³ = −8, Σ N m¹n²m̃³ = −8, Σ N m¹m²n³ = −16.
- **SUSY:** θ₁ + θ₂ + θ₃ = 0 for every stack, with tan θᵢ = χᵢ mᵢ/nᵢ (m̃ on torus 3). The common χᵢ > 0 are solved numerically.
- **Families:** I_ab = Πᵢ(n_aᵢm_bᵢ − m_aᵢn_bᵢ) and I_ab′ with m_b → −m_b. Left-quark count = \|I(C₁, B₁)\| + \|I(C₁, B₁′)\|.

**Step 1, calibration (positive control):** the seed must give all four tadpoles exact, a SUSY solution for χ, and a left-quark count of 3. **If it fails, stop.**

**Step 2, rings:**
- **Ring k** changes k wrapping integers of the seed by ±1 (k = 1, 2; all choices, every stack and entry; the m̃ half-integer offsets are kept).
- **Hard filters:** all four tadpoles exact, a SUSY solution exists (residual < 1e-8), and a left-quark count of 3.
- **Report:** the survivors per ring and how many differ from the seed by more than a stack relabelling.

**Scope (stated):** this is a consistency-neighbourhood scan. Gauge-coupling predictions (α_s) are **deferred**, because the hypercharge normalisation for the Higgsed USp(8) → U(1)² is not yet fixed. No physics verdict is drawn on α_s.
