# PREREG R5b — close D1045's caveat: fine κ scan for the ℓ = −ln(2 Im T) tilt
Locked 2026-11-17 before any R5b number. Same code/model as R5. κ on 41 log-spaced magnitudes per sign, |κ| ∈ [1e-5, 1e-2]
(plus κ = 0). Record n_s(N*=49.49) − target at each; any finite sign change → brentq κ* and run R5's three-N* comparison
(same tolerances: |Δn_s| ≤ 3e-4, |Δr/r| ≤ 2%, |Δα_s| ≤ 2e-5). No sign change among finite values → R5 FAILS confirmed (no κ in
1e-5 ≤ |κ| ≤ 1e-2). Results: field_tests/results/r5b_fine_scan.txt.
