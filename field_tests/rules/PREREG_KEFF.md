# PREREG KEFF — read every existing P3 route off the universal chart: effective approach exponent k_eff at horizon exit

Locked 2026-11-19 (08:50 CT) before computing. Danny "Djl". Follows D1516 (UCHART: band ⇔ k ≈ 1.85–2.2, C ≈ 1–1.6e-6).
Definition: along the pipeline path, 1 − V₀ = 1/(e+1) for the untilted plateau, k_eff(y) = d ln(e + 1)/d ln y, evaluated at y* = the field
value N* e-folds before the end (engine F: third-order flow + self-consistent N*, same as UCHART), λ = 1, T_R 8.94e8.
Routes (each with its own tilt as run before): SERAPIS-E (E(τ,2), C 1.25e-6); form A E(τ,3/2) (C 0 and 1.25e-6 = DILATON32 A0/A1);
form B (C 0 = B0); DILMIX α ∈ {0.25, 0.5, 0.75} × C ∈ {1.25, 2.5}e-6 (λ = 1).
Rule (does the chart predict the route?): for every route, read the UCHART F grid at (k_eff, C) by bilinear interpolation and compare with
the route's own exact result (field_tests/results/DILATON32, DILMIX). "Chart predicts" if |Δn_s| ≤ 0.002 and |Δr|/r ≤ 15 % for all
routes with valid neighbours; else report which routes break the two-number reduction and by how much.
Expectation stated now: E(τ,2) k_eff ≈ 2, form A ≈ 1.5, form B ≈ 3; DILMIX in-band points ≈ 1.85–2.05 (D1495).
No reruns to chase results; fixes only via PREREG_KEFF_DEVIATIONS.md written first.
