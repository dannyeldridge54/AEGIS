# PREREG NA12 — nstar_i / band_i with the audited τ = i reheating (NA8: T_R ∝ m^{3/2}, D730 masses)
Locked before running. Code: D815's exact-MS obs() (theory/modular/chronos_ms_d815.py lines 1–10, D632 MS code unchanged), new driver only.
N*(ε) = 50.31 + ΔN*(ε), the D730/D815 physical (stiff) history value plus NA8's shift ΔN* = ½ ln(m(ε)/1.9e11), with m(ε) linear between D730's (1.3e-4, 2.28e11) and (1.6e-4, 2.65e11) [shift: estimate; spectra: exact MS].
Grid ε = 1.30, 1.35, 1.40, 1.45, 1.50e-4. Report n_s, r, α_s and in-band (frozen band_i: n_s 0.970–0.975, r 4.8–5.7e-4).
Expectation (pre-stated): ΔN* ≈ +0.11–0.14 raises n_s by ~1e-4, so the D815 window ε 1.40–1.45e-4 shrinks: ε = 1.45e-4 leaves the band (n_s > 0.975), ε = 1.40e-4 stays.
Verdict: window_new = in-band ε values. CONSISTENT if non-empty (τ = i keeps a window); report it. Post-hoc, band_i frozen.
Also arithmetic check of D861's benchmark: Im S = 0.1125/g_s at g_s = 0.232 → 0.485; C = 15·4/(64π⁶·781) → 1.25e-6.
Results: field_tests/results/na12_band_i_audited.txt.
