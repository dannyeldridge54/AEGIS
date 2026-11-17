# PREREG J7f — "pulse": Janus vs ASPIC on (nearly) every ASPIC model in ONE automated batch (Danny 17 Nov 00:37)
Locked 2026-11-17 before any J7f number.
Selection: every ASPIC @75400d2 model whose *sr module exposes norm_potential, norm_deriv_potential, x_endinf(params only),
x_trajectory and epsilon_one..three (47 found by script), each at ONE parameter set taken from its own *main.f90 where a value
is set there, otherwise a standard value (table in theory/janus/j7f_pulse.py, written before running). Models ASPIC cannot
run at that set (STOP / no x_end / never-ending) are LISTED with ASPIC's message, not dropped.
Per model, one generated Fortran program (separate process, so one ASPIC STOP cannot abort the batch) prints, for N* = 50, 60:
x*, n_s, r, α_s (srflow 2nd order), x_end, ε₁(x*); and V̂(x), V̂′(x) on 4000 points from x_end outward (direction from x*).
Janus and the exact reference use THE SAME potential (cubic spline of ASPIC's own V̂ and V̂′), with φ = s·x, s fixed from
ε₁ = ½(V̂′/V̂)²/s² at x*(60); exact background ends at ε_H = 1 (or, if never reached, the model is listed); start from the
grid point giving ≥ 75 e-folds (listed if the grid cannot). Reference: exact MS (J7b settings). Janus: core.spectra3.
Claims C1–C4 and verdict rule as PREREG_J7b, over all scored points. Report also the count of models scored / listed.
