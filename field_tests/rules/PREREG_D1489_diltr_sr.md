# PREREG D1489 — SR forecast of DILTR (reheating sensitivity), help for the P3 chat

Locked 2026-11-19 ~11:49 UTC before computing. Our own check; no P3 files, scans or D-numbers touched.
Model and grid exactly as PREREG_DILTR: DILATON32 form A on E(τ,3/2), λ = 1, C ∈ {0, 1.25e-6}, T_R ∈ {1e8, 1e10} GeV, compared with T_R = 8.94e8.
Method: D1481 independent second-order SR (field_tests/scripts/d1481/sr_check.py functions), N* from the shared Nstar(r, V*/V_end, T_R).
Rule (DILTR's own): "robust" if |Δn_s| ≤ 0.002 and |Δr|/r ≤ 10 % across the T_R range, else "reheating-sensitive"; in band / near as SMSCAN.
Bonus ([estimate]): the same T_R sweep for D1485's best-centred DILMIX point (α 0.375, C 1.5e-6) with the D1485 method — does it stay in band?
A forecast only; the P3 chat's DILTR runs remain the record. Fixes only via PREREG_D1489_DEVIATIONS.md first. No reruns.
