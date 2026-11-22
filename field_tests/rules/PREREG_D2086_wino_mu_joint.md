# PREREG D2086: joint feasibility of α_s, wino and gluino when the higgsino mass μ is freed (v4 spectrum, pure-gravity-mediation form). Locked before computing.

**Formulas** (Ibe–Moroi–Yanagida et al., PGM, 1207.5453 Eqs. 6, 7, 9, quoted; log taken as log₁₀, an assumption with ~1% effect):
- **Gluino:** m_g̃ = 2.5e-2 (1 − 0.13 δ₃₂ − 0.04 δ_S) m₃/₂
- **Wino:** m_W̃ = 3.0e-3 (1 − 0.04 δ₃₂′ + 0.02 δ_S)(m₃/₂ + L)
  - δ₃₂ = log(m₃/₂ / 100 TeV)
  - δ₃₂′ = log((m₃/₂ + L) / 100 TeV)
  - δ_S = log(M_SUSY / 100 TeV), with M_SUSY = m₃/₂
- **Higgsino threshold:** L = μ sin2β · m_A²/(|μ|² − m_A²) · ln(|μ|²/m_A²). With **m_A = |μ|** (the x → 1 limit, stated), L = μ sin2β.
- **α_s:** CPW Eq. 16 T_SUSY with m_H̃ = m_H = |μ| and m_l̃ = m_q̃, then two-loop exact unification (tools/seed/twoloop.py, D2084). α_s(T) is tabulated on a log grid and interpolated; the table is checked against direct calls at 3 points.

**Scan:**
- m₃/₂ ∈ [30, 3000] TeV (log grid, 121 points);
- μ = ±[10, 3000] TeV (log grid, 121 points per sign);
- tan β ∈ {1.5, 2, 3, 4} (v4 band 1–4).

**Goalposts (bloom_data, unchanged):**
- wino ∈ [0.670, 0.700] TeV;
- gluino ≥ 2.3 TeV;
- |α_s − 0.1180| ≤ 2 × 0.0009.

**Report:**
- whether any point passes all three, and where;
- in particular c = μ/m₃/₂ at feasible points, against the PGM expectation μ = O(m₃/₂), |c| ∈ [0.3, 3];
- whether v4's present point (μ at the scalar scale, L = 0 as used so far) passes.

**Labelled HYBRID:** exact-unification boundary (D2083) with the v4 spectrum.
