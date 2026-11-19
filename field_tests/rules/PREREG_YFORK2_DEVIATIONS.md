# PREREG_YFORK2 — DEVIATIONS (written before rerun, 2026-11-19 12:58 CT)
D1: run 1 crashed in the first case (δx = 0) with math.log(y ≤ 0). A Radau Newton trial point stepped to y ≤ 0. No outcome was printed, not even the validation number. Fixes, which leave the equations unchanged:
 (a) integrate in u = ln y instead of y (u̇ = ẏ/y; same EOM rewritten), so y > 0 always;
 (b) extend the ln E table to y ∈ [0.3, 25] (oscillations near ρ/i can cross the |τ| = 1 arc into SL(2,Z) images below y = 0.6; E is valid there);
 (c) print the spline validation before the runs.
The δx list, C, initial conditions, classification and tolerances are unchanged.
D2 (2026-11-19 13:00 CT, before rerun 3): run 2 passed validation (5.2e-9) but after 11 min it had not finished even the first case. Two causes: Radau with a numerical Jacobian, and the locked early-stop rule, which was never implemented (implementation bug). No outcome was seen. Fixes:
 (a) implement the stop as a terminal event: total energy K + V < 1e-4 V∞. This is below every ridge value in the fork band (V₀ ≥ 2e-3 on the ridge for y ≥ 0.99, D1605), so the field is trapped in one basin. The stopped state is then classified;
 (b) classify after reducing τ to the standard fundamental domain (|x| ≤ ½, |τ| ≥ 1): "i" if |τ − i| < 0.15; "ρ" if within 0.15 of e^{iπ/3} or e^{2πi/3}; "other" otherwise. The orbit can cross into SL(2,Z) images, and the locked 0.05 radius in un-reduced coordinates would misclassify those;
 (c) solver DOP853 (rtol 1e-9, atol 1e-12) instead of Radau. The system is not stiff before the stop.
The δx list, C, initial conditions and the end-of-inflation (ε = 1) report are unchanged.
D3 (2026-11-19 13:07 CT, before rerun 4): rerun 3 is INVALID. Every case ran to y ~ 1e-80 and ended at t = 2000 without settling. The field left the tabulated domain (y < 0.3), where the spline extrapolates and is meaningless. Rerun-3 numbers are therefore not physics; they are kept in the log only as evidence of the domain exit. Fixes:
 (a) table extended to y ∈ [0.05, 25] (600 points in ln y). The repo E (Fourier, nmax = 40) agrees with its SL(2,Z) image to 2e-8 relative at y = 0.05 (checked: 29.82137 vs 29.82136);
 (b) validation adds two points at y = 0.1 and 0.2;
 (c) new terminal event: y < 0.06 ⇒ stop and classify "toward the x = ½ cusp" (the strong-coupling image of the weak cusp), with the time and energy reported;
 (d) also report the minimum y reached and the energy at the first passage of y = 0.866.
