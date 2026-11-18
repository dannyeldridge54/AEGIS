# PREREG A1 — accuracy queue: SERAPIS reheating with the MSSM g* = 228.75 (flag D1258)
Locked before running. SERAPIS is supersymmetric with its whole spectrum below T_R ~ 1e9 GeV ⇒ g* = 228.75 at reheating. Two effects (D1258): T_R(Γ) ∝ g*^(−1/4) ⇒ every audited T_R (computed with 106.75) × (106.75/228.75)^(1/4) = 0.82649; and N*'s explicit g-terms cancel at fixed T_R (checked in W2).
Change: pipeline.predict_fast gains g (default 106.75 unchanged for other models); SERAPIS runs use g = 228.75 and the converted T_R. No other change.
Compute: PW2 point (C 1.25e-6, T_R 8.94e8 → 7.389e8) and the audited box edges (C 1.0, 1.15, 1.3e-6 × T_R 6.6e8, 2.0e10 → 5.455e8, 1.6530e10).
Pre-stated expectation: every n_s lower by (6.3 ± 0.5)e-5, N* lower by 0.063 ± 0.003, r higher by (0.16 ± 0.03) %. PASS if all points inside.
Then the audited values (box, point, nstar_e) are updated with MSSM g* in the derivation doc and the map (new D-note; frozen predictions unchanged).
Results: field_tests/results/a1_mssm_gstar.txt.
