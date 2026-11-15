# D588 deviations (written before rerun)
D1: the run crashed with no output. Starting at y = 80 gives N ~ 50·(80/24)³ ≈ 1800 e-folds, beyond the N = 400 integration cap, so the end event was never reached.
Fix: start at y = 40 (N_total ≈ 230–250, still ≫ N* + 10 for attractor settling). Raise the cap to 1000.
No other change. No results were seen before this fix.

D2 (after the first post-D1 run; results were seen and are INVALID): mode amplitudes |R| ~ 1e-145 lie far below atol = 1e-30, so the solver applied no error control. This gave nonsense two-term n_s (≈ −25) and failed the HS-Kairos validation (MS 0.9642 vs attractor 0.9592, limit 0.002).
Fix: the mode equations are linear, so integrate the normalised modes R/|R₀| and h/|h₀| with atol = 1e-12 and rtol = 1e-10, then rescale. No other change. One rerun. The validation rule stays as locked; if it fails again, D588 is reported as FAILED with no further reruns this tick.
