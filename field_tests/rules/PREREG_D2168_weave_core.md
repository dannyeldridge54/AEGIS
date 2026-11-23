# PREREG D2168: weave_core, one engine for fingerprint + compass + scales + per-node optimisation (locked 22 Nov 2026 ~23:36 CT, before running)
Danny 23:31: "make an engine like ours that does our equation fingerprinting, compass, scales, all; then optimise each node with full improvements; then hand to the referee."
Engine (tools/loom/weave_core.py), built only from existing pieces, nothing re-fitted:
- NODES = every margin of the D2156 VN resonance map (layers 1-10, the same equations and data scales), evaluated at the derived dial values D (u, M_N, m3/2, T_R, split = 0, dNeff = 0).
- SCALES: each node's margin (> 0 holds).
- FINGERPRINT: the Jacobian dm_i/d(dial_j) (log dials for u, M_N, m3/2, T_R; linear for split, dNeff), central differences, step 1e-3.
- COMPASS: for each node, the unit direction of steepest improvement, and which other nodes that direction hurts (sign of J_k . direction).
- LENSES: SVD of the Jacobian (tools/loom/lens_core.py): how many independent directions the dials really have.
- PER-NODE OPTIMISATION: for each failing node, the smallest dial move (L2 in log units) that lifts it to >= 0 while keeping every node that holds at the start >= 0, found by a constrained minimiser (SLSQP, 5 starts), then VERIFIED by a full re-evaluation. Each dial moved by more than 1% counts as a fit spent (guard G-T3).
Readout per failing node: CLOSABLE (move, fits spent, who pays) or NOT CLOSABLE BY DIALS (data-fixed scale or no feasible move).
Speed: report wall time of one full fingerprint and of the whole run.
Not evidence: a deterministic consistency map (D1948). Referee review follows before anything enters the preprint.
