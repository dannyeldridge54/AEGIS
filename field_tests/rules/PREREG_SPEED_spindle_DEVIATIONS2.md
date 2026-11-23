# SPEED-Spindle DEVIATIONS 2 (referee R79, written before fixes), 2026-11-23 ~09:35 CT
R79: S1, S2 equivalence confirmed. Defects:
DEV-2 (blocker): period_analytic fails when sin(theta) = 0 (phi = 0 or pi): rho0 is itself a turning point. Fix: if g(rho0) ~ 0,
  rho0 is one endpoint; the other is the nearest root on the side where g > 0. Case 2 DOES oscillate (r 0.02-0.30, period ~4.41,
  reference with T = 60); the earlier "does not oscillate" note is withdrawn. S3 still FAILS as locked (no rerun to chase it);
  the fixed function is re-checked against the reference with a longer window as a diagnostic only.
DEV-3 (blocker): S4 diagnosis corrected: at J = 0 the sparse path returned [1,1,1] vs dense [0,1,1] - it missed the
  NON-degenerate ground state (diagonal H: Krylov space collapses; a symmetric v0 sees one symmetry sector). Opt-in label:
  "may return wrong lowest levels, including the ground state"; dense used below dim 5000.
DEV-4: the DEV-1 rerun harness is committed (tools/qsim/speed_spindle_s4_rerun.py).
DEV-5: S2 timing redone as median of 3 (timing only; accuracy unchanged).
DEV-6: mf_single_fast asserts normalised psi; theta docstring fixed. DEV-7: citations completed (2410.09015 authors;
  Stamper-Kurn & Ueda full title; Bluvstein et al. scars under driving).
The Lantern stays at the top of the field map by the author's standing wish (referee noted it; author's call).
