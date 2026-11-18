# PREREG W2 — measured waves on the reheating chain at the audited SERAPIS-E point (PW2: C 1.25e-6, T_R 8.94e8 GeV)
Locked before running. Engine: pipeline.predict_fast (U2, D1257). Each wave = + and exact inverse; report Δn_s, Δr/r, Δα_s, strength |Δn_s|/0.0030 (σ_SPA), asymmetry.
 w_m: inflaton mass m_φ × 1.1 / ÷ 1.1 at fixed couplings → T_R ∝ m_φ^{3/2} (NA8 scaling) → T_R × 1.1^{±1.5}.
 w_g: relativistic degrees of freedom: SM g* = 106.75 vs MSSM g* = 228.75 (SERAPIS is supersymmetric; winos) — T_R ∝ g*^{-1/4} at fixed Γ → T_R × (106.75/228.75)^{±1/4}; the N* formula's explicit g-terms cancel at fixed T_R for w = 0 (ρ_th ∝ g T⁴ vs −(1/12) ln g), stated here and checked by running nstar.Nstar with g = 228.75 at the MSSM T_R.
 w_n: Kähler-weight wave (the NA3 correction as a wave): couplings × √3 / ÷ √3 → T_R × 3^{±1/2}.
Pre-stated expectation: ΔN* = (1/3) ln(T_R ratio): w_m ±0.048, w_g ∓0.064, w_n ±0.183 e-folds; Δn_s ≈ 1.0e-3 per e-fold (W1) ⇒ |Δn_s| ≈ 5e-5, 6e-5, 1.8e-4.
Verdict: (1) expectation PASS if every measured |Δn_s| is within 30 % of the pre-stated value; (2) if |Δn_s(w_g)| ≥ 5e-5, flag the SM-g* choice in nstar.py as a correction candidate for an MSSM model (no silent change).
Results: field_tests/results/w2_reheat_chain.txt.
