# PREREG D982: Boltzmann check of the instantaneous-decay leptogenesis yield used for SERAPIS-E at ρ (D731/D775) (written before any run)
Question: D731/D775 use Y_B = c_sph (3/4)(T_R/m_φ)·2ε (c_sph = 8/23; two N per φ → NN decay; T_R from H(T_R) = Γ_φ, g* = 106.75, as in D725). Is this accurate when solved as a Boltzmann system?
System (2311.05824 eq. 15 structure, number form; M/T ≥ 300 so equilibrium N and washout are kept but exponentially small):
 dρ_φ/dt = −3Hρ_φ − Γ_φρ_φ; dn_N/dt = −3Hn_N + 2Γ_φρ_φ/m_φ − Γ_N n_N;
 dρ_R/dt = −4Hρ_R + Γ_φρ_φ(1 − 2M/m_φ) + Γ_N M n_N  (N kinetic energy at production thermalised at once; N treated as non-relativistic after production [assumption, stated]);
 dn_{B−L}/dt = −3Hn_{B−L} + εΓ_N n_N − W_ID n_{B−L}, W_ID = (Γ_N/2)(n_N^eq/n_ℓ^eq) evaluated at the plasma T;
 H² = (ρ_φ + Mn_N + ρ_R)/(3M_P²), M_P = 2.435e18 GeV; T from ρ_R with g* = 106.75; Y_B = c_sph n_{B−L}/s at the end (s = 2π²g*T³/45).
 Start: ρ_φ only, at H = 1e4 Γ_φ; end: when ρ_φ/ρ_R < 1e-8 and n_N M/ρ_R < 1e-8; solver solve_ivp LSODA in ln a, rtol 1e-9 (φ term switched off once ρ_φ a³ < e^-690 of its start).
Inputs (D731 cases, m_φ = 2.2e13 GeV, decaying-state masses and T_R exactly as in theory/modular/lepto_rho_d731.py): every (c, M_H, state) row with M < m_φ/2; Γ_N = K·H(T = M) with K ∈ {1, 10, 100}; ε = 1e-6 (the yield is linear in ε; ratios are ε-independent).
Output: κ = Y_B(Boltzmann)/Y_B(instantaneous formula) for each row and K.
Verdict: if all κ ∈ [0.85, 1.15]: "instantaneous yields stand"; D775 node can move from estimate to computed for its yield convention.
 Otherwise: a correction note rescales the D775 yields by κ; specifically c = 0.3 at M_H = 1e12 (D775: short by ×1.15) passes only if κ ≥ 1.15 for its rows.
Selftest before the run (in the script): with Γ_N → ∞ (K = 1e6) and M/m_φ → 0 limits the code must reproduce the analytic n_φ/s scaling within 30% (sanity, not a verdict).
Script theory/modular/lepto_boltz_d982.py; output field_tests/results/lepto_boltz_d982.txt. D982 is the lock label; the result note gets the number the claim script returns.
