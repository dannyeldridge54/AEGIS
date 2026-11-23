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

## CM-IRIS (animated chart generator), 2026-11-23
Run 1 as locked: I2/I3 pass, I1 fail (LTTB 47.8 px on noisy data), I4 fail (relative metric near zero) -> FAILED AS LOCKED.
Rerun after DEVIATIONS (M4 decimation; DEV-2 range-normalised I4, post-hoc label): I1 max 0.03 px, I2 0 px differ,
I3 prep 25 ms / frame 0.39 ms (5x20k pts), I4 0 -> PASS under deviations. Referee round: pending.

## CM-PAPERS (nuclear paper generator), 2026-11-23
As locked, first run: P1 47/47 printed numbers reproduced by independent engine reruns; P2 5 notes, 0 console errors, all
charts drawn; P3 suite builds in 0.01 s; P4 Limits present -> PASS. After the test, a cosmetic change only (identical-title
charts shown once: fission 3->1, fusion 2->1); test rerun still PASS. Referee round: pending.

## R80 (2026-11-23 10:20 CT): Iris, paper generator, Hyperion fast J-factor — 3 MAJOR
Iris: readout wrong for decreasing x; NaN/null leak into readout. Papers: P1 did not cover literal inputs/constants; t0 omitted.
Hyperion: fast route exceeds 1e-6 for cored profiles with the core edge inside the region; b_mask 0 crash. DEVIATIONS written first.
R80 fixes (after DEVIATIONS): Iris DEV-3 edge tests E1-E5 + I1b (sub-pixel column extent 0.022 px) PASS; locked I4 now FAILS on logy
(3.9e-8) by design: DEV-3 makes the log-axis readout interpolate in log y to match the drawn curve; recorded, not hidden. Papers DEV-1:
73 inputs echoed from call args (P1b), 9 constants read from the engine (P1c), chart labels (P4b), Ac-225 matrix exponential vs 50-digit
analytic Bateman 5.7e-16 (P5) all PASS; untraced-token scan flags only citation years and isotope mass numbers. Hyperion DEV-1: fast path
falls back to route A for b_mask 0 or smooth=False; scope narrowed in docstrings. Referee R80b pending.
R80b (10:22 CT): no MAJOR; 7 MINOR fixed after PREREG_R80b_MINORS_DEVIATIONS (I4 post-hoc label; "" filtered; empty series out of
legend/tooltip; index chart counts 3->1, 2->1; per-note Validation wording; Way-Wigner coefficient recovered from the engine value;
cored profiles auto-fall back: NFW rc 0.1 kpc now 0.0 vs route A). Formula exponents stay typed, labelled as law constants. Round closed.

## FUSION-1 R81-R83 + single rerun (2026-11-23 11:10 CT)
R81 (S1/S7): goalposts G2 and G13 were wrong (mass-number shortcut; 15 vs 15.7 MK); code right; D-He3 coefficients confirmed.
R82 (S2/S3): no synchrotron/line radiation; ITER columns mixed; G5 passed by cancellation. R83 (S4-S6): G10 goalpost a rounded figure;
NIF 8.6 MJ / 2.08 MJ = 4.13; TBR doubling model; wall-area label; dpa via Stork 2014.
Rerun after DEV-1..14: G1, G2 (post-hoc), G3, G4, G7, G9, G10b (post-hoc), G13 (post-hoc) PASS; TBR example 1.051 (R83 value).
G5/G6 (post-hoc ITER 500 MW column) FAIL: P_fus 340 MW, Q 6.8, tau_E 4.82 s, W 301 MJ, P_loss 62 MW (< P_LH 97), f_G 0.98.
Cause found: subtracting ALL radiation (56 MW) from P_loss; ITER's 104 MW P_loss implies only ~46 of 61 MW is counted (core vs edge
radiation convention). Dials find no admissible point (P_loss < P_LH everywhere). Open for the next loop cycle; not hidden.
R85 (cycle 2): 2 MAJOR (Q2 non-discriminating; 51 MW is the 1999 law) -> cycle 2 NULL; loop stops (D2194a).
SPEED-fusion: V1 2e-15, V2 1e-14, V3 same best point (P_net rel 2e-14), V4 goal dials 511 s -> 14.7 s (35x). PASS as locked.
R86 (cycle 3): 1 MAJOR (E3 over Greenwald), 4 MINOR -> fixed (D2195a); SIM-1 PASS.
