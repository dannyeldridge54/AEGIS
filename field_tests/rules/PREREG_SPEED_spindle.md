# PREREG SPEED-Spindle (rotation rung 1, one wave), locked 2026-11-23 ~09:05 CT before code
Goalposts set up front (Danny: "set the goalposts at the beginning, one pulsing wave").
Reference = the D2183 engine tools/qsim/loom_qsim.py, unchanged. Fast paths in tools/qsim/spindle_fast.py.
S1 sma_rho0 vectorised over times (one matrix product): matches reference to 1e-12 (abs) on N in {6, 40, 200}.
S2 mean-field single-site run with scipy DOP853 (rtol 1e-10, atol 1e-12) instead of the Python RK4 loop: rho0(t) matches the
   reference RK4 (dt = 1e-3) to 1e-6 (abs) over t <= 12 on three locked cases (c, q, rho0, phi) =
   (1, 0.3, 0.5, 0.5), (1, 1.5, 0.3, 0), (-1, 0.5, 0.6, 1.0).
S3 analytic period: single-mode mean-field energy E = c r(1-r)(1+cos th) - q r gives (dr/dt)^2 = 4 (E+qr)(2c r(1-r) - E - qr);
   period = 2 * integral between turning points (scipy quad). Must match the reference osc_obs period to 2e-3 relative on
   the three cases (the reference period is itself an interpolated crossing average). Accepted only if the formula's
   normalisation agrees; otherwise recorded as failed and the numeric path is kept.
S4 Bose-Hubbard: sparse Lanczos (scipy eigsh) for the lowest k levels matches dense eigvalsh to 1e-10 at (L, N) = (5, 5),
   and enables (6, 6) and (7, 7) (reported, no reference).
Timing protocol: wall time, median of 3, same machine, reported before/after.
Field map (same wave): quantum simulation with ultracold atoms / spinor BECs: the field's planning studies and reviews,
Oklahoma people (Y. Liu, OSU), needs, our coverage, gaps, build order -> releases/field_maps/quantum_simulation.md.
