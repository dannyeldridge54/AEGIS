<!-- AEGIS-FP ZIOATIWFJTCGWTXJ · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# PREREG J1c — stiff-solver fallback for singular inflation ends; PSNI rescore (follows D1020)
Locked 2026-11-17 before any J1c number.
Change: core.Model — if the DOP853 background run returns no ε_H = 1 event, rerun the same ODE with method='Radau'
(rtol 1e-11, atol 1e-13); everything else unchanged. Regression guard (must hold before scoring): the J7b Janus numbers
for LFI p = 2 and SI at N* = 50, 60 are reproduced to |Δn_s| ≤ 1e-12 (those models never take the fallback).
Then the J7d2 script (unchanged) is rerun for PSNI α = 1e-3, f = 5: report per-point |Δn_s|, |Δr/r|, |Δα_s| for Janus
and ASPIC vs exact MS (exact MS uses ms.Background, which gets the same fallback). If the fallback still fails, report and stop.
