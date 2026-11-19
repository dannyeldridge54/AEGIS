# PREREG SPECIES32 — DEVIATIONS (written before any rerun)

## D1 (2026-11-19 09:12 CT) — numerical noise in run 1; derivative stencil fixed, all 8 points rerun
Run 1 (kept in field_tests/results/SPECIES32/run1_INVALID/): checks passed (V(ρ) = 2e-20, fitted approach exponent 1.996), but α_s
jumps between −7e-2 and +5e-2 across C, and n_s(C = 0) = 0.9565 vs 0.9604 for the pure k = 2 power — signatures of noise in the
higher flow parameters, not physics. Cause: y∂_y ln E was a 2-point central difference with relative step 1e-6; its round-off
(~1e-16·|ln E|/1e-6 ≈ 5e-10) is amplified by the spline's second and third φ-derivatives on the 4000-point grid (Δφ ≈ 1.4e-3) to
~1 % in η and worse in ε₃, ε₄.
Fix: 5-point stencil in ln y with relative step h = 1e-3 (truncation O(h⁴) ~ 1e-12, round-off ~ 1e-13). Model, grid, C values, engine,
start rule, band rules unchanged. Acceptance (stated now, before the rerun): α_s must be smooth and of plateau size (|α_s| < 3e-3) on
all valid points; else the engine-F rows are not quoted and only exact-MS rows are used.
