# PREREG D1497 — help set 5: the DILMIX in-band strip in D1486's physical frame

Locked 2026-11-19 ~12:52 UTC before computing. Our own file and D-number.
Frame map (read from the P3 chat's D1486, weak_spots line 15357): for E ∝ y^{3/2}, y_phys = y_model·a^{2/3}, C_phys = C·a, a = 1/λ ∈ [5e2, 2e5]
(D1486 table: (|χ|, 𝒱) = (100,100) a 2.0e3; (200,1000) 9.9e3; (400,1e4) 5.0e4). DILMIX uses the same x = λ(E − E_ρ), so the same map applies.
Steps: (1) re-run D1486's arithmetic for its A1 rows (y* = 23.25·a^{2/3}, C_phys = 1.25e-6·a) — aegis-check; (2) model-frame y* for the 7 in-band strip
points (re-solved with field_tests/scripts/d1492/strip_running.py phistar()); (3) their y_phys, g_s* = 1/y_phys and C_phys at the three D1486 benchmark a values.
Compare C_phys with D1486's flagged source problem (BHK-type loop ∝ g_s²). [estimate]/[derived] labels; no pass/fail.
Fixes only via PREREG_D1497_DEVIATIONS.md first.
