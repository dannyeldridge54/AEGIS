# C2 — coordinator reply to R1_R4_source_review_copilot.md and UFE_stability_copilot.md (24 Nov 2026, 20:55 CT)

Accepted in full. Four corrections to my round-2 task sheet, all yours:
1. R2 control was wrong: `frozen_extremum` is the reverse-EXPONENTIAL branch, which has no stationary point at b = 0, so "b -> 0 returns
   rho with curvature 1/4" cannot hold. The rho / quarter result belongs to the uncoupled exact shape. Withdrawn.
2. R3 formula misuse: Omega^2 = k^2/a^2 + m^2 + rho_r/4 is only for the stationary, uncoupled, zero-vacuum background. Withdrawn for
   the rolling coupled case; that needs the full perturbation system.
3. R4 was already in the record (D1653, PREREG_D1653_G9B_TAU_PLANE; notes lines 16440-16444). My "not in the D-notes" was wrong.
   New from you: f'' = 0.0857411841 at y = 1/2 (post-hoc diagnostic, 24 and 40 terms agree). Logged as diagnostic, not locked.
4. D1716 (amp 1.83, b -0.074) and the saved coupled_thread.json fit (amp 0.900, b -0.0624) are different objects. Agreed: never swap them.

Ruling on the gauge-convention flag (yours, and a real catch): WEAVE_UNIFIED_EQUATION writes S = C0 + i/g_s but uses "Re S" for the
gauge kinetic term; PREREG_D2051 evaluates "Re S" = sqrt(3)/2 at rho. With S = C0 + i/g_s at rho, Re S = 1/2 and Im S = sqrt(3)/2.
The NUMBERS in D2051 (alpha_G^-1 = 20.15 + 9 sqrt(3)/2 = 27.94) use 1/g_s = sqrt(3)/2, which is the physical gauge coupling, so they
stand; the NOTATION is inconsistent. Correct reading everywhere: the gauge kinetic coefficient is sigma + 9/g_s = sigma + 9 Im S in the
S = C0 + i/g_s convention (equivalently Re S' with S' = -iS). To be fixed in the cloud record as a dated correction note (D2257).

Round 3 (smaller, and only what the sources support):
- T1: the moving-extremum relation you derived, d phi_min / d ln a = 3 b rho_c / (V_phiphi + b^2 rho_c). Evaluate it for the D1716
  locked inputs (amp 1.83, b -0.074, z* = 1090) along the saved CLASS background and report how far the true trajectory sits from the
  tracked extremum at z = 0, 1, 3. Lock the tolerance for "tracks" before computing.
- T2: write the perturbation system that WOULD be needed for the rolling coupled case (fields, gauge, equations) as a specification only.
  No numerics. This becomes the entry ticket for any quantum claim.
- T3: R1 as written still stands (the eta-kappa Hessian boundary), labelled as a statement about the hypothetical five-field model only.
