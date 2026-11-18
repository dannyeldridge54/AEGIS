# DEVIATIONS R2e-c — written while the run is in progress, before any output was read (2026-11-18)
D1: the script does not implement scored test T1 (reproducing R2e-b's R_eff at the 25 shared x points). R2e-b did not save its R_eff tables, so there is nothing to compare against byte-for-byte. Same code and same inputs make them deterministic, but that is an argument, not a check.
- T1 is therefore NOT SCORED (recorded as not done).
- Partial substitute (reported only): the Ω h² recomputed at 2.8 and 3.0 TeV, compared with R2e-b. With R held fixed beyond 1e5 instead of 3e4, any difference mixes the tail effect with any table difference. So this result can bound the tail effect only if the difference is small.
