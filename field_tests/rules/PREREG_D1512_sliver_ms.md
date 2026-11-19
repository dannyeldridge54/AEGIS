# PREREG D1512 — tilt plan T3f: exact Mukhanov–Sasaki check of the physical-frame DILMIX sliver point (α 0.1, C 1.8e-6)

Locked 2026-11-19 ~14:12 UTC before computing. Our own file and D-number; not a P3 locked grid point.
Engine: shared pipeline (tools/serapis_calc pipeline.predict: exact MS spectra, self-consistent N*, T_R 8.94e8) with our own copy of the DILMIX overrides
(as D1491) and the physical frame: lam = 1/9930.9 (D1505 benchmark (200,1000)); the pipeline's tilt is C_pipe·g/lam, so C_pipe = 1.8e-6·lam gives V = P(1 + 1.8e-6·g)
as in D1510; ymax raised to 2e5 and npts to 8000 so the plateau region (y* ≈ 3.1e3) and ≥ 100 e-folds are on the grid; DILATON32 D1 start rule.
Forecast under test (D1510 SR): n_s 0.97197, r 5.462e-4. AGREE if |Δn_s| ≤ 5e-4 and |Δr/r| ≤ 2 %; IN BAND if n_s ∈ [0.969, 0.975] and r ∈ [4.55, 5.7]e-4.
Fixes only via PREREG_D1512_DEVIATIONS.md first. No reruns to chase.
