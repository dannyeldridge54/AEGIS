# PREREG D2091: the KL racetrack on T_vis as the mirage fix. Is the D2089 branch still CONSISTENT once the residual tree gaugino mass is added? Locked before computing.

**Formulas** (Kallosh–Linde-type strong stabilisation, from 1111.1465; the derivation is in this lock):
- D_ρW = 6√(2σ₀)(m₃/₂/m_σ)m₃/₂
- m_{1/2} = (√(2σ)/6)·D_ρW·∂_ρ ln Re f, with f = ρ, so ∂_ρ ln Re f = 1/(2σ)
- ⇒ **M_tree = m₃/₂²/m_σ** (universal at M_s)

**Inputs:**
- m_σ = 1.6e8 GeV (D2037 B0b at σ ≈ 20). A factor-2 band [0.8e8, 3.2e8] is carried as uncertainty.
- Both signs of M_tree relative to the AMSB contribution.

**Low-scale map (estimate, stated):** M_a(μ) = M_tree·α_a(μ)/α_G, with α_G⁻¹ = 25 (D2084), α₂⁻¹(0.7 TeV) = 30.3, α₃⁻¹(3 TeV) = 11.0. So M₂ += 0.83·M_tree and M₃ += 2.27·M_tree.

**Test:** rerun the D2089 four-goalpost scan (GM μ, tan β continuous, m_h band) with the wino and gluino shifted as above. m₃/₂ ∈ [100, 200] TeV.

**Verdict:**
- **CONSISTENT** if ≥ 1 point passes at every (m_σ, sign) combination;
- **PARTIAL** if only some combinations pass;
- **FAIL** if none do.

**Report also the costs (D2072):** racetrack naturalness B/A = 0.057 at N′ = 7 (natural window 0.1–10), and that the KKLT W₀ relation is replaced by the racetrack W₀ (the W₀ gap changes form). The inflation-side KL gap (H_inf ≫ m_σ) remains, as stated.
