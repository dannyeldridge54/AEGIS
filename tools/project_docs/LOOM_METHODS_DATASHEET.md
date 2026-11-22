# Loom methods data sheet: every way we optimised data collection and checking (kept for CubeMind)
Compiled 21 Nov 2026, 17:55 CT, from today's record (D1873–D1971). **Adopted as the Loom's current method (Danny 17:55).** Every round runs through layers A to G in order. Danny 17:51: "put them all on one thing … we're going to implement that into CubeMind later."

Each row gives:
- the method;
- what it does;
- where it lives (file);
- the evidence from today (what it caught, or what went wrong without it);
- how CubeMind should use it.

Status:
- **T**: tested and catching real errors.
- **U**: in use, not yet tested on its own.
- **L**: a lesson (a practice that went wrong and was fixed).

## A. Integrity layer: the record cannot be quietly changed
| # | method | what it does | where | evidence today | status | CubeMind use |
|---|---|---|---|---|---|---|
| A1 | Lock before compute | Fix the prediction, threshold and null in a PREREG with a sha256, pushed **before** running | field_tests/rules/PREREG_* | Every referee confirmed the locks came first (D1897, D1927, D1935, D1942, D1948) | T | Every retrieval or test job writes its lock before fetching or computing |
| A2 | DEVIATIONS before a rerun | Any fix is written down first; one rerun only; no rerunning to chase a result | *_DEVIATIONS.md | Caught D1926 (Fourier ×2), D1929 (baseline), D1937 (bracket), D1946 (64π) | T | A job that fails validation may rerun only after logging the deviation |
| A3 | Dated corrections, never silent edits | Wrong claims get a correction note (D###a) | D-notes | More than 15 corrections today, all traceable | T | Append-only log; corrections reference the original |
| A4 | Never loosen a tolerance | Thresholds stay as locked | locks | D1925's knife-edge result stayed NONE and was not rescued | T | Threshold drift is blocked by the lock hash |
| A5 | Propagate after a withdrawal | Grep every document for the old value and fix each place | Loom step 6 | The U29 and arrow withdrawals reached the paper and the docs | U | Dependency graph: a withdrawn value flags every consumer |
| A6 | Variable registry | One meaning per symbol (ε ≠ u, frozen U, h²¹ = 1) | theory/loom_registry.json | Born from the ε/u mix-up (D1894b) | U | A typed schema for every quantity |

## B. Triangulation layer: never trust a single reading
| # | method | what it does | where | evidence today | status | CubeMind use |
|---|---|---|---|---|---|---|
| B1 | Three-point fix | Three independent readings, then median ± spread, consensus vs open fix | THE_LOOM rule 6 | Wino bound 660 vs ~700 GeV (D1947) | T | Every retrieved number needs three bearings |
| B2 | Pre-registered search and one extraction rule | Fixed query, all qualifying hits, symmetric extraction | rule 6a–6e | Referee D1909 | U | The retrieval agent logs the query and the inclusion rule |
| B3 | Iterated triangulation | Re-triangulate around the centre | rule 6g | Ring 0 (D1932) | U | — |
| B4 | **Seven nulls in a row** | Repeat until 7 rounds change nothing | rule 6h, tools/loom/triangulate.py | **L:** vacuous for deterministic bisection (D1935). It counts only for multi-reader or stochastic readings | L | Apply it to stochastic retrieval or ensembles only |
| B5 | Mirror-Loom posterior | At least 5 bearings, log-likelihood mixture, FRAGILE flag | rule 6f | Adopted D1914 | U | For contested numbers |
| B6 | Median first | Start from the sector with the largest strain | Loom step 0 | — | U | A priority queue |
| B7 | **Independence check (C1)** | Readings that move together exactly under perturbation are one reading | tools/loom/check.py | Caught the D1941 m_φ duplicate | **T** | Dedupe sources that are copies of one origin |

## C. Guard layer: catch errors automatically before a verdict
| # | method | what it does | where | evidence today | status | CubeMind use |
|---|---|---|---|---|---|---|
| C1 | **Power check (C2)** | Perturb the inputs; if the verdict never flips, the test is "structural" | check.py | Caught D1938's seam test (no power) | **T** | Reject tests that cannot fail |
| C2 | **Validation gate (C3)** | Code must reproduce a known reference value before it is used | check.py | Caught D1926 run 1 (8.950 vs 8.893) | **T** | Every tool runs a canary computation first |
| C3 | **Numerology guard (C4)** | The chance that some simple candidate matches, using the target's real uncertainty | check.py | 3/4 match: 20–50 %, not the 2 % claimed (D1948) | **T** | Coincidence detector |
| C4 | **Claim lint (C5)** | Flags overclaim words without a powered test | check.py | Caught "strongest pointing" (D1931) | **T** | Reports are linted before they are shown |
| C5 | **Four corners (C6)** | Forward, reverse, early and late readings must agree | check.py | n_s agrees; α_s is missing two corners | **T** | Each claim is checked from four sides |
| C6 | **Formula benchmarks (C7)** | Each formula reproduces a textbook number before use | check.py BENCH | Caught D1946's 128π vs 64π | **T** | A benchmark library per formula. **Limit:** catches an error only if a benchmark exists |
| C7 | Self-test of the checks | The checks are run on known past mistakes | tools/loom/test_check.py | All of today's mistakes were caught (D1949) | **T** | Regression suite for the checker |
| C8 | Honest labels | FIT / TRUST / PHEN / CONDITIONAL / INDETERMINATE / NO-POWER, kept separate from PASS | D-notes, verdict files | Prevents counting fits as predictions (D1942, D1970) | U | Every output carries an evidence class |
| C9 | Trials ledger and anti-overfit cap | Count every option tried; at most 2 new postulates per sector before a referee | field_tests/loom/trials_*.md | Flavour went over the cap, so a referee was required (D1928) | U | Look-elsewhere accounting |

## D. Direction layer: every result points somewhere
| # | method | what it does | where | evidence today | status | CubeMind use |
|---|---|---|---|---|---|---|
| D1 | **Compass fingerprints** | Each measurement carries a direction (↑/↓/●/◔/!/○), headroom, the knobs it pulls, and a field tag | tools/loom/compass.py → WEAVE_COMPASS.md | 24+ fingerprints | U | Every datum is a vector, not a pass/fail |
| D2 | Three fields plus seams | Split S/T/U and tag the interfaces | UFE v4 §7 | Every open failure sits on S–T | U | Tag each datum by subsystem |
| D3 | Central equation knob engine | O(K_S, K_T, K_U), Jacobian, targeting | tools/weave_knobs.py | **L:** a rank-1 Jacobian is a property of the engine, not physics (D1942) | L | Sensitivity map, labelled by construction |
| D4 | Field map | What each attempted fix did to every sector | tools/loom/field_map.py | **L:** the entries are hand judgments and must be labelled (D1942) | L | — |
| D5 | **Knock-on ledger** | Every adjustment: what it fixed and **exactly what it disturbed** | field_tests/loom/knockon_ledger.json | 16 entries: 8 moved strain, 3 spent predictivity, 4 errors | U | Side-effect log per action |
| D6 | Pattern review | All fingerprints and the ledger reviewed together; 3 weightings, then the median | tools/loom/review.py → WEAVE_REVIEW.md | Found the gravitino as the largest hub (4 of 8) | U | Periodic global synthesis |
| D7 | Pulse | Every flag triangulated together, coupled, re-read, repeated | tools/loom/pulse.py | **L:** a maximin optimiser output is not evidence (D1948) | L | Joint optimisation, labelled as such |
| D8 | **Still-point lens** (Danny 18:12–18:13) | Find the best-balance point on the three tandem axes. Classify the directions: **inward** (stiff, restoring) vs **outward** (loose, free). Then view Δχ² at 36 angles in every plane (the 360° view) | tools/loom/still_point.py (D1978) | All three axes restoring: U and S stiff (3 %), T loosest (10 %); α_s needs a 4th axis | T | Every retrieval round starts at the still point |
| D9 | **Mine the loose directions** (Fisher targeting) | New data are worth most along the **loosest** direction; along stiff ones they add little. Leftover tension at the still point signals a **missing axis**, not a knob to absorb it | uses D8 | Today the loosest axis is T (m₃/₂): wino limit at the pure-wino lifetime, gluino, Higgs mass | U | Rank fetch jobs by the information gain per direction |
| D10 | **Three tandem axes + bounds as data** | Collapse many knobs into S/T/U and count the limits as data, so dof ≥ 3 | tools/loom/method_tests_3axis.py (D1976) | False balance 52 % → 14 %; the method can now FAIL, and it flags α_s | **T** | Keep knobs ≤ data − 3; every new knob needs ≥ 2 new data |
| D11 | **Method tests every model change** | Injection–recovery (≥ 0.9), null false-balance (≤ 0.2), hold-out, dof | tools/loom/method_tests*.py (D1974, D1976) | Showed that balance with dof 0 was meaningless | **T** | The regression suite for the balancer itself |

## E. Coverage layer: test everything a physicist would ask
| # | method | what it does | where | evidence today | status | CubeMind use |
|---|---|---|---|---|---|---|
| E1 | Test battery | About 78 tests from every field, tagged by field and by RUN / FUT / NEED / DONE | WEAVE_TEST_BATTERY.md | Found the "you missed this" items (wino lines, BBN, moduli) | U | Checklist generator per domain |
| E2 | Test plan with six irrefutability gates | Pre-registered, reproducible, triangulated, refereed, falsifiable, honest count | WEAVE_TEST_PLAN.md | — | U | A publication-readiness gate |
| E3 | Kill-condition per term | Each term names the observation that would kill it | the test plan | — | U | Falsifiability field per claim |

## F. Agent layer: independent eyes and parallel work
| # | method | what it does | where | evidence today | status | CubeMind use |
|---|---|---|---|---|---|---|
| F1 | **Independent heterogeneous referee** | A fresh-context agent on a different model reviews each block | every ≤ 4 ticks, now every 2nd round | Caught **every** MAJOR error today | **T** | Mandatory reviewer link |
| F2 | Adversarial referee | Tries to rescue the model first, then judges | D1923 | Narrowed the quark blocker | T | Red-team link |
| F3 | **Node agents** | One read-only agent per node of the equation, reporting in a fixed JSON schema | WEAVE_NODE_CHARTER.md | 9 nodes; found shared bottlenecks (U₃, m₃/₂ tuning, fits counted as passes) | T | **The CubeMind pattern: one sub-agent per link** |
| F4 | Balance board and endpoint | Merge the node reports, check, choose moves that do not strain other nodes | WEAVE_BALANCE_BOARD.md | 0/9 balanced, stated honestly | U | Consensus dashboard |
| F5 | **Anti-gaming guards G-T1–G-T6** | Relabelling is not progress; the TRUST/FIT count may not rise; killable predictions may not fall | the charter | Closed the "relabel everything TRUST" loophole (D1971) | T | Goal-hacking guard |

## G. Cadence and cost
| # | method | what it does | evidence | status |
|---|---|---|---|---|
| G1 | Fixed tick loop with scheduled wake-ups | Self-scheduling loop | **L:** scheduling the next tick last missed the reschedule twice. Now the next tick is scheduled **first** | L |
| G2 | Three workstreams at once | More throughput | **L:** the error rate rose (D1948 found 3 MAJORs) | L |
| G3 | Slower cadence (about 12 min), one main item plus one battery item | Fewer errors per result | Adopted 17:44 | U |
| G4 | Re-spawn only the nodes whose inputs changed | Keeps cost down | Adopted 17:55 | U |
| G5 | Idempotent ticks | A stale or duplicate tick is skipped and logged | Many stale ticks today | T |
| G6 | Docs updated every few ticks, standing rules in one file | Less churn | Adopted 17:44 | U |

## H. The CubeMind design (from the 14:32 note plus today)
- **One independent sub-agent per link.** Each does one simple job: fetch one source, run one code path, or read one bound. It works in its own context, blind to the others.
- **Each link returns a bearing:** {value, uncertainty, framework tag, provenance, exact quote, locator}.
- **A non-model step verifies the bearing:** it fetches the source and string-matches the quote and the number. A bearing that fails is dropped.
- **The consensus step:** median, overlapping error boxes, at least 2 of 3 agreeing. Outliers are flagged with the direction they point.
- **Then the guard layer:** C1–C7 run on every consensus result.
- **Then the direction layer:** a compass fingerprint plus a knock-on ledger entry.
- **A referee link** with fresh context audits every consensus. The goal guards (F5) stop progress from being faked by relabelling.
- **Test harness:** replay today's real mistakes (C7) and known-wrong cases (the D1907, D1931 and D1946 errors) as blind cases. CubeMind must catch them.

## What worked best today (ranked by errors caught; updated 18:13)
1. The independent referee (F1).
2. The validation gates and DEVIATIONS (A2, C2).
3. The automatic checks C1–C7 (section C).
4. The lock before compute (A1).
5. The node agents (F3).
6. **Three tandem axes + bounds as data (D10)**: the single change that gave the method power. Plus the still-point lens (D8–D9) to decide where to mine next.

**Weakest:** hand-entered arrows and judgments (D3, D4), and raw speed (G2).

## Per-round checklist (the current method in one pass)
1. **Schedule the next round first** (G1).
2. **Read the board, the compass and the ledger.** Pick the moves with the highest information gain (B6, D6).
3. **For each move:**
   - lock it (A1);
   - gather three independent, tagged readings (B1, B2, B7);
   - run check.py C1–C7: independence, power, validation, numerology, lint, four corners, benchmarks;
   - then run it;
   - if a fix is needed, write the DEVIATIONS before the one rerun (A2).
4. **Label** each result PASS, FIT, TRUST, PHEN, CONDITIONAL, INDETERMINATE or NO-POWER (C8). Count trials (C9).
5. **Record** the fingerprint in the compass (D1) and the knock-on in the ledger (D5). Run review.py (D6). Update the battery row (E1).
6. **Node round:** re-spawn only the nodes whose inputs changed (F3, G4). Merge them into the board (F4) and apply guards G-T1 to G-T6 (F5).
7. **Referee** every second round, plus any time a verdict changes (F1).
8. **Write** the D-note, with TRIANGULATE:, COMPASS: and REVIEW: lines. Correct earlier claims with dated notes (A3) and propagate the change (A5). Commit and push. Send one short message.
