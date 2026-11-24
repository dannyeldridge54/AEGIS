# PREREG D2240 — Exhaust-solutions pass (reactor paper 2 test), locked 2026-11-23

Question: D2239 found no design that meets every limit; the wall is the exhaust/H-mode squeeze. Does an
advanced-divertor exhaust solution open a window?

Engine: theory/tests/d2239_breathe.py unchanged (same physics, limits, starts, coil classes, breathing rule),
with two added knobs only:
- leg ladder extended [1,2,3,4,5] (connection-length multiplier; long-leg / Super-X class). ESTIMATE: models
  only connection length, not flux expansion.
- nu ladder [0.4,0.5,0.6]: separatrix density n_u / <n> (literature range ~0.3-0.6). ESTIMATE.
Unchanged: seeding cap 5% SOL Ar, core Ar = c/3 floor, L-H 1.3 P_LH <= P_loss, Greenwald 0.94, beta_N 2.8,
wall 2.0, coil 12/20 T, TBR margin, Lengyel K0, compression 3.

Control (must reproduce before any reading): with leg<=3 and nu=0.4 fixed, all six D2239 endpoints infeasible.
Verdicts (fixed now):
- WINDOW OPEN: >=1 run per coil class ends feasible; TRIANGULATED if >=2 of 3 starts in a class end within one
  ladder step on every knob.
- WINDOW CLOSED: no feasible endpoint.
- Points needing the 5 cm first-wall blanket inherit the D2238 SUSPECT flag.
Run once. Fixes only via PREREG_D2240_EXHAUST_PASS_DEVIATIONS.md written before any rerun.
