# D588 deviations (written before rerun)
D1: the run crashed with no output. Starting at y = 80 gives N ~ 50·(80/24)³ ≈ 1800 e-folds, beyond the N = 400 integration cap, so the end event was never reached.
Fix: start at y = 40 (N_total ≈ 230–250, still ≫ N* + 10 for attractor settling). Raise the cap to 1000.
No other change. No results were seen before this fix.
