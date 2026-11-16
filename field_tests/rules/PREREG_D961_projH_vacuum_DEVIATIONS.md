# DEVIATIONS (written before any run produced results)
D1 (code bug, found 16 Nov 16:54 CT from "Polyfit may be poorly conditioned" warnings in the D958 run log, which was then stopped with no results file written):
the script calls spectra(..., dlnk=(-0.05, 0.0, 0.05)) — 3 points — while tools/serapis_calc/ms.py (after the 5-point upgrade) always fits a degree-4 polynomial, which is underdetermined for 3 points, so n_s/r/alpha_s from such a call are unreliable.
Fix: ms.py fits degree min(4, npoints - 1); selftest gains a check that a 3-point call reproduces the 5-point n_s to 1e-4 on m^2 phi^2. The script's stencil and everything else in the lock are unchanged. One run.

D2 (written before any rerun; run 1 crashed with no results file): the script starts the background at Ehat = 600/lambda' in the PAPER convention (2 zeta(4) larger than the normalised one used when that start rule was first written), which gives fewer total e-folds than the N* ~ 50 being asked for; the N* iteration then evaluated the background before its start (extrapolated V < 0, sqrt NaN, log domain error). Log: tools/calcq/logs/D961-projH.log (run 1, kept).
Fix: start at Ehat = 5000/lambda' (capped inside the spline grid) and assert Ntot >= N* + 8 before any spectrum is taken. Everything else in the lock unchanged. One run.
