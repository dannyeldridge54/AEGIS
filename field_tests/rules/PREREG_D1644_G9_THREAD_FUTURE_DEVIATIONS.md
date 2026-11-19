# DEVIATIONS for PREREG_D1644_G9_THREAD_FUTURE (written before any rerun)
D1 (coding/numerical, 2026-11-19 ~22:40Z). First run (kept on record): R2 PASS; R1 FAIL with NaN ⟨w⟩ and a³ρ ratio −138. Cause: the potential grid stopped at y = 0.45. Past ρ the Re τ = ½ line has only a tiny bump (f ≲ 7e-4), the field crossed it at a ≈ 3 and left the grid; CubicSpline extrapolation sent φ to −5e47. Not physics.
Potential checked (no results read): f = 7.8e-5 at y = 0.30 (a second zero at y = √3/6 ≈ 0.289, the SL(2,Z) image of ρ on this line), rising toward the cusp τ = ½: 0.025 (y 0.2), 0.35 (0.1), 0.75 (0.05).
Fix: grid lower edge y = 0.45 → y = 0.03 (24000 points); integration and every rule unchanged. If the field still reaches the grid edge, report that as a FAIL with reason, no further rerun.
Note for the record: the line Re τ = ½ below ρ leaves the fundamental domain; the motion there is a 1D restriction (axion direction ignored), as the lock's caveat already stated.
