# PREREG R2e-a — MS-bar α̂₂(2M) in the annihilation matrices, x_end = 1e8, constant g_* — locked 2026-11-17, before any code or run
Source: arXiv:2009.00640, Secs. 3.3 and 4.1, Eqs. 3.27–3.28.
- α̂₂(m_Z) = 0.00780372/0.232486.
- One-loop SM running: 1/α̂₂(μ) = 1/α̂₂(m_Z) + (19/6)/(2π)·ln(μ/m_Z), at μ = 2M. The b₂ = 19/6 coefficient is a textbook value, labelled as such. No wino threshold in the running.
Changes vs R2d:
- σ_Born → σ_Born·(α̂₂(2M)/α₂^os)², with α₂^os = sommerfeld_nlo.ALPHA2. The Sommerfeld potentials stay on-shell, as in Beneke.
- x_end = 1e8. R_eff(x) is held at its x = 3e4 value beyond 3e4 (labelled assumption; the effect is reported by also running with x_end = 3e4).
- Everything else as R2d: constant g_* = 106.75, R_eff from r2c_b_alls with n = 40, the same 25 x points.
- Mass grid {2.2, 2.4, 2.6, 2.8, 3.0, 3.2} TeV. The Born root is found by brentq on [1500, 4000] GeV.
Scored:
- B1: Born M_th within 3% of Beneke's 2.207 TeV (the residual is g_*).
- L1 is reported, not scored (g_* not yet sourced): LO-Sommerfeld M_th vs Beneke's 2.886 TeV.
Regression: S3 rerun with the old inputs (on-shell α₂, x_end = 3e4, R ≡ 1) must give 2.564 ± 0.002 TeV.
