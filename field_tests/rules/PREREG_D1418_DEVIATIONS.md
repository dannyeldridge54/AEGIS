# PREREG D1418 — DEVIATIONS (written before the first run; no result seen)
D1. Start point: the script's φ0 = φ* + 1.0 (y0 ≈ 61) needs ≈ 850 e-folds, beyond ms.Background's Nmax = 400, so N_end would be
    None. Changed to φ0 = φ* + 0.3 (y0 ≈ 22.6, ≈ 66 e-folds before the pivot — enough for the Bunch–Davies start at k/aH = 200,
    ≈ 5.3 e-folds). No change to model, targets, solver or rule.
D2. Crash on the first run: ms.spectra returns key 'ns' (not 'n_s'); KeyError before any value was printed. Fix: read s['ns']. No other change.
