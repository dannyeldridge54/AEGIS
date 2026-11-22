# PREREG D2112: full derivation checklist for the unique Z₂×Z₆′ global Pati–Salam model (Table 27 of 1209.3010, shown unique in D2111). One staged run, locked before computing.

**Sources:** 1209.3010 (arXiv LaTeX, downloaded 2026-11-22 with OK). Spectrum inputs come from paper Tables 28 (chiral) and 29 (non-chiral). The chiral part was reproduced by our engine in D2110; the non-chiral part is literature input. PDG 2024 values at M_Z: α_em⁻¹ = 127.951, sin²θ_W = 0.23122, α_s = 0.1180 ± 0.0009. Quark masses at M_Z are ESTIMATES: m_t ≈ 171, m_c ≈ 0.62, m_u ≈ 0.00127 GeV.

| # | Item | Method | Pass / record |
|---|---|---|---|
| K1 | Global consistency | D2110/D2111 engine | Already PASS (cite) |
| K2 | Chiral spectrum | D2110 | Already PASS (cite) |
| K3 | Sym/Anti exotics | χ^Sym = χ^Anti = ½ Π_x∘Π_x′ (paper eq. CSeqCA), for x = a, b, c, d, e | Report. Visible a, b, c must give 0. Consistency check of D2111 uniqueness against the paper's "27 three-stack configurations, identical chiral spectrum" |
| K4 | GS U(1) masses | Compute N_x c_x^{(k),α} from our exceptional numbers with the paper's c definitions; compare with the paper's 15×5 matrix (Eq. GGS-matrix) | **PASS if exact** (an overall sign is allowed). Report the match up to row permutation within a sector, and the rank (paper: 5, so all U(1)s massive) |
| K5 | β coefficients | Paper Eq. beta-coeffs with the Table 28+29 multiplet counts (h.c. included) for SU(4)_a, SU(2)_b, c, d, e | Report the b's. Hidden confinement only if b < 0 |
| K6 | One-loop thresholds | Evaluate the paper's Eq. one-loops with exact ϑ₁/η (mpmath, ϑ₁ normalisation checked against the stated asymptotics), both the **literal** text and **corrected** where the literal coefficient contradicts the paper's own asymptotic (the 1/2π vs 1/2π² prefactor in the b, c line). Solve Re f_a = Re f_b at v₁ = v₂ | Compare with the paper's printed condition v₁ = v₂ = 4v₃ + 168 ln2/π. A disagreement is reported as a possible typo in the source, not as our claim |
| K7 | String scale | α_tree⁻¹ = C·M_Pl/M_s, with C from the paper's Eqs. tree-gauge and mass-ratios (paper quotes ≈ 4e-4). Find the M_s needed for α_X⁻¹ = the one-loop MSSM unified value, using reduced and non-reduced M_Pl | Report the ratio to M_GUT(MSSM, one-loop) |
| K8 | α_s at one loop | PS broken at M_s. **S1:** only the MSSM is light. **S2:** every PS-vector-like state from Tables 28/29 is light at 1 TeV, with its SM decomposition stated in the code | PASS for a scenario if \|α_s − 0.1180\| < 0.01 (one-loop tolerance). Non-perturbative counts as FAIL |
| K9 | Yukawas | 1 perturbative generation (paper). Instanton suppression needed: S = ln(m_t/m_c), ln(m_t/m_u) | ESTIMATE |
| K10 | PS breaking | Search Tables 28/29 for a (4,1,2) or (4̄,1,2̄) Higgs | Absent means OPEN (needs brane recombination) |
| K11 | Hidden sector | From K4 and K5: massless dark photon? Confinement scale? | Report |

**Verdict:** a per-item table. No item may be rerun to change a verdict. Fixes go in DEVIATIONS only.
