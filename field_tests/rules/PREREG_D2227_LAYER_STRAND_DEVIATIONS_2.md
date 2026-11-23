# D2227 DEVIATIONS 2 (after run 1 and referee round 8, before the one rerun)
Run 1 (field_tests/results/d2227_layer_strand.json): official 0/30 stable (model point fails only on alpha_s/Hoyle, as known); threshold
column 30/30 "stable" - INVALID: hex.loop's Forces postulate re-set s_m32 (to ~1, which puts alpha_s on 0.118) at every point, so the pulse
erased the strand (e.g. points with m3/2 x 5e-8 reported no wino/gluino OUT). The official column only escaped because that move worsened the target.
- DEV-1 (BUG, harness): strand variables are string data, not centre knobs. Rerun freezes T_R and s_m32 at the strand values; only C (the
  inflation coefficient) may re-settle, via the Inflation node's own postulate (accepted only if the Bloom target improves).
- DEV-2 (referee R109 #3, invented coupling): sigma (the condensing stack's 4-cycle) is held at 20.15; it is NOT tied to the visible Re T.
  So g changes only T_R (through x), Re S changes g_s and T_R, N changes m3/2.
- DEV-3: the wino band check is reported as its own column (wino mark) next to the full stability flag.
Unchanged: strand ranges, stability rule, the two alpha_s variants, the reading.
