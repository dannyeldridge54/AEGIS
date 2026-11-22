# PREREG D2099 (loop 2, tick 1, L1): does the radiative splitting from M_s down to M_S turn BIM's boundary tan β = 1 into tan β ≈ 1.9? Locked before computing.

**Formulas (Martin hep-ph/9709356, one loop, top-dominated; gauginos dropped since M_a ≪ m₃/₂; S = 0 and stays 0 for universal boundaries):**
- 16π² dm²_Hu/dt = 3X_t
- 16π² dm²_Hd/dt = 0 (no b/τ Yukawas at tan β ~ 2)
- 16π² dm²_Q3/dt = X_t
- 16π² dm²_u3/dt = 2X_t
- X_t = 2y_t²(m²_Hu + m²_Q3 + m²_u3) + 2a_t²
- 16π² da_t/dt = a_t(18y_t² − …) + gaugino terms. Here a_t(M_s) = 0 and the gaugino sources are dropped, so a_t stays ≈ 0.
- 16π² dμ/dt = μ(3y_t² − 3g² − (3/5)g₁²); B = Bμ/μ is constant (a_t, M_a ≈ 0)
- 16π² dy_t/dt = y_t(6y_t² − (16/3)g₃² − 3g² − (13/15)g₁²); gauge couplings at one loop, MSSM b = (33/5, 1, −3)

**Boundary at M_s = 1e16 GeV** (BIM hep-ph/9707209 Eqs. 69–70 at Θ → 0, universal untwisted sfermions):
- all scalar masses m² = m₃/₂²;
- |μ| = m₃/₂, Bμ = 2m₃/₂²;
- so Eq. 72 holds and tan β = 1 there.

**At M_S = m₃/₂ = 128.5 TeV:**
- tree minimisation, sin2β = 2Bμ/(m²_Hu + m²_Hd + 2|μ|²);
- y_t(M_S) = y_t^SM(M_S)/sin β, with y_t^SM from the D2088 two-loop-corrected run;
- tan β is iterated to a fixed point.

**Verdict:**
- **CONSISTENT** if the fixed-point tan β lies within the m_h-allowed band [1.81, 2.02] (D2088);
- **TENSION** if it lies outside but tan β > 1.3;
- **FAIL** if tan β stays ≈ 1 (< 1.3).
