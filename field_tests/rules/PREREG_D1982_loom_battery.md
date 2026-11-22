# PREREG D1982: test battery for the Loom itself, plus the triangulation rotation (Danny 18:44). Locked 22 Nov 2026 ~00:50Z, before building.
## Part 1: the battery (each test has a known answer, fixed now)
**B1 Known-answer lensing (calibration).** The lensing core (refactored out of tools/loom/lensing.py, with output byte-identical to D1981) runs on synthetic 9-layer, 5-knob models with linear margins:
| model | what it is | expected result |
|---|---|---|
| (a) NESTED | layer k responds to x_(k mod 5) + x_(k+1 mod 5), so neighbouring layers share one knob | every non-window transfer BENT at 60°; chain dim ≥ 1; verdict SUPPORTED |
| (b) DIAGONAL | layer k responds only to x_(k mod 5) | every transfer BLOCKED; chain dim 0; verdict DECOUPLED |
| (c) STAR | layers 1–7 and 9 each respond to their own knob; layer 8 responds to all 5 | hub = L8 |
| (d) OPAQUE | as NESTED, but layer 4's margin is constant | L4 reads OPAQUE (rank 0) and both its transfers BLOCKED |
| (e) SAME | every layer responds to x_0 | every transfer PASS (0°); chain dim 1 |
| (f) WINDOWS | NESTED with layers 3 and 9 removed | the transfer 2→4 is computed across the window |

**If any of (a)–(f) fails, D1981's verdict is downgraded to UNCALIBRATED.**

**B2 Rotation invariance (metamorphic test).** Apply a random orthogonal rotation Q to the knob coordinates of the real model (5 seeds). The lens counts, every principal angle (within 1e-6°), the hub and the verdict must be unchanged.
Known non-invariance, stated now: rescaling the knob units (ln vs raw) is **not** a rotation and can change the angles. The split knob is raw and the others are in ln, so the unit choice is a reported convention.

**B3 Determinism.** Two consecutive loomd pulses on unchanged inputs give the same state (lock map, fits, ledger length), and the second is NULL.

**B4 Mutation testing.** A mutant is a deliberately broken copy of the code. Mutants of planner.py and of the lensing core are run against their own tests. **Kill rate ≥ 80 %**. Every surviving mutant is listed, and a test is added only through a new dated lock.

**B5 Checker self-test.** test_check.py reproduces EXPECT (8 cases) and test_planner.py and test_planner_2.py pass (23 cases).

**B6 Anti-gaming replay.** These scenarios fed to the planner raise the named alarm:
- a relabel of NO LOCK → TRUST raises G-T1;
- a new fit raises G-T3;
- killable predictions falling to 3 raises G-T4;
- 7 null pulses without balance gives a STALL, not the endpoint.

**B7 Balancer injection–recovery** (D1976, already locked): rerun only after a model change; reported, not re-scored here.

## Part 2: the triangulation rotation (derived from the model as it stands)
Inputs, fixed now:
- the still-point one-sigma steps (D1978): T ≈ 10 %, S ≈ 3 %, U ≈ 3 %;
- the lensing hub L8 and the opaque L4 (D1981);
- N0's lead (D1979);
- the mission's exploration share, 0.2.

**Axis cycle: 4 pulses, T, S, T, U.** Data are worth most along the loosest direction (Fisher: the gain goes as the step squared, so T is about 10× S or U). Pure Fisher weighting would starve S and U, so the floor is that every axis is visited at least once in every 4 pulses. T gets 2 of 4.

**Every pulse, fixed slots:**
1. **The derive slot** goes to the innermost unlocked layer (L4, opaque, until it locks or N0 holds it).
2. **A hub cross-check on L8**: one bearing, because L8 couples to L2, L5, L6 and L7, so an error anywhere shows up there first.
3. **The axis slot**: three bearings on the pulse's axis:
   - T: wino at the pure-wino lifetime; gluino; Higgs mass.
   - S: n_s; r; N* from reheating.
   - U: the lepton and neutrino rungs; JUNO sin²θ₁₂; the quark window.

**Reading rotation:** every bearing set uses three methods with different failure modes: numeric (R1), probe or data (R2), and literature or hand (R3). R2 alternates between random probes and external data on odd and even pulses, so that no single method's blind spot (for example R2 at kinks, D1981) repeats twice in a row.

**Exploration:** every 5th pulse, the axis slot goes to the loosest *new* direction the still point reports (if any), not to the cycle.

**Success measure, scored after 12 pulses (3 full cycles):** the number of the 9 layers' statuses or fits that changed, per pulse, compared with the round-1–4 baseline (0 per pulse in physics). The rotation is retained if it beats the baseline. It is not tuned before then.
