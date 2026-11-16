# AEGIS update ladder + data streams (plan, 15 Nov 2026; approved by Danny)

## The ladder (equation → map → predictions → Star Mapper)
| Rung | Where | Passes up |
|---|---|---|
| 1 Equation / script | theory/modular/*.py | output file + lock hash |
| 2 Lock + result | field_tests/rules/PREREG_D###, field_tests/results/ | verdict PASS / FAIL / NULL / CORRECTION |
| 3 D-note | theory/pending_docs/D72_D75_weak_spots.md | one tag line: `MAP: node=<id> status=<status> touches=[..]` |
| 4 Theory map | theory/map/map.yaml → Whiteboard | downstream nodes flagged `recheck` |
| 5 Predictions | papers/v3/prediction_sheet.md, tools/tracker, paper caveats | frozen bands untouched; post-hoc marked |
| 6 Star Mapper / Sky Map | ufe-v2/model_current.json (+ "changed since freeze") | live model card |

- Up: `python tools/ladder/ladder.py update` reads new MAP lines, updates map.yaml, flags downstream nodes, writes docs/map/map.json (Whiteboard data) and the model card's change list.
- Down: flagged nodes become the next "Ddl" tick's first job.
- Sideways: Star Mapper discoveries/reviews go to the observing log only. The Star Mapper does not test SERAPIS.
- CI: fail if a new D-note lacks a MAP line, or a node stays `recheck` for more than 5 notes.

## Build order
1. map.yaml seed: done (30 nodes, 5 layers + observing side).
2. tools/ladder/ladder.py + tests: done (CI runs `ladder.py check`).
3. Whiteboard view: done (claude.ai artifact "AEGIS Theory Map", https://claude.ai/artifact/Hwhxvt5avauRxFnPA5n9BT; redraw from docs/map/map.json after big changes).
4. "Ddl" loop starts from flagged nodes.
5. Star Mapper model card shows the "changed since freeze" list: done (ufe-v2/model_current.json, copied to Danny's AEGIS_latest).

## Data streams (from memory; check terms and endpoints before wiring)
| # | Stream | Feeds | Access |
|---|---|---|---|
| 7 | New-measurement watch (arXiv + experiment pages: n_s, r, Σm_ν, DESI/Euclid) → tracker scores the frozen predictions | theory (rung 5) | public. First priority |
| 1 | Rubin alerts via ALeRCE / Fink brokers ("what changed in the sky") | Sky Map layer | public APIs. Second |
| 2 | GraceDB live gravitational-wave alerts (replaces the catalogue-only gravity feed) | mapper | public |
| 4 | Minor Planet Center NEO confirmation page | mapper | public |
| 6 | CHIME/FRB catalogue | Sky Map layer | public |
| 8 | ATLAS/CMS disappearing-track wino limits (monthly) vs the 0.67–0.80 TeV window | theory (wino_window node) | public |
| 3 | Transient Name Server (named supernovae) | Sky Map layer | needs an API key (Danny registers) |
| 5 | Gaia DR4 (2 Dec 2026) | mapper | public; plan in docs/STAR_MAPPER_DR4_PLAN.md |
| — | GCN Kafka (live gamma-ray alerts) | mapper | optional; needs a GCN account. The per-circular JSON feed works now |
Rule: every stream lands as candidates or measurements with its source and time. Nothing is promoted to a "discovery" or "confirmation" automatically.

## Jl learning loop: functions, checks and balances, built like SERAPIS (15 Nov 2026, 22:29)
SERAPIS works because every part has one job, hard checks it must pass, and balances that tie its parts together. The loop is built the same way.

### Functions (each with one job, like V0, E(τ,2), the tilt C, N*)
| ID | Function | SERAPIS analogue | Job |
|---|---|---|---|
| L1 | Observe | data in (Planck, ACT, DESI) | Read LESSONS.md, the map flags, the last 8 D-notes and new data |
| L2 | Select | the vacuum choice (i or ρ) | Pick the side (forward/reverse, alternating) and ONE target |
| L3 | Research | literature inputs (BHK, DKL) | 1–5 searches. Record sources |
| L4 | Create | a new term (SERAPIS-E's 1/E) | Name a new term, or POSTULATE Pn (assumptions, form, falsifier) |
| L5 | Lock | PREREG + sha256 | Commit the rule before computing |
| L6 | Compute | the slow-roll / N* integrator | Short script; results to field_tests/results |
| L7 | Derive | the analytic chain | Full labelled chain to theory/derivations/DERIVATION_LOG.md |
| L8 | Learn | the BHK tilt (a small correction) | 1–2 lessons in LESSONS.md that steer L2 next time |
| L9 | Record | the paper + prediction sheet | D-note + MAP line, ladder update, commit and push, report |
| L10 | Restart | reheating → next epoch | send_later 5 min with the next side, target and queued mirror question |

### Checks (hard gates, like the frozen bands; a failed check blocks L9's "confirmed")
- **K1 Lock-before-compute:** the PREREG commit is older than the results file.
- **K2 Labels:** every derivation step carries [derived]/[literature]/[postulate Pn]/[estimate].
- **K3 Units and arithmetic:** done in code, not prose (aegis-check).
- **K4 Regression:** a new computation reproduces a known earlier point (e.g. D759 C = 0 = D758).
- **K5 Source match:** a fetched source really uses the function we build on (lesson D760).
- **K6 No chase:** fixes only via DEVIATIONS written before a rerun.
- **K7 Map line:** present and valid; postulates get status=assumed.
- **K8 Frozen bands untouched:** post-hoc results never change the frozen predictions.

### Balances (cross-ties, like the bridges B1–B5 and both vacua passing the same bands)
- **β1 Two-way chain:** the forward derivation's output equals the reverse ladder's requirement. CONFIRMED needs both.
- **β2 Mirror rule:** every forward result queues a reverse question, and every reverse term queues a forward prediction.
- **β3 Postulate budget:** at most 2 open postulates. A third forces the next tick to test or retire one (keeps the theory honest, like N* ≤ the bound).
- **β4 Derived vs assumed ratio:** report the map's derived:assumed count each tick, and flag it if assumed rises two ticks running.
- **β5 Cost:** ≤ 5 searches and ≤ 1 locked computation per tick (credits).

### Tick order
L1 → L2 → (L3 → L4 if a wall) → L5 → L6 → L7 → checks K1–K8 → balances β1–β5 → L8 → L9 → L10.
The mechanical checks run with `python tools/loop/jl_check.py` (K1, K2, K7, β3, β4).
