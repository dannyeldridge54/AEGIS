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

## Jl learning loop: a mirror of SERAPIS (added 15 Nov 2026, 22:27)
SERAPIS has two mirrored vacua: τ = i (the S-fixed point) and ρ (the ST-fixed point), joined by one modular potential and checked by the same frozen bands. The learning loop copies that shape: two mirrored ladders, one shared potential (the theory map and the lessons file) and one set of frozen checks.

| SERAPIS | Jl loop |
|---|---|
| Vacuum τ = i | **Forward ladder (i-side)**: model assumptions → derive → predictions. Asks "what does SERAPIS say?" |
| Vacuum ρ | **Reverse ladder (ρ-side)**: target or observation → requirement → new term or postulate → source. Asks "what must SERAPIS contain?" |
| Modular potential V(τ) linking the vacua | **Centre / DERIVE**: the full labelled chain must run both ways. Forward output must equal the reverse requirement. |
| Frozen bands (n_s, r, α_s) | **Frozen checks**: locked PREREGs, honest labels, post-hoc models scored only on future data. |
| Modular symmetry Γ2 ≅ S3 (relates the sides) | **Mirror rule**: every forward result spawns a reverse question ("what else could give this?"), and every reverse term spawns a forward prediction ("what else does this predict?"). |
| BHK tilt (small loop correction, C ~ 1e-6) | **Lessons file**: small, accumulated corrections that tilt the next choice of target (theory/derivations/LESSONS.md). |
| Reheating / N* (where one history meets data) | **Report + map update**: the tick's result meets the theory map, the prediction sheet and the Star Mapper. |

Tick order:
1. Read the lessons.
2. Run the side the last tick did NOT run (alternate i → ρ → i …).
3. At a wall: deep research, then create a term, or a postulate Pn if there is no source; lock it and compute it.
4. DERIVE at the centre: write the chain both ways. A mismatch is a correction note, and the side that caused it reruns next tick (through DEVIATIONS, not a chase).
5. Mirror rule: queue the spawned question for the other side.
6. D-note + MAP line, ladder update, commit and push, report.
7. Restart in 5 min.
A result counts as CONFIRMED only when both sides agree at the centre, the way a SERAPIS branch counts only when both vacua pass the same bands.
