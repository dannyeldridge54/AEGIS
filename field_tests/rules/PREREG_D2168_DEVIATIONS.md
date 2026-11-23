# D2168 DEVIATIONS
## DEV-1 (written before the rerun): crash fix
The first run crashed inside SLSQP: a trial step took a log dial to exp(-huge) = 0 (ZeroDivisionError in L2 M_N_top). Fix: bounds |z_j| <= 3 on every dial (a factor e^3 = 20 in the log dials; +-3 on split/dNeff), and a failing evaluation returns -1e6 for every node (infeasible). No equation, scale or readout changed. No result existed from the first run.

## DEV-2 (referee R68, written before the rerun)
1. Jacobian: the ACT-dNeff and BBN-spine rows have a log floor max(dn, 1e-6) at dn = 0; the +-1e-3 step crossed the kink and produced -3454 artefacts. Their dNeff entries are set to 0 (true local slope at dn = 0 is 0) and the lens rank is recomputed, also on the column-normalised J.
2. Spent-dial noise: |z_j| < 1e-6 is set to 0 and the point re-verified before applying the 1% (log) / 1e-9 (linear) spent rule; ties in the objective go to the earlier start.
3. split is a STEP dial: removed from the smooth optimiser; each failing node is optimised twice, split off and split on (any nonzero split), and reported as CLOSABLE / CLOSABLE ONLY WITH THE SPLIT STEP / NOT CLOSABLE.
4. The dNeff >= 0 wall (100 min(dn, 0)) is added as a fixed node.
5. Timing with time.perf_counter, reported in ms.

## DEV-2 addendum (R69-1, recorded): the code also zeroes the dNeff slope of the L10.dNeff_nonneg wall row (kink at dn = 0; slope on the allowed side is 0). With that row's slope kept, the raw lens rank is 4; the headline rank is the column-normalised one (5).

## DEV-3 (R69-3, written before running): JOINT readout added
For split off and split on: maximise t subject to margin_i(z) >= t for every node a dial can move (nodes whose fingerprint row is nonzero), all smooth dials within |z| <= 3, SLSQP, 5 starts. Report t*, which nodes are >= 0 at the joint optimum, which got WORSE than at the derived dials (including nodes that were already failing), and the fits spent. Per-node results stay as they are; the joint readout is the one to use.

## DEV-4 (written before running): joint readout redesigned (D2168b)
Hard constraints: every node that holds at the derived dials stays >= 0 (walls included). Excluded: nodes shown NOT CLOSABLE BY DIALS (L4, L9, L10 H0). Objective: maximise the minimum margin over the remaining failing nodes (wino, alpha_s, leptogenesis); report which of them reach >= 0 together, split off and split on (split on handled by fixing alpha_s to its split value, since the step makes it constant).
