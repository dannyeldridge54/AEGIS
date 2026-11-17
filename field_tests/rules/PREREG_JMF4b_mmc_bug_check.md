# PREREG JMF4b — is JMF4's failure explained by MultiModeCode's own derivative code?
Locked 2026-11-17 after JMF4 (NOT VALIDATED: N1 |Δn_s| 2.4e-4, Δr/r 3.8%; N2 |Δn_s| 1.2e-3, Δr/r 8.9%) and BEFORE any JMF4b number.
Reading MMC's modpk_potential.f90 after the failure (source quoted in the D-note) shows its V, dV and d²V disagree for these cases:
 case 12: V has 2εφ₁φ₂ (sum over i≠j) but dV_i = m_i²φ_i + εφ_j and V_12 = ε — derivatives of εφ₁φ₂, half the coupling in V.
 case 11: dV_L (lightest) drops (1/12)φ_L Σ_{i≠L} λ_iφ_i²; d²V is asymmetric (V_iL = (1/6)λ_iφ_Lφ_i, V_Li = 0) and V_LL drops (1/12)Σ_{i≠L}λ_iφ_i².
 (case 8 hybrid also: V_11 has 2φ₁φ₂²/ν⁴ where 2φ₂²/ν⁴ is right — noted, not tested here.)
Test: rerun JMF4's two models with Janus-MF given MMC's exact V, dV and d²V as coded (bugs included, asymmetric matrix passed as is), same
φ_init, pivot and MMC numbers (MMC re-run identically). JMF4's verdict is NOT changed by this test whatever it gives.
Claims: E1 |n_s^J(MMC-coded) − n_s^MMC| ≤ 2e-4 and |r/r_MMC − 1| ≤ 2e-3 for both models → "JMF4 FAILURE EXPLAINED BY MMC's DERIVATIVE CODE"
(the reference is unusable for non-separable potentials; Janus-MF non-separable stays UNVALIDATED until an independent check).
Else → "NOT EXPLAINED" (a Janus-MF non-separable problem stays open). Results: field_tests/results/janus_jmf4b.txt (+ stamp).
