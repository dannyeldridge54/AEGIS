# PREREG UCHART — DEVIATIONS (written before any rerun; none planned)

## D1 (2026-11-19 08:45 CT) — validity flag, no rerun
11 of 64 engine-F points returned non-physical numbers (|n_s| ~ 1e86–1e100, N* 92–106): (2.25, 2.5–3e-6), (2.5, 2–3e-6), (3.0, 1–3e-6).
Cause: at large k·C the tilt C·e grows like y^k and the N* iteration walks to N* > ~90, past the slow-roll stretch of the background
(the potential is tilt-dominated there, no plateau at horizon exit); the flow expansion is then evaluated outside its domain.
Treatment: these points are marked INVALID (no plateau observable), excluded from the band map, and not rerun. Validity filter, fixed
now and applied to every row: 0.9 < n_s < 1.05, 0 < r < 0.1, 45 < N* < 60. They do not touch the band boundary: every valid neighbour on
their side already has n_s ≥ 0.975 (k = 2.25, C = 2e-6: 0.992; k = 2.5, C = 1.5e-6: 0.998; k = 3, C = 5e-7: 0.984).
Note: the exact check point (2.5, 2e-6) lies in this INVALID region; it is kept as locked and reported as is.
