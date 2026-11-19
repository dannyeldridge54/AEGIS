# PREREG DUAL — DEVIATIONS (written before any additional run)

## D1 (2026-11-19 10:08 CT) — R4 grid did not bracket n_s 0.9706; extend downward
R4 (8D level, tilt C·(E₂ − E₂,ρ), λ₈ = 0.063298) at C = 2e-7 already gives n_s 0.99122; C = 4e-7 and 8e-7 gave "inflation does not end"
and C = 6e-7 a math-domain error (tilt-dominated — the y² tilt is ~ E₂ ≈ 2.16y² ≈ 6700 at y* vs E_{3/2} ≈ 1000, so the same C is ~7× stronger).
The locked purpose of R4 was "scan to bracket n_s 0.9706", which the grid failed to do — a grid-design error, not a result to chase.
Fix: add C ∈ {2.5e-8, 5e-8, 7.5e-8, 1e-7} (same code, same rule). The failed rows are kept as reported (INVALID: tilt-dominated).
