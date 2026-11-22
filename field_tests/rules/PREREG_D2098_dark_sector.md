# PREREG D2098: is v4's dark SU(12) consistent, and does it avoid the dark-glueball problem? Locked before computing.

**Formulas:**
- **One-loop running:** α⁻¹(μ) = α⁻¹(M_s) + (b/2π) ln(M_s/μ). For pure SU(N) SYM, b = −3N (NSVZ one-loop), here −36.
- **Confinement:** Λ = M_s exp(−2π α⁻¹(M_s)/|b|) for b < 0.
- **Dark-glueball window** (1609.02151, quoted): a confining hidden sector with **3 eV ≲ Λ ≲ 2.4e8 GeV** overproduces DM or breaks BBN, unless reheating is strongly asymmetric (ξ ≳ 2.3 Λ/eV). Λ ≥ 2.4e8 GeV is rescued by decays to moduli.

**v4 inputs:**
- σ_d = 40.3 (D1812).
- Two readings of α_D⁻¹(M_s): **(i)** σ_d, and **(ii)** σ_d + 7.79 (if the 9S piece also enters f_dark).
- M_s ∈ {1e16, 2e16} GeV.

**Tests:**
- **T1:** Λ_d for pure SU(12) SYM, in each reading.
- **T2:** the b needed for α_D(12.8 GeV) = 0.021 (D1812) from the same α_D⁻¹(M_s).
  - **CONFLICT** if T1 gives Λ_d > 12.8 GeV while T2 needs b > 0: one SU(12) cannot both condense (to hold σ_d) and stay perturbative at 12.8 GeV.
- **T3:** the glueball window for Λ_d, and for the KL racetrack condensates (7, 8) and (14, 15). Same formula, σ = 20.15, b = −3N.

**Verdict:** report CONFLICT / CONSISTENT for T2, and SAFE / PROBLEM for each sector in T3.
