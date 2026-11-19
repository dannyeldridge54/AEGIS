# PREREG D1481 — independent second-order slow-roll cross-check of DILATON32 form A, and a fast band map (help for the P3 chat)

Locked 2026-11-19 ~10:40 UTC before computing. Danny 04:33 CT: "only help other chat rn". This note does NOT touch the P3 chat's files, PREREGs, scans or D-numbers; it is our own independent check.
Model (read from field_tests/scripts/dilaton32/run.py + tools/serapis_calc/pipeline.py, form A): x = 1/2, φ = ln y/√2,
e(φ) = E(½ + iy, 3/2) − E(ρ, 3/2), V = e/(e + 1)·(1 + C e), λ = 1, T_R = 8.94e8, g* 106.75, k = 0.05.
Method (independent spectrum method): own mpmath E(τ,3/2) (zero modes + Bessel K₁ terms), own end of inflation (ε_H = 1 from the exact
background ODE, own integrator), second-order Hubble-flow slow roll (1609.04739 Eqs. 9–12; α_s to O(ε³) as D1442); N* self-consistent with
the shared tools/serapis_calc/nstar.py Nstar(r, V*/V_end, T_R) (read-only).
Part 1 (cross-check): C = 0, 1.25e-6, 1e-5 vs the P3 chat's exact-MS rows A0, A1, A2 (field_tests/results/DILATON32/*.json).
 AGREE if |Δn_s| ≤ 5e-4 and |Δr/r| ≤ 2 % for A0 and A1 (A2 reported only; n_s > 1 is outside slow-roll validity of the comparison).
Part 2 (map, [estimate]): C grid 0 … 1e-5 (21 points, log-spaced above 1e-7 plus 0): where n_s crosses 0.969 / 0.975 and r there.
 Reported as a forecast for the locked DILATON32_TILT scan (C 1.5e-6 … 4e-6), not a substitute for it; it does not alter that lock.
Fixes only via PREREG_D1481_DEVIATIONS.md first. No reruns to chase.
