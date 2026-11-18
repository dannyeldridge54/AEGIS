# PREREG NA14 — node audit sweep: vac_rho, vac_i, n_sector_rho, n_sector_i, covariant/matter_parity, halo_profile, tests_lhc
Locked before computing (the HL-LHC literature fetch for tests_lhc was read before this lock; it is literature, recorded with source, no computation depends on it).
Arithmetic checks (PASS if each quoted number reproduces to its quoted digits):
1. vac_rho (D613): equation of state for V ∝ δ^n: w = (n−2)/(n+2): n = 12 → 5/7 = 0.714; octic n = 8 → 3/5 (τ = i, D730).
2. vac_rho running (D634): ratios α_s/α_s,att = 9.5/4.5 = 2.11, 8.5/3.7 = 2.29.
3. n_sector_rho (D896): 699/20000 = 3.50 %; |τ − ρ| ≈ √3 × 1.6e-4 = 2.8e-4 (1.1e-4 – 7.3e-4 for ε 6.3e-5 – 4.2e-4).
4. n_sector_i (D664/D785): Y(i) = (0.1306, 0.0754) ∝ (√3/2, ½) and s = |Y| = 0.1508; rerun theory/modular/i_mirror_d785.py unchanged and diff against field_tests/results/i_mirror_d785.txt (PASS if identical).
5. halo_profile (D1061): ρ_⊙ rescaling 0.39/0.286 = 1.364; f_max 0.24 → 0.33, 0.18 → 0.25, 0.57 → 0.78.
6. tests_lhc [literature, 1812.07831 §4.1.1 and §4.1.3]: compare D736's statement ("Run 3 / HL-LHC will close or find" the window) with the current window 0.67–1.85 TeV (D784) and the fetched HL-LHC reaches. Verdict: CONSISTENT / CORRECTED.
Results: field_tests/results/na14_sweep.txt.
