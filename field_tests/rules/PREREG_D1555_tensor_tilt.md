# PREREG D1555 — Janus L2: tensor tilt n_t at second order and the consistency deviation n_t + r/8, both vacua

Locked before any number is computed.

Inputs (read only): field_tests/results/D1480_pivot.json, k = 0.05 Mpc⁻¹ block (exact MS n_s, r) for rho_A1 (SERAPIS-E) and tau_i_NA12.
Method (script field_tests/scripts/d1555/tensor_tilt.py):
1. [literature] Second-order Hubble-flow results (Stewart–Lyth / Schwarz–Terrero-Escalante; C = γ_E + ln 2 − 2):
   n_s − 1 = −2ε1 − ε2 − 2ε1² − (2C+3)ε1ε2 − Cε2ε3;  r = 16ε1[1 + Cε2];  n_t = −2ε1 − 2ε1² − 2(C+1)ε1ε2.
2. Observable-only form (eliminates ε): n_t = −(r/8)(2 − r/8 − n_s), so Δ ≡ n_t + r/8 = (r/8)(n_s − 1 + r/8).
3. Cross-check: solve for ε1, ε2 from (n_s, r) with ε3 term dropped (it enters n_t only at third order) and evaluate n_t from step 1; |difference| from step 2 must be ≤ 1e-7, else report as a FAIL, not tuned.
Outputs: field_tests/results/D1555_tensor_tilt.json: n_t, Δ, Δ/n_t for both vacua; ρ − τ=i difference.
Expectation (stated, not tuned): Δ ≈ −(r/8)(1 − n_s) ≈ −1.5e-6, i.e. a 0.3 % deviation from n_t = −r/8 — unobservable (σ(n_t) for r ~ 5e-4 is ≫ 1e-6) [estimate]. Verdict rule: "CONSISTENCY HOLDS TO X %" with X computed; no fit, no free parameter.
