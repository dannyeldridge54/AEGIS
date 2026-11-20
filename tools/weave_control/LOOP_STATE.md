# Weave Control build loop — state (read this first every tick)
Danny 20 Nov 2026 04:39 CT: "set up the loop like this: research, postulate, engineer, review, engineer, referee, review, etc., and loop it 3 minutes."
Plan: tools/WEAVE_CONTROL_PLAN.md (51 Weave items, per-tool "better than the specialists", wiring table, build order).

## The cycle (one stage per 3-minute tick, then the next item starts again at R)
| stage | what the tick does | output |
|---|---|---|
| R  research   | 1–2 searches on the item (data, competitor gaps, latest numbers); check our D-notes first | notes in this file |
| P  postulate  | state what the item should do and the pass rule BEFORE building (for physics: lock a PREREG first) | "Postulate:" line below |
| E1 engineer   | build it: code + test | commit |
| V1 review     | aegis-check: units, signs, arithmetic in code, like-with-like, labels (P/F/G), UI at desktop + phone | findings list |
| E2 engineer   | fix every V1 finding | commit |
| F  referee    | hostile read: would an expert in that field accept it? missing standard features, wrong conventions, overclaims; compare with the leading tool | referee list (fixes go to the next E) |
| V2 review     | confirm referee points handled or recorded as open, run all tests, commit + push, report 2–4 lines to Danny | DONE row |

## Item queue (build order from the plan)
1. W1 engine: one parameter set → levels (Inflation A, Flavour B, BBN D, Late universe C, Colliders C, Galaxy & dark matter C, Stars D, Sky E), each with inputs, outputs, data + sources, pulls, status
2. W2 links: dark sector ΔN_eff → BBN; wino mass → gamma line (verify the σv mass scaling against D1322 first); J-factor region → Mapper; b_A → z† and G_eff
3. W3 server + control panel UI (a panel per level with its own chart; scorecard across categories; light/dark; phone)
4. W4 Flavour level: Koide Q, Brannen δ, TM1 δ_CP band vs NuFIT
5. W5 Hyperion: rate-uncertainty Monte Carlo on Y_p, D/H
6. W6 Janus: N* ± band from reheating; B1/B2 bridges on every run
7. W7 Mapper: science overlays (DESI/Euclid footprints, GC gamma-line region) + tonight ranked by Weave-test value
8. W8 CERN+1: simplified likelihood (R5) + triglavon/cassion reach
Then the older toolkit queue (M1c, sexagesimal input, J2a, M4, R6, M5, H1d, M1e, M1g, CLI --prov, map data items 2–8).

## Current position
Item W1 · next stage: E1 (R and P were done in the plan: tools/WEAVE_CONTROL_PLAN.md Parts 1–4).
Postulate W1: every level returns {category, inputs, outputs, data[{name,value,sigma|limit,source}], pulls, status ∈ pass/tension/fail/open}; nothing typed in by hand except measured data with a source; fits labelled F; a test per level.
Notes: wino gamma-line σv — the D1322 formula is written for M = 1 TeV; the M-scaling must be checked against sommerfeld_nlo before it is shown (flagged 04:38).

## Done log
