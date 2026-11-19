# PREREG D1488 — SR forecast of the LVSDIL k-scan (help for the P3 chat)

Locked 2026-11-19 ~11:39 UTC before computing. Our own check (Danny 04:33 "only help other chat"); no P3 files, scans or D-numbers touched.
Model (read from field_tests/scripts/lvsdil/run.py + PREREG_LVSDIL): x = ½, φ = ln y/√2, E = E(½ + iy, 3/2), F(E) = E^{1/3}·exp(−k E^{2/3}),
V = 1 − F(E)/F(E_ρ), C = 0, λ = 1, T_R = 8.94e8. k ∈ {0.15, 0.3, 0.6, 1.2}.
Method: D1485 (independent second-order SR with Taylor-based flow parameters, own exact background to ε_H = 1, shared Nstar read-only).
No exact LVSDIL rows exist at lock time, so this is a forecast only ([estimate]); when the P3 chat's rows appear, compare (AGREE if |Δn_s| ≤ 5e-4, |Δr/r| ≤ 2 %).
Report n_s, r, α_s, N*, Im τ at horizon exit, vacuum-at-ρ flag (k·E_ρ^{2/3} > ½), in band / near by SMSCAN rules; also test the PREREG's stated expectation (r ≪ 1e-4).
Fixes only via PREREG_D1488_DEVIATIONS.md first. No reruns to chase.
