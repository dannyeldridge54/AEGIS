# D2168 DEVIATIONS
## DEV-1 (written before the rerun): crash fix
The first run crashed inside SLSQP: a trial step took a log dial to exp(-huge) = 0 (ZeroDivisionError in L2 M_N_top). Fix: bounds |z_j| <= 3 on every dial (a factor e^3 = 20 in the log dials; +-3 on split/dNeff), and a failing evaluation returns -1e6 for every node (infeasible). No equation, scale or readout changed. No result existed from the first run.

## DEV-2 (referee R68, written before the rerun)
1. Jacobian: the ACT-dNeff and BBN-spine rows have a log floor max(dn, 1e-6) at dn = 0; the +-1e-3 step crossed the kink and produced -3454 artefacts. Their dNeff entries are set to 0 (true local slope at dn = 0 is 0) and the lens rank is recomputed, also on the column-normalised J.
2. Spent-dial noise: |z_j| < 1e-6 is set to 0 and the point re-verified before applying the 1% (log) / 1e-9 (linear) spent rule; ties in the objective go to the earlier start.
3. split is a STEP dial: removed from the smooth optimiser; each failing node is optimised twice, split off and split on (any nonzero split), and reported as CLOSABLE / CLOSABLE ONLY WITH THE SPLIT STEP / NOT CLOSABLE.
4. The dNeff >= 0 wall (100 min(dn, 0)) is added as a fixed node.
5. Timing with time.perf_counter, reported in ms.
