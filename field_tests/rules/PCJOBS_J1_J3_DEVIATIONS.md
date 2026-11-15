# PCJOBS J1–J3 — DEVIATIONS (written 2026-11-14, before any rerun)

Locks: PREREG_D500_TWISTM_CASE1 (+ its DEVIATIONS D1–D6), PREREG_PCJOBS_J2_J3.

## D7 — first PC run (2026-11-14 ~22:03 local)
- Result: J1 point crashed inside twistm_case1_d500.py with `ValueError: math domain error`
  (log of a negative argument in modular_twist_d490.lnV, reached after the ODE overflowed:
  RuntimeWarnings "overflow", "divide by zero" just before). The exception killed the whole
  multiprocessing pool, so J1, J2, J3 produced no lines.
- Physics reading (not a fix): the field left the region where V is defined, i.e. a runaway.
  Under the locked criterion this point does NOT capture.
- Fix (harness only, no physics or grid change): each job is wrapped in try/except; a point that
  raises is written as `FAILS (error: <type>: <msg>) — counted as no capture` and the pool
  continues. Grids, tolerances, criteria and code paths are unchanged.
- Rerun: once, J1→J2→J3, same grids. No further reruns unless a new DEVIATIONS entry is written first.

## Note on J4 (no rerun)
J4 completed (500 points). κ = 8 gives n_s > 1 or nonsense values (a feature enters the plateau);
κ = 7 is shifted. This is recorded as a result (validity range κ ≲ 6), not fixed.
