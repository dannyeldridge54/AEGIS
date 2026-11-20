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
Item W1 · next stage: E2 engineer (fix V1 findings below). V1 done 04:45 CT.
Postulate W1: every level returns {category, inputs, outputs, data[{name,value,sigma|limit,source}], pulls, status ∈ pass/tension/fail/open}; nothing typed in by hand except measured data with a source; fits labelled F; a test per level.
Notes: wino gamma-line σv — checked: the D1322 '/1e6' is M² in GeV² at 1 TeV, so π α²/M² is the general tree form; the M dependence of the Sommerfeld factor comes from wino_s_nlo itself. At 1 TeV the engine reproduces 1.42e-26 (same formula as the smoke test).
E1 results (defaults): inflation pass (n_s 0.9706, r 5.4e-4); flavour pass (Koide Q 0.6666645 ± 5.1e-6, −0.4σ; Brannen δ 0.2222248 vs 2/9 = 0.2222222); BBN tension (D/H −2.6σ vs Cooke 2018); late tension (thread −2.6/−8.1/−3.4, coupling ~0); colliders pass at 1 TeV (ATLAS 670); galaxy open (f²σv 2.2–6.0e-28 at 1 TeV vs the 2.3e-28 used in D1322: borderline, needs the limit curve); stars pass (SLy 2.05 vs J0740 2.08 ± 0.07); sky open.
For V1 to check: (1) bridge B1 = −2.0e-3 here, not the −0.9e-4 of the twin-ladder notes (those were for an earlier model): do not show the old tolerance; (2) late-level 'd_coupled' is the guard ceiling min(coupled, thread), label it '≤'; (3) stars pass rule uses 2σ below J0740: state it; (4) runtime 5 s per run (galaxy J-factor + Sommerfeld): cache for the UI.

V1 findings (W1 engine), all to fix in E2:
1. DARK_SECTORS values were not sourced correctly. The D-notes say: minimal dark sector with equal sharing ΔN_eff = 0.21 (D1646, estimate); with the P-brane split (C5, D1671) the inflaton heats our side only, ΔN_eff ≈ 0 (bound ≤ 0.086, register C5); full mirror with equal sharing ΔN_eff = 7.4 (D1646, ruled out); mirror at its viability bound 0.3 (D1648). The engine had 'mirror 0.086', which matches none of these. Replace the table with these four, each with its D-note.
2. Bridge B1 = −2.0e-3 at the full SERAPIS point. The twin-ladder target (−0.9e-4, tol 1.2e-4) was set for an earlier model: show B1/B2 as numbers, with no pass/fail, until a new lock sets them.
3. Late level: 'd_coupled' is the nested-guard ceiling min(coupled, thread); rename it to 'd_coupled_at_most' and label it. Its status was hard-coded 'tension': derive it instead (pass if the thread beats ΛCDM on all 3 sets, plus the label 'trails w0wa (−9/−20/−15, CAMB)').
4. Stars: the pass rule (M_max ≥ 2.08 − 2σ = 1.94) must be in the labels.
5. Flavour: the Brannen δ is chosen from the symmetric forms (δ, 2π/3 − δ, any order) as the one nearest 2/9. That is a domain choice, not a fit, but it must be stated, along with the value of the other forms.
6. Galaxy: no status rule. Keep 'open', but add a CONSERVATIVE comparison at 1 TeV only (the single stored limit), labelled as such.
7. Speed: 5 s per run, mostly the J-factor + Sommerfeld. Cache by (halo, rho_sun) and (M) with functools.lru_cache.
8. Errors are caught per level (good), but the error text should also go to a 'error' field so the UI can show it plainly.

## Done log
- 04:45 CT W1/V1 review: 8 findings (above)
- 04:43 CT W1/E1 engine.py + tests (6 pass)
