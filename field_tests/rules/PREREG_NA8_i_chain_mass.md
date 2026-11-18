# PREREG NA8 — τ = i chain with D730's computed inflaton mass
Locked before running. D727 (pseudo_i), D728 (lepto_i), D738 (2⊕1 at i) hard-code m_φ = 1.9e11 GeV; D730 computed m = 2.28e11 (ε 1.3e-4) and 2.65e11 (ε 1.6e-4).
Run: copies in field_tests/scripts/na8/ with ONLY m changed (each value), outputs saved. All three scripts take M = x·m, so expected T_R ∝ m^{3/2} (×1.31, ×1.64) — check (PASS if within 1 %).
Report: (i) T_R windows (g* 106.75) and ΔN* = (1/3) ln(T_R ratio) (matter-dominated decay segment, D730 history: octic → matter → radiation; decay during the octic phase negligible);
(ii) D728's passing ΔM/M range and D738's PASS/fail rows vs the originals; lepto_i verdict CHANGES if any original PASS row fails or vice versa.
Post-hoc; frozen band_i unchanged. Results: field_tests/results/na8_i_chain_mass.txt.
