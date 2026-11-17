# PREREG A2f — is D1111's 7PN gap from LAL's octupole/magnetic handling? (Djl D) — locked 2026-11-17
Known before the lock: on an empty LAL dict, Lookup TidalOctupolarLambda1 returns 0.0 and dQuadMon1 returns 0.0.
Probes (1.4 + 1.4, Λ = 300, TaylorF2, PNTidalOrder 7PN, D1098 method):
- P1: insert TidalOctupolarLambda1/2 = 0 explicitly. Residual vs gw.taylorf2_tidal_dphase_hfb(order 7). Hypothesis (a) is CONFIRMED iff the residual is ≤ 1e-6 rad. If it stays ~7e-4, (a) is REFUTED for octupole.
- P2: insert TidalOctupolarLambda1/2 = 1000. Report the change in LAL's detrended phase vs P1. Tells whether TaylorF2 uses octupole at all.
- P3 (reported): residual of ours(7) vs LAL with the 7PN μ̃± coefficients replaced by... nothing. No coefficient fitting is allowed. Instead, report the residual's frequency scaling (fit of residual ∝ v^n), to identify the PN order of the missing piece.
Script theory/janus_astro/a2f_check.py (written after this lock). No tuning; diagnostic.
