# PREREG D1398 — DEVIATIONS (written before any rerun)

## D1 (2026-11-18, before rerun)
Both first runs (C = 0) crashed in ms.spectra (non-finite y0) before any row was printed — no result seen. Diagnosis: the
pipeline's start rule (e = 600·λ) puts the field at y ≈ 120 for this model, giving only N_end = 21.7 e-folds (the full-Y plateau
is approached as 1/U₂, much slower in e-folds than E(U,2)'s 1/U₂²). Fix: start at the deepest grid point (ph[-5], y ≈ 2976),
which gives N_end = 120.5 for T₂ = 4. Implemented by wrapping pipeline.build to return that start point. Model, scan, band and
rule unchanged.
