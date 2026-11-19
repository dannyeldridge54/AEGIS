# PREREG_YFORK2 — DEVIATIONS (written before rerun, 2026-11-19 12:58 CT)
D1: run 1 crashed in the first case (δx = 0) with math.log(y ≤ 0). A Radau Newton trial point stepped to y ≤ 0. No outcome was printed, not even the validation number. Fixes, which leave the equations unchanged:
 (a) integrate in u = ln y instead of y (u̇ = ẏ/y; same EOM rewritten), so y > 0 always;
 (b) extend the ln E table to y ∈ [0.3, 25] (oscillations near ρ/i can cross the |τ| = 1 arc into SL(2,Z) images below y = 0.6; E is valid there);
 (c) print the spline validation before the runs.
The δx list, C, initial conditions, classification and tolerances are unchanged.
