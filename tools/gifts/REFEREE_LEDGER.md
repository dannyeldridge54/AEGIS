# Referee ledger: every tool, every ping-pong round

A round = an independent referee (person or separate agent that did not build the tool) attacks the locked plan, the code and
the claims; the builder fixes only through a DEVIATIONS note written before any rerun; repeat until a round returns NULL.
`python tools/gifts/pingpong_suite.py` re-runs every locked test any time (also in CI, job `gifts`).

| Tool | For | Lock | Rounds | Verdict | Deviations |
|---|---|---|---|---|---|
| Spindle | Y. Liu (OSU) | D2183-D2185 | R71, R72 | NULL after fixes | PREREG_D2183_*_DEVIATIONS, D2185 DEV-1 |
| Zurvan | H. Baer (OU) | D2187 | R75, R75b | NULL | DEV-1..13 |
| Aion | K. S. Babu (OSU) | D2188 | R76, R76b | NULL | DEV-1..9 (DEV-8 Lantern kept by author) |
| Chronos | Nuclear rung (OU/OSU) | D2189 + A1-A3 | R77, R78, R78b | NULL | DEV-1..16 |

## Speed record (speed rung, before/after on the locked test set)
| Tool | Slow path | Before | After | Accuracy kept |
|---|---|---|---|---|
| Spindle | mean-field run (Python RK4) | 3.81 s | 0.108 s DOP853 (35x) | 3.9e-10 |
| Spindle | SMA time series | 0.0139 s | 0.0053 s vectorised (2.6x) | 5.6e-16 |
| Spindle | oscillation period (osc_obs) | ~0.7 s | ~0.01 s analytic quadrature (option) | 2e-8 where it oscillates |
| Spindle | Bose-Hubbard sparse Lanczos | - | NOT accepted (misses degenerate levels) | fails S4 |
| Chronos | chain solve (matrix exponential, 1,995 solves) | 0.016 s | 0.004 s analytic Bateman (4.4x); browser engine instant | 3e-13 (T1) |

## Next in the rotation (older toolkits, one per loop tick)
Hyperion (astro / BBN / neutron stars) -> CERN+1 (LHC toolkit) -> Lattice Lab -> Janus (astro, lt) -> SERAPIS calc -> chem -> golden.
Each gets: lock a short referee charge, one independent referee round, DEVIATIONS for any fix, rerun its CI tests, record here.
