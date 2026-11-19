# PREREG D1483 — independent second-order SR cross-check + forecast of the SMSCAN (s, m) grid (help for the P3 chat)

Locked 2026-11-19 ~10:40 UTC before computing. Our own check (Danny 04:33 "only help other chat"); no P3 files, scans or D-numbers touched.
Model (read from field_tests/scripts/smscan/run.py + PREREG_SMSCAN): x = ½, φ = ln y/√2, e = (E(½+iy, s)/E(ρ, s))^m − 1,
V = e/(e + 1) = 1 − (E_ρ/E)^m, C = 0, λ = 1, T_R = 8.94e8. Same method as D1481 (own mpmath E(τ,s), own exact background to ε_H = 1,
second-order Hubble-flow SR 1609.04739, shared Nstar() read-only).
Part 1 (cross-check): grid points already reported by the P3 chat at lock time — (2, 1/2), (2, 1), (3, 1/3) — AGREE if |Δn_s| ≤ 5e-4 and |Δr/r| ≤ 2 %.
Part 2 (forecast, [estimate]): the remaining SMSCAN grid points (3, 2/3), (3, 1), (2, 3/2), (1.5, 1), (1.5, 4/3): n_s, r, α_s, N*, in-band/near
by SMSCAN's own rules. A forecast only — the P3 chat's locked runs are the record.
Fixes only via PREREG_D1483_DEVIATIONS.md first. No reruns to chase.
