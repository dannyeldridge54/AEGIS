# PREREG D1485 — SR forecast + (α, C) band map of DILMIX (help for the P3 chat)

Locked 2026-11-19 ~10:47 UTC before computing. Our own check (Danny 04:33 "only help other chat"); no P3 files, scans or D-numbers touched.
Model (read from field_tests/scripts/dilmix/run.py + PREREG_DILMIX): x = E(½+iy, 3/2) − E(ρ, 3/2), φ = ln y/√2,
P = α·x/(1+x) + (1 − α)·[1 − 1/(1+x)²], g = P/(1 − P), V = g/(g+1)·(1 + C g) = P·(1 + C·P/(1 − P)), λ = 1, T_R = 8.94e8.
Method: D1481/D1483 independent second-order SR (own E, own exact background to ε_H = 1, shared Nstar read-only).
Part 1 (anchors, AGREE test): α = 1, C = 1.25e-6 must reproduce DILATON32 A1 and α = 0, C = 0 must reproduce DILATON32 B0 (exact MS)
 to |Δn_s| ≤ 5e-4 and |Δr/r| ≤ 2 %.
Part 2 (forecast, [estimate]): the 6 locked DILMIX points α ∈ {0.25, 0.5, 0.75} × C ∈ {1.25e-6, 2.5e-6} — in band / near by SMSCAN rules.
Part 3 (map, [estimate]): α ∈ {0, 0.125, …, 1} × C ∈ {0, 0.5, 1, 1.5, 2, 2.5, 3, 4}e-6: the (α, C) region with n_s ∈ [0.969, 0.975] and
 r ∈ [4.55, 5.7]e-4 (and the frozen-band variant n_s 0.970–0.975). A forecast only; the P3 chat's locked runs remain the record.
Fixes only via PREREG_D1485_DEVIATIONS.md first. No reruns to chase.
