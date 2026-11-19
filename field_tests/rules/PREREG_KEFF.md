# PREREG KEFF — does the UCHART two-number reduction work? Measure each real route's effective approach exponent at horizon exit

Locked 2026-11-19 (08:40 CT) before computing. Danny "Djl" (follow-up to D1516).
Definition: plateau variable e(y) with V = e/(e+1)(1 + C e); k_eff(y) = d ln(1 + e)/d ln y (= k exactly for the pure-power family).
y* = exp(√2 φ*), φ* = field at the self-consistent N* (engine F as PREREG_UCHART: third-order flow, T_R 8.94e8, λ = 1, DILATON32 D1 start).
Models (same e as their locked tests): S = SERAPIS-E E(τ,2) at C 1.25e-6; A1 = form A, e = x, x = E(τ,3/2) − E(ρ,3/2), C 1.25e-6;
B0 = form B, e = (1+x)² − 1, C 0; M25, M50 = DILMIX α 0.25 / 0.5, e = g = P/(1−P), C 1.25e-6; control U2 = pure y^2, C 1.25e-6 (must give 2).
Report k_eff(y*), y*, and the UCHART-F prediction at (k_eff, C) by bilinear interpolation of field_tests/results/UCHART/F_*.json vs the
model's own engine-F n_s, r (computed here) and its locked exact row where one exists (DILATON32 A1/B0, DILMIX a0.25/a0.5_C1.25e-06).
Rule: reduction "works" for a model if the chart prediction is within |Δn_s| ≤ 0.003 and |Δr|/r ≤ 20 % of its own engine-F values and
gets its in-band / out status right; "works" overall if all of S, A1, B0, M25, M50 pass. Expectation stated now: S ≈ 2, A1 ≈ 1.5,
B0 ≈ 3 (minus vacuum-side corrections), M25/M50 in the 1.5→3 crossover with k_eff ≈ 1.9–2.1 (they are in band).
No reruns to chase results; fixes only via PREREG_KEFF_DEVIATIONS.md written first.
