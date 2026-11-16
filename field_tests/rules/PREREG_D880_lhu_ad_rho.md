# PREREG D880 (B.5): LH_u Affleck–Dine leptogenesis at ρ with the late reheating T₂
Locked before computing, 2026-11-16.
Formula [literature, hep-ph/0102187 eqs. 25–26 and text]: n_B/s ≃ 1e-11·δ_eff·(m_ν₁/1e-8 eV)^{−3/2}·(m_{3/2}|a_m|/1 TeV) for 1e8 ≲ T_R ≲ 1e12 GeV; below 1e8 GeV the dependence is mild, n_B/s ∝ T_R^{1/3}. Implemented as the eq. 26 value times (T_R/1e8 GeV)^{1/3} for T_R < 1e8 GeV.
At ρ: T_R → T₂ (the late reheating by the Z₃-charged pair, which dominates while the condensate oscillates), T₂ ∈ {1e5, 3e5, 1e6} GeV (band-safe, D781); m_{3/2} ∈ {2.5e5, 7e5} GeV (covariant completion, paper Sec. on superpartners); |a_m| = 1; δ_eff ∈ {0.1, 1}.
Output: the m_ν₁ that gives n_B/s = 8.7e-11 for each case.
Verdict: "fits" if the required m_ν₁ lies in [1e-12, 1e-6] eV (i.e. an essentially massless lightest neutrino, compatible with the frozen Σm_ν NO floor, whose Σ changes by < 1e-6 eV).
Prediction (pre-stated): required m_ν₁ ≈ 1e-8–1e-7 eV (larger m_{3/2} than the paper's 1 TeV raises it), still "essentially massless".
