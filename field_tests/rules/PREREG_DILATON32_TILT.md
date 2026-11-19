# PREREG DILATON32_TILT — can form A (x/(1+x) on E(τ,3/2)) reach the band with an intermediate tilt? (D1479 follow-up)

Locked 2026-11-19 before computing (Danny "Djl" 04:26, plan item 3).
Same model, code path and start rule as PREREG_DILATON32 + its DEVIATIONS D1 (field_tests/scripts/dilaton32/run.py, form A, λ = 1,
T_R = 8.94e8). C ∈ {1.5e-6, 2e-6, 2.5e-6, 3e-6, 4e-6} (fixed now). From D1479: C = 1.25e-6 → n_s 0.9672, r 6.25e-4; C = 1e-5 →
n_s 1.003, r 1.5e-3; r rises with C, so the band's r edge (5.7e-4) is expected to bind.
Rule: "in band" if any C gives n_s ∈ [0.969, 0.975] AND r ∈ [4.55e-4, 5.7e-4] → "E(τ,3/2) one-power plateau viable (fixed-point)";
else record the closest point and "not in band at any tested tilt" (expected outcome stated now: r > 5.7e-4 whenever n_s ≥ 0.969).
No reruns to chase results; fixes only via PREREG_DILATON32_TILT_DEVIATIONS.md written first.
