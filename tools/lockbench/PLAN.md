# LOCKBENCH improvement plan (17 Nov 2026) — researched against established practice
Prior art checked: provenance tracking (LHCb, arXiv 1910.02863; DataLad/HPC data versioning, arXiv 2505.06558; reproducibility survey arXiv 2402.07530),
blind analysis and preregistration (particle-physics blinding; registered reports), code verification & numerical-error estimation (Roy/Oberkampf V&V:
order-of-accuracy tests, method of manufactured solutions, Richardson/GCI — OSTI 1142223, Roy EACM chapter).
Failure modes from our own logs this week that each item would have caught are given in [brackets].

1. Machine-readable claims (highest value). Each PREREG gets a `claims:` YAML block (quantity, comparator, threshold, scope). LOCKBENCH evaluates it —
   scripts only emit numbers. [J7b numpy-bool verdict bug; hand-coded verdict strings everywhere]
2. Lock linter (runs before a lock can be committed): flags n_params ≥ n_data [L8, D1047]; tolerance tighter than the stated reference spread [D1039,
   D1141]; "A agrees with B" where A and B are different approximations of the same quantity — require one side to be the exact/reference [JMF1, D1161];
   missing per-task wall limit or resume [J7h kmiii, S4e2 cloud timeout].
3. Blind mode: job output goes to a sealed results file; only the claim verdicts (from item 1) print until the D-note step unseals it. Parser/plumbing
   fixes then never require looking at values. [JMF1 D2 — numbers leaked in an error tail before the fix]
4. Provenance stamp on every results file: git commit, lock sha256, code-file hashes, input-data hashes (e.g. Pantheon+ cov), package versions,
   machine (cloud/PC), wall time. Results without a stamp are not citable in a D-note.
5. Verification kit (tools/lockbench/verify): order-of-accuracy test (observed vs formal order), Richardson + Grid Convergence Index for any cutoff/grid
   parameter, two-independent-solver agreement as a required step, manufactured-solution hooks for ODE/eigen solvers. [S4c2 "not converged" → S4c3 Aitken
   was done ad hoc; S4e solver had no MMS check before the 10D comparison]
6. Deviation workflow: `lockbench deviate <lock> "reason"` appends a timestamped, hashed DEV entry; runners refuse a second run of a locked job without one.
7. Ledger outputs: a dashboard artifact (claims, verdicts, precision honesty, open deviations) and a CubeMind export (each lock → an eval item:
   "given this lock and these numbers, what is the verdict?") — the method becomes CubeMind's mirror-check training/eval data.
8. One environment: pinned requirements for cloud + PC with a start-up self-test (as the CubeMind grader does). [PC/cloud package drift risk]
Build order: 1 + 2 (they prevent most of this week's errors), then 4 + 3, then 5, then 6–8.
