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
| Speed rungs Spindle/Aion/Zurvan | rotation 1-3 | SPEED-* | R79, R79b | majors fixed (harnesses, wiring, tachyon); see DEVIATIONS | SPEED-*_DEVIATIONS |

## Speed record (speed rung, before/after on the locked test set)
| Tool | Slow path | Before | After | Accuracy kept |
|---|---|---|---|---|
| Spindle | mean-field run (Python RK4) | 4.08 s | 0.109 s DOP853 (37x, median of 3) | 3.9e-10 |
| Spindle | SMA time series | 0.0139 s | 0.0053 s vectorised (2.6x) | 5.6e-16 |
| Spindle | oscillation period (osc_obs) | ~0.7 s | ~0.01 s analytic quadrature (OPTION; failed locked S3 as first written, fixed DEV-2) | 5e-8 vs long-window reference |
| Spindle | Bose-Hubbard sparse Lanczos | - | NOT accepted (can miss the ground state); opt-in above dim 5000 | fails S4 |
| Zurvan | Sigma terms (float64 finite differences) | 65 ms /600 | 4.4 ms exact derivative (15x), WIRED as default (delta_ew method='exact') (more accurate: 1e-17 vs 50-digit check; float64 reference off by up to 6e-5) | Z1 failed as locked, see DEVIATIONS |
| Aion | 3-sigma scan (53k points, Python loops) | 0.40 s | 6.4 ms numpy broadcasting (62x) | 4e-16 |
| Aion | Monte Carlo 1-sigma (20k) | 0.16 s | 14 ms (12x) | 2e-16 |
| Hyperion | J-factor route A (14,400 adaptive quads) | 18.0 s /4 profiles | 0.18 s Chebyshev los table (102x), now the default | 4e-11 |
| CERN+1 | whole test suite | 2.5 s | nothing worth speeding (already fast) | - |
| Lattice Lab, Janus-lt, SERAPIS calc, chem, golden, Kaluza | whole suites | 10.7 s together (slowest test 3.0 s) | nothing worth speeding now | - |
| Chronos | chain solve (matrix exponential, 1,995 solves) | 0.016 s | 0.004 s analytic Bateman (4.4x); browser engine instant | 3e-13 (T1) |

## Next in the rotation (older toolkits, one per loop tick)
Hyperion (astro / BBN / neutron stars) -> CERN+1 (LHC toolkit) -> Lattice Lab -> Janus (astro, lt) -> SERAPIS calc -> chem -> golden.
Each gets: lock a short referee charge, one independent referee round, DEVIATIONS for any fix, rerun its CI tests, record here.
