# PREREG R1 — Hyperion wino relic-density module, Born level (new module; Danny "Run them") — locked 2026-11-17
Target (quoted, arXiv:2009.00640): Ωh² = 0.1205 is reached at m = 2.207 TeV with the Born cross section (no Sommerfeld). It is 2.886 TeV with the LO potential and 2.842 TeV with NLO (used later, in R2/R3).
Annihilation (sourced, hep-ph/0610249 Eqs. 2–8, fetched in D1110): σv = c Σ AΓA*, with c = 2 for identical particles and 1 otherwise, and tree A = 1.
- Γ: (−+, 00) S=0 block (πα₂²/2m²)[[3,√2],[√2,2]]; χ⁻χ⁺ S=1 25πα₂²/(24m²); χ⁰χ⁻ S=0 ½πα₂²/m² and S=1 (25/24)πα₂²/m²; χ⁻χ⁻ S=0 πα₂²/(2m²).
- Spin average: (1/4)σ_S0 + (3/4)σ_S1, with S=1 absent for identical pairs.
- σ_eff = Σ_ij g_i g_j σ_ij / g_eff², with g = 2 for each of χ⁰, χ⁺, χ⁻ (g_eff = 6) and δm neglected (δm/T_f ~ 2e-3).
Boltzmann, standard (Kolb–Turner form, written from memory and labelled):
- dY/dx = −(s⟨σv⟩/(Hx))(Y² − Y_eq²), with s/H = √(π/45) M_Pl √g* m/x².
- Y_eq = (45/(4π⁴)) (g_eff/g*s) x^{3/2} e^{−x} √(π/2).
- Ωh² = m Y_∞ s₀ h²/ρ_c,0, with s₀ = 2891.2 cm⁻³ and ρ_c/h² = 1.0537e-5 GeV cm⁻³ (labelled constants).
- M_Pl = 1.2209e19 GeV. g* = g*s = 106.75 (assumption: SM above ~100 GeV; T_f ≈ 90 GeV is near the top/W thresholds).
α₂: the on-shell α/s_W² as in A1c (0.03479). Labelled: the scheme choice is a ~±5% effect on α₂², so ~±2.5% on the mass.
Test T1: the m solving Ωh² = 0.1205 lies within ±6% of 2.207 TeV. Reported: x_f, σ_eff in units of πα₂²/m², and m with α₂ MS-bar(m_Z) 0.03357.
R1 VALIDATED iff T1 passes. Fixes only via DEVIATIONS.
Code: tools/janus_astro/relic.py; check theory/janus_astro/r1_check.py (written after this lock).
