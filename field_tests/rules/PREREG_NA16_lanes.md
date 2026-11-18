# PREREG NA16 — left/right/centre lane audit against the SERAPIS model
Locked before computing.
1. L_bridge: twin-ladder nulls B1 = r − 3(1−n_s)² ≈ −0.9e-4 (tol 1.2e-4) and B2 = α_s + ½(1−n_s)² ≈ 0 (tol ±1e-4, stated here). Evaluate on the PW2 point and the 9 PW1 corners (exact numbers from those results files).
   Verdict: if all fail, the bridges are nulls of the pre-SERAPIS (Twist, Starobinsky-like p = √(2/3)) model, not of SERAPIS-E (p = 2√2, κ = 1), and the web edge L_bridge → janus is relabelled "Twist-era null; SERAPIS uses the Janus relation".
   Check the reason: for a pure plateau with exponent p, leading order r = (8/p²)(1−n_s)²/4·… — compute the untilted SERAPIS-E r/(1−n_s)² from the TK1/NA data and compare with 3 (Starobinsky) and 3α = 2/p² (α-attractor form, α = 2/(3p²) = 1/12).
2. R_w0wa: SERAPIS's late universe is ΛCDM (w = −1, Σm_ν 0.0588). Report 1-D pulls of (w0, wa) = (−1, 0) from the L7 values (−0.853 ± 0.053, −0.518 ± 0.200) — information only (the correlated Δχ² is D1029/D1032's job; L5 D1032: ΛCDM + frozen Σm_ν at Δχ² 2.37, consistent).
3. C_nstar: shared N* for SERAPIS is now the audited 50.1–51.3 (ρ, D1235) and 50.40–50.45 (τ = i, D1247) — update the node text.
Results: field_tests/results/na16_lanes.txt.
