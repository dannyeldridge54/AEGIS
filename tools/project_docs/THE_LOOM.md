# The Loom: the Weave's research loop, examined as a theory and rebuilt (21 Nov 2026; v2 after the methods referee)
Danny 14:15–14:17: "do the same big weave loop … add the median at the beginning … then researching, reviewing, then postulating and executing … that's the way I want the loop going forward." Then: "we've been building this pattern that's most effective. Examine this with the triangulation, reviewing, referees … look at it like it's the theory … how we can improve it … set that to the weave loop. Call it the loom."

## 1. The loop treated as a theory: what today's record shows
The data set is the 37 notes D1873–D1904 (21 Nov, 11:54–14:17 CT), with 22 locked tests and 46 lock files (including DEVIATIONS). Outcomes: 10 PASS, 5 FAIL, 1 PARTIAL, 7 referee notes, 5 dated corrections (plus withdrawals inside them).

### What worked (keep)
| practice | evidence |
|---|---|
| Lock before compute (PREREG + sha256, pushed first) | The independent referee confirmed 19/19 locks in order. No result was quietly changed. |
| Corrections as dated notes, never silent edits | D1881a, D1881b, D1885a, D1886a, D1894a were all traceable. The referee could follow every change. |
| The median / one-pass scoreboard | It made the true state visible. 16/16 "PASS" became 13 PASS / 3 FAIL once labelled honestly (D1896 → D1898). |
| Research at the decision point | Literature flipped three outcomes: the DKL normalisation (D1881), the brane gauge term (D1900) and real Z₆′ models (D1904). |
| Failing fast and closing families | Corner shielding was closed in two tests (D1873, D1882). Single-sector charges were closed by a theorem (D1874–D1876). |

### What failed (fix)
| failure mode | instance | how it was caught | cost |
|---|---|---|---|
| Self-review misses domain errors | the b′ gauge term missing (D1881a) | the **independent** referee only | the α_s claim stood for about 1 h |
| Numerical artefact taken as a result | the flux-6 degenerate class (D1885) | by accident, during a crash (D1893) | one withdrawal, and it had spread into 3 docs |
| No look-elsewhere accounting | the arrow's ±20 % (D1894) | independent referee | overclaim |
| Weak tests counted as evidence | naturalness bars and bounds counted as PASS | independent referee | 16/16 shown instead of 13/3 |
| Planning values seen before the lock | D1891 and D1902 computed candidates first | declared openly, but selection bias stays | weak evidence |
| Formula carried across frameworks | heterotic b′ used in a brane model (D1881 → D1900) | literature, later | a flip-flop on Δ₃ |
| Conflict with an earlier postulate | the thread modulus is also stabilised by SU(12) (D1902 vs D1812) | self-referee D1903 | an extra postulate U30 |
| Toys too loose to discriminate | 25,088 configurations pass (D1901b) | noted in the note itself | no content |
| Hard-coded numbers in the scoreboard | proton, two-stack, theorem rows | independent referee | traceability |
| Stale or duplicate ticks | 4 stale fired ticks today | manual | credits |

### First Loom result (tick 1, D1907)
The RESTORED flag plus the independent referee withdrew the Δ₃ restoration within one tick, before anything was built on it. That is the intended behaviour.

### Diagnosis
- The loop's integrity layer (locks, dated corrections) is strong.
- Its **epistemic layer** is weak. Three things are missing:
  - triangulation (a second independent route to each claim);
  - chance calibration (how often would this pass by luck?);
  - an independent referee often enough.
- Every MAJOR error today was caught by a fresh-context referee or by literature, never by the same thread that made it.

## 2. Triangulation: the rule the Loom adds
A claim counts as **woven** (evidence) only when **three independent threads** cross it:
1. **Compute**: a locked script whose numbers are read from files, never typed in.
2. **Source**: a primary paper that was opened and quoted, with its framework tagged (heterotic / IIA / IIB / field theory).
3. **Check**: either an independent referee or an alternative method. Examples: a different basis or seed, a different grid, an analytic limit, or a control run on shuffled inputs.

Thread rules, tightened after the methods referee:
- **Check** must use a *different code path or derivation*, or be the independent referee. A reseed, a finer grid or a basis change counts only as a **stability check**, which is required but is not a thread.
- **Source** must be checked *against* the claim, not just used to import a formula. Its framework must match the Weave's, or the mismatch must be flagged.
- A claim that brings back a number withdrawn earlier carries the flag **RESTORED**. Example: D1904's R = −0.023, which D1881b had withdrawn and D1900 brought back by a framework argument. A RESTORED claim needs an independent referee before it can be woven.
- A claim whose content was chosen from a scan carries the flag **POST-SELECTED**, and it cannot be woven on that test alone.

A claim with one or two threads is **loose** and is reported as such. A claim that cannot get thread 2 or 3 is labelled **TRUST** (an explicit input). Danny 14:04: "it may just end up being trust".

## 3. The Loom: tick order (the standing loop from now on)
**Median and triangulation at EVERY step** (Danny 14:30). Every step that produces a number, a choice or a reading gathers **three independent readings**: three sources at RESEARCH, three candidate postulates at POSTULATE, three estimates or code paths at EXECUTE. The step records all three, takes the **median** as the working value and the **spread** as its uncertainty. MEDIAN at step 0 is the same rule applied to the sectors. First used in D1908.

**Triangulated data points (Danny 14:32): "triangulate exactly where it's pointing."** Whenever a tick needs data (a measured value, a literature number, a bound, a parameter), it does not take one number. It takes a **fix**, the way a navigator plots a position from three bearings:
1. **Three bearings.** Three independent readings: different sources, methods or code paths, each with its own uncertainty and framework tag.
2. **The fix.** The point they converge on: the median, with the spread (min–max of the two nearest readings) as the error box.
3. **The pointing.** Where the three agree (overlapping error boxes means a *consensus fix*). Where one disagrees, record which way it points away and why (framework mismatch, regime, older data). Three readings that do not converge give an *open fix*: the number is labelled TRUST and the disagreement is a finding.
4. **The fix line in the D-note:** `FIX <quantity>: readings r1/r2/r3 (sources) → fix = <median> ± <spread>; consensus | open; outlier points <direction> because <reason>`.
5. **Only a consensus fix may enter a lock** as data. An open fix enters only as a range to scan.

Each tick is one pass of the shuttle. Every step is mandatory, and its output is one line in the D-note.

0. **MEDIAN.**
   - Read the live scoreboard (the latest locked weave_derivation run plus the conditional states).
   - Take the sector with the largest |strain| (equilibrium = all sectors balanced). Ties go to whichever has the most dependants.
   - Write: "Median: <sector>, strain <x>, why it is first."
   - **Open the trials ledger here**, before research shapes the options. It is cumulative per sector, so every option ever tried for that sector counts.
   - **Anti-overfit cap:** at most 2 net new postulates per sector before an independent referee reviews that sector.
1. **RESEARCH.**
   - At least one primary source, actually opened.
   - Tag its framework (heterotic / IIA / IIB / FT) and note whether it matches the Weave's framework. A mismatch must be flagged before its formula is used.
2. **REVIEW.**
   - Read the last 5 notes and the postulate table.
   - Run a **conflict scan**: does the target touch any modulus, field or number that an earlier note fixed? List the conflicts, or write "none".
3. **POSTULATE.**
   - Exactly one, labelled P/C/E.
   - State the kill condition.
   - Fill the **trials ledger**: the alternatives considered, and how many.
   - State any values already computed in planning.
4. **EXECUTE.**
   - Lock (PREREG + sha256 + script hash, pushed), then run.
   - **Power check before running:** if the lock's own conditions would pass almost everything (as D1901b did, with 25,088 passes), tighten the test or label it "necessary-condition only" before it runs.
   - **Control:** the null distribution (range, prior, what gets shuffled) is fixed in the PREREG. The chance pass rate p₀ is reported *after* the trials-ledger correction. Below 0.05 it counts as informative; between 0.05 and 0.2 as weak; above 0.2 as uninformative. p₀ is always reported.
   - **Scored on everything else:** each new postulate is also scored on the sectors it does *not* target, and must not raise their strain.
   - Any eigenvalue, basis or random-sample result gets a **stability check** across 3 seeds or bases, because of D1885.
5. **TRIANGULATE AND REFEREE** (merged, following the referee).
   - Name the claim's threads under the §2 rules.
   - Self-check arithmetic and lock order every tick.
   - Run an **independent fresh-context referee** whenever a scoreboard line changes, a claim is promoted to woven, or a claim is RESTORED. In any case run one at least every 4th tick.
   - Corrections go in dated notes.
6. **PROPAGATE** (new). After any withdrawal or correction, grep every doc, JSON and the paper for the old value or claim and fix each one. List every place changed in the note. This step comes from D1885a, which had not reached the median map or centre.json.
7. **RECORD.**
   - Log every stale-tick skip as a line in the D-note, so the queue cannot be reordered silently.
   - D-note, commit, push.
   - If a scoreboard line changed, rerun the scoreboard under a new lock and update the paper section.
   - Send one short message to Danny.
   - Schedule the next tick 3 min after this one ends.
   - Guard against stale ticks: if the fired tick names an item already done, skip to the next item.

## 4. The Loom's own metrics (tracked every 4th tick)
- **Net postulates per sector** (the anti-overfit cap).
- **Woven / loose / TRUST** counts across the scoreboard lines.
- **Evidence-class mix**: data pulls vs bounds vs naturalness vs internal. Only data pulls are evidence of agreement.
- **Trials ledger total**, and the chance-adjusted significance of any headline coincidence.
- **Catch rate**: errors found by the independent referee vs by self-review. If the referee keeps finding MAJORs, the referee cadence rises.
- **Equilibrium**: total strain and the largest strain, from the median step.

## 5. First Loom queue (from the median now)
1. **α_s / Δ₃ (largest strain).** Impose the Z₆-II projections and RR tadpoles on the U29 family. There must be exactly one N = 2 Higgs pair per plane (D1904).
2. **The thread's fifth force.** Check U30 (the second dark torus factor) against Ġ/G and Cassini γ.
3. **The rung-step displacement**, which is 10⁴ larger than the landscape prefers.
4. **g_s < 1.**
5. **Non-thermal leptogenesis.**
6. **Koide δ and v/m_SUSY.** These are labelled TRUST until a second thread exists.

## 6. Methods referee on this design (fresh context, 21 Nov 14:20)
- **§1 spot-checks:** accurate. Two corrections:
  - Only 2 of the 3 FAILs are data FAILs; the pyramid line is internal.
  - D1881a was itself wrong. That makes the case for independent refereeing stronger.
- **Bookkeeping:** "D1896a" was cited by D1897 but never written. It is added now (see D1905).
- **Six improvements, all adopted above:**
  1. Referee on every scoreboard change or promotion.
  2. Null fixed in the PREREG, and p₀ after the trials correction with a 0.05 threshold.
  3. The check thread must use an independent code path.
  4. A propagation step after withdrawals.
  5. Postulates scored on the non-target sectors, with a per-sector cap.
  6. RESTORED and POST-SELECTED flags, plus a power check before running.

## 7. Next: CubeMind built the same way (Danny 14:32, design note)
CubeMind's data retrieval will be designed as a Loom:
- **Every link is its own independent sub-agent.** Each one does a single simplified job: fetch one source, run one code path, read one bound. Each has its own fresh context and does not see the others' answers.
- **They work it together to triangulate.** Each link returns a bearing (value, uncertainty, framework, provenance). A consensus step plots the fix (median, spread, agreement) and flags outliers with the direction they point.
- **Consensus decides.** Only consensus fixes feed CubeMind's derivations, and open fixes are surfaced as TRUST or as findings. A referee link (fresh context) audits the consensus step.
- Engineering items, to be locked when started: the link interface (bearing schema), the consensus rule (median + overlapping error boxes, 2-of-3 minimum), cost caps per link, and a test harness that replays today's D1908 and D1906 fixes to check that CubeMind reproduces them.
