# PREREG D731: non-thermal leptogenesis for SERAPIS-E at ρ (2 ⊕ 1, W2, b = 0; D725)
Locked 2026-11-16 before computing. Script: theory/modular/lepto_rho_d731.py. Output: field_tests/results/lepto_rho_d731.txt.
## Inputs (fixed now)
- Open cases of D725 with their T_R and the masses produced: c = 0.3 (M_H = 1e12, 1e13; 5e13), c = 1 (1e12, 1e13), c = 3 (1e12). m = 2.2e13 GeV.
- Y_B = (8/23)(3/4)(T_R/m)·n_N·ε, with n_N = 2 N per decay, ε the CP asymmetry per N decay.
- ε: the exactly degenerate light pair has no mutual resonant asymmetry (x = 0 → ε = 0, D597 regulator). The asymmetry comes from the non-degenerate partner in the loop. Upper estimate = Davidson–Ibarra bound for the decaying state, ε_DI = 3 M m_ν/(16π v²) (m_ν = 0.05 eV, v = 174 GeV), times sin δ = 1. Self-energy enhancement for M_L/M_H close to 1 is ignored (conservative).
- Washout: thermal, suppressed by exp(−M_L/T_R); report M_L/T_R (needs ≳ 10).
## Decision rule (written before running)
- PASS (maximal phase) if Y_B(ε_DI) ≥ 8.75e-11 with M_L/T_R ≥ 10; report the required sin δ = Y_obs/Y_B(ε_DI).
- FAIL if even ε_DI falls short.
- Fixes only via D731_DEVIATIONS.md.
