# The Loom v3: 25 methods ranked by today's record, then woven together (Danny 15:04, 21 Nov 2026)
Danny: "research online … ways for improving data collection, data mining, target acquisition … a list of 25 … the best results, the largest percentage … then we weave them together."

## How they were ranked
Today's 19 recorded errors (D1873–D1920) are the data. Each method is scored by the share of those errors it would have caught.
- The mapping is my retro-judgement, one line per error, so it can be disputed and audited: field_tests/loom/method_ranking.py, output in method_ranking.txt.
- The percentages are retrospective and small-sample (n = 19). They rank priorities; they are not efficiency measurements.
- Methods that prevent errors (locks) or save effort (targeting) score 0 % here by construction, and are kept for those reasons.

## The 25, ranked
| # | method | share of today's errors | source / note |
|---|---|---|---|
| 1 | Independent heterogeneous referee on every scoreboard change | 78.9 % | today's record; heterogeneity: arXiv:2502.08788 |
| 2 | Framework-applicability gate (heterotic / IIA / IIB / FT tag; mismatch justified before use) | 26.3 % | D1881 → D1907 |
| 3 | Forking-paths ledger (every analysis choice and alternative; trials-corrected p) | 26.3 % | look-elsewhere practice |
| 4 | Kill-first red team (one step trying to break a postulate before testing it) | 26.3 % | D1902, D1906b, D1917a |
| 5 | Symbol and convention registry (theory/loom_registry.json) | 21.1 % | D1894b, D1906a |
| 6 | Multiverse / sensitivity analysis over all allowed choices | 21.1 % | D1908a |
| 7 | Constraint graph of fixed quantities and postulates (automatic conflict scan) | 21.1 % | D1903, D1917a |
| 8 | Blind analysis / hidden answer: fix the method before seeing the verdict number | 21.1 % | Klein–Roodman, physics/0312102 |
| 9 | Null / control runs through the same test | 21.1 % | D1901b, D1918a |
| 10 | Power / invariance check before any test | 15.8 % | D1918a |
| 11 | Single source of truth for numbers (values file; no typed numbers) | 15.8 % | D1896, D1894b |
| 12 | Analytic-limit regression tests | 15.8 % | D1906a |
| 13 | Reproduce a published model first (calibrate on a known answer) | 15.8 % | D1915 worked |
| 14 | Fit-vs-derive label enforced (count free parameters vs constraints) | 15.8 % | D1917a |
| 15 | Adversarial collaboration (a pair agent argues the opposite) | 15.8 % | — |
| 16 | Systematic-review protocol (search string, inclusion criteria, all hits) | 10.5 % | Loom 6a |
| 17 | Meta-analysis with heterogeneity statistics and clusters (Mirror-Loom) | 10.5 % | D1914 |
| 18 | Propagation step after every withdrawal | 10.5 % | Loom step 6 |
| 19 | Stability check (seeds, bases, grids) | 5.3 % | D1885 |
| 20 | Mechanical quote-and-number verification | 5.3 % | CubeMind E2 |
| 21 | Idempotent ticks keyed to the next D-number | 5.3 % | stale ticks |
| 22 | Sequential / iterated design | 5.3 % | Loom 6g |
| 23 | Delphi-style structured consensus (anonymous rounds, report spread) | 5.3 % | — |
| 24 | Expected-information-gain target selection | 0 % (efficiency) | arXiv:2302.14545 |
| 25 | Pre-registration + sha256 locks | 0 % (prevention, already in use) | Loom 4 |

- The top 8 together cover 16 of the 19 errors (84 %).
- Adding #9 (null runs), #11 (single source of truth) and #21 (idempotent ticks) covers **19 of 19**.
- Caveat (arXiv:2502.08788): multi-agent *debate* often fails to beat simple self-consistency unless the agents are **heterogeneous**. So the referee (#1) must differ from the author in prompt, framing and, where possible, model. A fresh context alone is not independence.

## The weave: Loom v3 tick (five layers, the 25 methods placed where they act)
**0. TARGET** (acquisition)
- MEDIAN: the most-strained sector.
- Among the top 3 candidates, pick by **expected information gain** (#24): the test whose possible outcomes would most change the scoreboard. A cheap proxy: P(pass) × P(fail) × the number of lines that depend on it.
- Open the forking-paths ledger (#3).

**1. GATHER** (data collection)
- Systematic-review search (#16) with framework tags (#2).
- Fixes: 3-point by default, Mirror-Loom posterior (#17) near a bar or for a shared quantity.
- Mechanical quote check (#20).
- Iterated triangulation (#22).

**2. GUARD** (before any compute)
- Registry check: every symbol used is in loom_registry.json (#5).
- Constraint-graph conflict scan (#7).
- **Kill-first** red-team step (#4).
- Fit-vs-derive count (#14).

**3. TEST** (execute)
- Lock (#25) with a **blinded verdict** (#8): the script prints the verdict only after the method is frozen. Thresholds and nulls go in the PREREG.
- Power and null runs (#9, #10).
- Multiverse over the allowed choices (#6).
- Stability (#19).
- Analytic limits (#12).
- When code is new, reproduce a published case first (#13).

**4. JUDGE** (synthesis)
- Triangulate threads.
- A **heterogeneous** independent referee (#1) on every scoreboard change, promotion, RESTORED claim, and at least every 4th tick.
- An adversarial-collaboration agent (#15) for any claim that is about to be woven.
- Delphi-style spread reporting when referees disagree (#23).

**5. KEEP** (bookkeeping)
- Single source of truth for numbers (#11).
- Propagate after every withdrawal (#18).
- Idempotent tick keyed to the D-number (#21).
- Record, then schedule the next tick.

## What changes from v2 (in effect from the next tick)
New this tick:
- target selection by information gain;
- the registry (seeded now with the error-prone symbols: ε vs u, β vs α_DEF, b′ vs brane b, the frozen-U rule, g_s);
- a constraint-graph scan;
- a kill-first step;
- a fit-vs-derive count;
- blinded verdict printing;
- null runs;
- referee heterogeneity;
- adversarial collaboration before weaving.

Deferred engineering (each its own tick):
- a values file that scripts and docs read;
- an automated constraint graph;
- an automated mechanical quote check (shared with CubeMind E2).

Sources: [Klein & Roodman, Blind Analysis in Particle Physics](https://ar5iv.labs.arxiv.org/html/physics/0312102); [Rainforth et al., Modern Bayesian Experimental Design](https://ar5iv.labs.arxiv.org/html/2302.14545); [Stop Overvaluing Multi-Agent Debate](https://arxiv.org/html/2502.08788v3); [Du et al., Multiagent Debate](https://arxiv.org/pdf/2305.14325).

### Rule 6h — triangulate to convergence (Danny 16:04, standing; supersedes "re-triangulate once")
This applies every time data is mined, a target is chased, or the loop steps onto a new rung.
1. **Three vectors.** Take three independent readings of the same target, from a different method, source or parameter path. Quick-calculate each.
2. **Centre.** The centre is the median and the spread is max − min.
3. **Re-triangulate around the centre.** Take three new readings inside the narrowed bracket, or refine each reading's inputs at the centre (a self-consistent fixed point). Repeat.
4. **Stop: 7 nulls in a row** (Danny 16:05). A round is *null* when the centre moves by less than the resolution AND the spread shrinks by less than 10 %. Keep triangulating until 7 consecutive rounds are null, then move on. The spread that remains is the **systematic floor**; report it rather than hide it.
4b. **The pulse.** At the start of each sector, first read where every existing result points (the compass). Then triangulate the target from there.
5. **Known end result.** If the end result is already known (data, or the median), the question becomes how to get there. Triangulate the *path*: which inputs move the centre onto the target, and by how much.
6. **Order.** Work from the middle outwards. The median sector comes first, then the shared quantities, then the outer sectors.
7. **Record.** Every D-note carries a `TRIANGULATE:` line: the three readings, the centre ± spread for each round, the number of rounds, the floor, and the distance to the target.
8. **Code.** tools/loom/triangulate.py is the reusable helper.

### Rule 6i — mark every knock-on, then review all the arrows (Danny 17:17)
1. Every adjustment gets a row in field_tests/loom/knockon_ledger.json: what it fixed and **exactly what it disturbed**.
2. Every derivation or test result is fingerprinted with a direction in the compass.
3. **At every result,** run tools/loom/review.py. It reviews *all* the pointed fingerprints and the whole knock-on ledger together, finds the pattern, and triangulates where they all point (three weightings, then the median).
4. Then pulse again.
