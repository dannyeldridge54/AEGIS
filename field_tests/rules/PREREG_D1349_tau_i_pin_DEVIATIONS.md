# DEVIATIONS for PREREG_D1349 (written before the rerun)
D1 (crash): at y = 5 the x-curvature is exponentially small (~e^(−2πy) ≈ 2e-14 of V), below double-precision central differences; both step sizes give 0 and the h-check divided by zero. Fix: guard the h-check; report "|∂²ₓV| below double precision (< 1e-12)" for such y. These points need no pin.
D2 (normalisation): the run divided by the local V(0, y); the lock defines V0 as the plateau scale. V here is already V/V0 (P_E → 1 on the plateau), so A_min = max_y [−∂²ₓV(0,y)]/(4π²) with V0 = 1. The rerun prints both, labelled. No change to C, the grid, the step sizes or the τ = i curvature check.
Single rerun; verdict from it.
