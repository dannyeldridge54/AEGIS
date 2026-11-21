# PREREG_RW3_PLATEAU — DEVIATIONS
## D1 (21 Nov 2026, after run 1; run-1 output kept as field_tests/results/rw3_plateau_run1_overflow.json)
- What was wrong (coding): in R3 the V_L shooting bisected over [1e-3, 1e3] and evaluated trial V_L values for which
  the field rolls past the cliff (x > 1); math.exp(−βφ) then overflowed ("math range error"). The exception was
  recorded per point, so every β = 2√2 start with x_i ≳ 0.128 (the region containing D1692's amp = 0.174) and the
  upper edge of the other tilts were lost. The validation gate correctly failed ⇒ run-1 R3 = INVALID, as locked.
- Fix: use the D1692 shooting (field_tests/scripts/realdata/run.py): V_L grid 0.5·2^k (k = 0…11), first sign change
  of H²(a=1) − 1 among finite evaluations, then brentq (xtol 1e-10); evaluations that raise are treated as
  non-finite and skipped; a start with no bracket is recorded as "no_solution". exp arguments are clipped at 700.
- Unchanged: R1, R2, R5 (no ODE; their run-1 numbers stand), all R3 grids, the gate, the VIABLE window, and the
  decision rule. Note: the run-1 decision (OPEN) does not depend on R3, because R5 already fails (m/H₀ ≫ 3).
