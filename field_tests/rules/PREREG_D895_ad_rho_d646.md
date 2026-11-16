# PREREG D895 (R2.2 major #1): LH_u Affleck–Dine at ρ recomputed with the model's own no-thermal yield (D646/D646a/D653)
Locked before computing, 2026-11-16.
Reason: referee R2 item 1 (REFEREE_v3.2_R2.md, D894). D880 used the FHY thermal scaling (hep-ph/0102187) extrapolated to T₂ = 1e5–1e6 GeV with m_{3/2} = 2.5e5–7e5 GeV. D653 showed thermal effects are negligible in exactly this regime (H_osc ~ m_soft ~ 2.5e5–1.1e6 GeV, φ/T ≳ 1e6), so the no-thermal yield of D646 applies.
Formula (D646 + D646a factor 2): n_B/s = (8/23)·T₂·M_eff·Q/(4M_P²), M_eff = 2v_u²/m_ν₁ ⇒ m_ν₁ = 2(8/23)T₂v_u²Q/(4M_P²·8.7e-11). Inputs: v_u = 174 GeV (as in D646's script), M_P = 2.435e18 GeV, Q from results/affleck_dine_d646.txt (median 0.020, max 0.087). T₂ ∈ {1e5, 3e5, 1e6} GeV.
Check K: also evaluate the FHY-extrapolated yield at D880's smallest m_ν₁ (4.4e-9 eV, T₂ = 1e5) against the no-thermal ceiling δ·T₂·M/(4M_P²) with δ = 1; if FHY exceeds the ceiling, D880 overestimated.
Output: field_tests/results/ad_rho_d895.txt: the required m_ν₁ window at ρ.
Decision rule: if the window differs from D880's 4e-9–7e-8 eV by more than a factor 3, write correction note D880a superseding D880's window, and flag D883 (lift ε target) and D891–D892 (Weinberg bound) for recomputation.
Prediction (pre-stated): window ≈ 2e-11–9e-10 eV, i.e. D880 corrected downward by ~100.
