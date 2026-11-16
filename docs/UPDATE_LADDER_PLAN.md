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
2. tools/ladder/ladder.py + tests.
3. Whiteboard view (from docs/map/map.json).
4. "Ddl" loop starts from flagged nodes.
5. Star Mapper model card shows the "changed since freeze" list (copy to Danny's AEGIS_latest).

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
