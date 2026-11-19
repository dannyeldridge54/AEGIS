# PREREG D1397 — DEVIATIONS / reading notes (written after the run; NOTHING rerun)

## N1 (2026-11-18 20:00 CT)
R0 completed (G0 PASS). R1 crashed (scipy: non-finite y0): the pipeline's start rule p0 = (grid point where e = 600·λ) puts the
field at x = λ(E − E_ρ) = 0.344 in the physical frame — on the shoulder, steep, too few e-folds. Diagnosis showed the lock's design
mixes frames: with C rescaled per D698 (C_phys = C/λ), horizon exit moves to x* ≈ 460 (y* ≈ 14.58/√λ), not to x ≈ 0.3, and the
tilt at x ~ 3–5 (needed for p > 0 below the peak) is ~4x (C_phys·Ê = 1.25e-6·x/λ²), so R2/R3 as locked are ill-posed.
Decision: R1–R3 are NOT rerun (R1 would only re-confirm D698; R2/R3 need a new design). Recorded as a design error in D1397.
