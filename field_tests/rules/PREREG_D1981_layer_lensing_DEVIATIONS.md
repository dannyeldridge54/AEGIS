# D1981 DEVIATIONS (written before the one rerun, 22 Nov 2026 ~00:47Z)
Run 1 crashed: the lock did not define a layer with margins but **rank 0**, meaning no knob moves any of its margins.
- Seen at L4 (cube): rung_agreement = ln1.15 − ln(max/min of [u, 0.0253, 0.0292]); u = 0.0266 is neither the max nor the min, so its derivative is 0 in R1 and R2.
- **Fix (definition only, no tolerance touched):** a rank-0 layer is **OPAQUE**.
  - Its projector is 0, so it blocks every direction.
  - Any transfer into or out of it is BLOCKED (angle 90°).
  - Its coupling row and column are 0.
  - This follows directly from the lock's definitions: no lens directions means nothing passes.
- Seen in the run 1 diagnostics and **not changed**: R2 (±3 % probes) is not linear where margins have kinks (L1 quark window, L7 |pull| and |split|). Per the lock, any disagreement makes that item INDETERMINATE. The ±3 % width stays.
- Seen and **reported as the lock asks**: R3 (KNOBS_OF) is wrong at L8. The gravitino box depends on m3/2 through M2, which the hand label leaves out. It is also wrong at L4, where the label says u but the true response is 0.
- 00:49Z addendum: the rerun crashed again before printing anything, on the 'shared knobs' display field of the same rank-0 layer. Guarded it (an empty lens shares nothing). No result had been produced, so nothing is being chased.
