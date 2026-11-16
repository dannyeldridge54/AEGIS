# DEVIATIONS (written before any run produced results)
D1 (code bug, found 16 Nov 16:54 CT from "Polyfit may be poorly conditioned" warnings in the D958 run log, which was then stopped with no results file written):
the script calls spectra(..., dlnk=(-0.05, 0.0, 0.05)) — 3 points — while tools/serapis_calc/ms.py (after the 5-point upgrade) always fits a degree-4 polynomial, which is underdetermined for 3 points, so n_s/r/alpha_s from such a call are unreliable.
Fix: ms.py fits degree min(4, npoints - 1); selftest gains a check that a 3-point call reproduces the 5-point n_s to 1e-4 on m^2 phi^2. The script's stencil and everything else in the lock are unchanged. One run.
