# PREREG_A3_D6_B — the D = 6 one-loop sign with a B-field (locked D1683, 2026-11-20 00:52 UTC)
Slice: T⁴ = T²×T², each with Kähler T = b + iR² and complex structure U = i, so Γ_{4,4} = Γ_{2,2}(T,U)². Γ_{2,2} in the Hamiltonian form over (m₁, m₂, n₁, n₂), truncated |·| ≤ 6.
Validation (must pass): RN∫Γ_{2,2} at T = 0.5 + i, U = i equals DKL −log(T₂U₂|η(T)η(U)|⁴) − log(8πe^{1−γ}/(3√3)) + 0.04523 (scheme term, D1680) within 3 × 10⁻³. Also b = 0, R = 1 must reproduce D1680's −0.662 within 0.02.
Compute: I for (R, b) ∈ {1, 1.25} × {0, 0.25, 0.5}, Zagier scheme.
Reading: if every b ≠ 0 point has I ≥ I(b = 0) at the same R, the B-field only HELPS (the self-dual point is the worst case) and A3 for D = 6 is closed; otherwise report where I is lowest.
Script: field_tests/scripts/a3d6/bfield.py
