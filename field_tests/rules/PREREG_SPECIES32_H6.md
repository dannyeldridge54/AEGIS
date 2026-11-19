# PREREG SPECIES32_H6 — D1524 open item 3: does the R⁴ tilt's H⁶ ∝ V³ factor change the D1523 band?

Locked 2026-11-19 (09:10 CT) before computing. Same code as PREREG_SPECIES32 (+ its DEVIATIONS D1 stencil), engine F, T_R 8.94e8.
Tilt T2: V = V₀·(1 + C·V₀³·(E − E_ρ)) (H⁶ ∝ V³ on the trajectory, V₀ normalised to 1 on the plateau) vs T1 = V₀(1 + C(E − E_ρ)).
Points: C ∈ {6.8e-7, 8e-7, 9.3e-7} under T2; compare with T1 rows (T1 at 6.8e-7 and 9.3e-7 computed now under T1 too).
Rule: "H⁶ factor negligible" if |Δn_s| ≤ 2e-4 and |Δr|/r ≤ 2 % at all three; else report the shift and the T2 band.
Expectation: V₀(y*) ≈ 0.9976 ⇒ tilt smaller by ~0.7 % ⇒ Δn_s ≈ −5e-5. No reruns to chase; fixes only via a DEVIATIONS file written first.
