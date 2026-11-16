# PREREG D900 (R3.2 major #1): τ = i LH_u AD window at the corrected reheating temperature
Locked before computing, 2026-11-16.
Reason: referee R3 item 1 (REFEREE_v3.2_R3.md, D899). The draft quotes the τ = i window at T_R = 1e3–1e5 GeV (D646, constant-W₀ era); the corrected τ = i reheating is T_R ≈ (0.8–3)e6 GeV (D727, D815).
Yield (D646 + D646a, unchanged): m_ν₁ = 2(8/23)·T_R·v_u²·Q/(4M_P²·8.7e-11); v_u = 174 GeV, M_P = 2.435e18 GeV, Q = 0.020 (median), 0.087 (max) from results/affleck_dine_d646.txt. T_R ∈ {0.8e6, 1e6, 3e6} GeV.
Thermal check (method of D653, an estimate): at onset H = m_soft ∈ {2.5e5, 1.1e6} GeV, plasma T = (T_R²·H·M_P)^{1/4}; φ_osc = √(m_soft·2M), M = v_u²/m_ν₁ (at the computed m_ν₁); require φ/T ≥ 1e3 (heavy coupled fields) and the two-loop thermal log term α²T⁴ (α = 0.1) ≤ 1e-3 of m_soft²φ².
Decision rule: if the check passes, the window is the result and the draft/sheet are updated to it; if it fails at any point, report which and flag the window as thermal-uncertain there.
Prediction (pre-stated): m_ν₁ ≈ 1.6e-10–2.7e-9 eV; thermal effects negligible (φ/T ≳ 1e5).
