# PREREG NA9 — gravitino → wino (D809) with the audited T_R windows (NA6, NA8)
Locked before running. Copy of theory/modular/gravitino_ps_d809.py with ONLY the T_R lists changed:
(A) τ = i: T_R ∈ {1.3e6, 5.0e6} (NA8; was 1e6, 3e6). (B/C) SERAPIS-E early T_R ∈ {6.6e8, 2.0e10} (NA6; was 3e8, 3e9), same T₂ list.
Locked rule (D809, unchanged): Ω_nth < 0.01 everywhere → PASS; also report the max Ω_nth against the node label "≤ 3e-4".
Plus arithmetic: C_lepto "0.87e-10 × D" vs Y_obs = 8.70e-11 (NA4) — PASS if within 1 %.
Results: field_tests/results/na9_gravitino_wino.txt.
