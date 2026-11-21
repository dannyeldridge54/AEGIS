# PREREG D1810 — DEVIATIONS (before rerun)
D1 (21 Nov 10:59): the bracket for the visible-cycle prefactor A ([0.5, 1e4]) excluded the solution (A < 0.5), so run 1 crashed before printing. Fix: bracket [1e-4, 1e4]. The visible check is report-only; dark-cycle part and verdict rule unchanged.
