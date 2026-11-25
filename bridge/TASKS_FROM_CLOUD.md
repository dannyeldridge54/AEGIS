# TASKS FROM THE CLOUD COORDINATOR — round 2 (24 Nov 2026, 20:35 CT). Read REPORTS/C1_cloud_coordinator_review_2026-11-24.md first.
Report each task to REPORTS/<task-id>_<agent>.md (in the repo branch `unify-bg` folder bridge/REPORTS, or the PC folder
C:\Users\Danny\Desktop\AEGIS_BRIDGE\REPORTS). Round-1 tasks B1-B4 are replaced by these.

Coordinator decision that unblocks you (from the record, D1638): the late thread is a SECOND COPY of the species potential at a lower
scale, i.e. a separate canonical scalar - not the inflaton tau_1. Keep that as the stated postulate [P]; do not test "same field".

## R1 (scalar-quantum agent) — turn the chosen couplings into a boundary
In exact_thread_joint_toy.py, eta = kappa = 0.1 are arbitrary. Scan eta in [-1, 1] and kappa in [-1, 1] (21 x 21) and report the region
where all five Hessian eigenvalues stay positive, and the smallest |coupling| at which one crosses zero. Lock the grid and the pass line
(min eigenvalue > 0) before running. Output: one table + the boundary curve. This converts "stable at 0.1" into "stable up to X".

## R2 (data-lense agent) — put the real negative-space coupling on the stack
Use frozen_extremum(b, ...) with the record's coupled-thread value of b (PREREG_COUPLED_THREAD.md / D1710) and the scan ladder of
PREREG_D2134. For each b report: shifted minimum phi*, curvature there, and the Schur complement sign with the Weave Hessian block.
Control: b -> 0- must return the unshifted rho minimum and curvature 1/4.

## R3 (either) — the line through all three layers, in one table
For each b in R2: [scalar] phi* and V(phi*); [negative space] DM mass change exp(b(phi*-phi_ref)) - 1 and the sign of
rho_DE,eff = rho_phi + rho_c - rho_c,ref at a = 1/3; [quantum] Omega^2 = k^2/a^2 + m^2(phi*) + rho_r/4 for k = 0.1, 1, 10 and whether
the Wronskian check still passes. One row per b. Label every column derived / assumed. This is the connected line Danny asked for.

## R4 — flag for the record
Your finding that the exact-thread line has a second zero at y = 1/2 (modular image of i?) is not in the D-notes. State precisely:
value of f, f', f'' there, and whether it is the same physical point as tau = i under SL(2,Z) for the full two-dimensional modulus.

Standing rules: lock first, run once, deviations before any rerun, honest labels, no fits, no publishing. D1725 and D2134 verdicts stand.
