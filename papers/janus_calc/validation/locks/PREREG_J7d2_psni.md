<!-- AEGIS-FP HXYPJVJPRJL4KASX · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# PREREG J7d2 — PSNI rescore with a bisection start-finder (J1b), follows D1018
Locked 2026-11-17 before any J7d2 number.
J1b: tools/janus_calc/anyV.py gets start_bisect(V, dV, y_lo, y_hi, Nwant=80): bisection on the starting field y₀ between
y_lo (pivot side) and y_hi (hilltop side) for the total e-folds N_tot(y₀) of the exact background = Nwant (±0.5),
Nmax = 20000. Used for PSNI α = 1e-3, f = 5 (V = 1 + α ln sin(y/f), y = f(π/2 − x)), N* = 50 and 60, against the
already-committed ASPIC numbers (field_tests/results/janus_j7d_aspic_raw.txt) and the exact MS reference (J7b settings).
Scores reported per point (|Δn_s|, |Δr/r|, |Δα_s| for Janus and ASPIC). The J7d verdict is not re-evaluated; these two
points are added to the running total with their own line. If the bisection fails, report and stop (no further tuning).
