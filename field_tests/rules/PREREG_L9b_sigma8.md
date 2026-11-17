# PREREG L9b — Janus-LT's own σ8 from A_s (derived normalisation + EH98 shape), validated vs CAMB
Locked 2026-11-17 before any L9b number. Normalisation [derived here, not fetched — the test is what validates it]: in matter domination
Φ = (3/5)ℛ on super-horizon scales and k²Φ = −(3/2)Ω_m H0² δ/a (Poisson, comoving gauge), so δ(k, a) = −(2/5) k² ℛ T(k) D(a)/(Ω_m H0²) with D = a deep in
matter domination; hence P_δ(k, 0) = (4/25)·k⁴/(Ω_m² H0⁴)·T²(k)·D(0)²·P_ℛ(k), P_ℛ = 2π² A_s/k³ (k/k_p)^{n_s−1}, k_p = 0.05 Mpc⁻¹.
σ8² = ∫ dk/k · k³P/(2π²) · W²(kR), R = 8 h⁻¹Mpc, top-hat W = 3(sin x − x cos x)/x³. T = EH98 no-wiggle (D1065); D(0) from the Janus-LT growth ODE
(growth.py equation) started with D = a at a = 1e-3 (radiation neglected → stated systematic).
Test: 3 cosmologies (as L9a), A_s = 2.1e-9, n_s = 0.9649, mν = 0; compare with CAMB 2.0.5 get_sigma8_0(). Claim: |σ8/σ8_CAMB − 1| ≤ 3% for all three
→ VALIDATED (own amplitude). Also report the ratio's spread across cosmologies (a constant offset would point at D's radiation-era start).
Results: field_tests/results/janus_lt_l9b_s8.txt.
