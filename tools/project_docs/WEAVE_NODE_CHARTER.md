# The Weave node charter: one agent per node, all working toward balance (Danny 17:46, 21 Nov 2026)
Every node of the unified equation gets its own agent. Each agent:
- reads its node's data and fingerprints;
- reports exactly what the node is doing;
- proposes one move toward balance;
- predicts the knock-on that move would have on the other nodes.

A coordinator merges the reports into the **balance board** (WEAVE_BALANCE_BOARD.md). The checks run on it (tools/loom/check.py C1–C7, tools/loom/review.py), and then an independent referee reviews it.

All earlier steps stay in force: lock before computing; the four-corner checks; triangulation; the compass; the knock-on ledger; review; and the referee.

## The endpoint: balance (the final equation)
Balance is not "every number matches". It is reached when **all** of the following hold:
1. **Every node is BALANCED or TRUST.**
   - BALANCED: all its tests pass with margin, after the checks (C1–C7) and with honest error bars.
   - TRUST: an explicit input with no derivation, listed openly.
   - No node is STRAINED.
2. **The knock-on ledger is quiet.** For 7 rounds in a row, no move on any node creates a new strain on another node.
3. **The four corners agree** for every shared quantity: forward (theory → data), reverse (data → input), early-universe and late-universe readings, within their errors.
4. **No term is a fit pretending to be a prediction.** Every fit is labelled FIT and counted. The final count of predictions, fits and TRUST inputs is stated.
5. **An independent referee signs off** on the whole board.

**The honest scoring of the final equation:** the number of real predictions that survived tests which could have killed them, against the number of fits and TRUST inputs.

## The nodes
Sources for every node: theory/pending_docs/D72_D75_weak_spots.md (the D-notes), field_tests/loom/compass_catalog.json, field_tests/loom/knockon_ledger.json, tools/project_docs/WEAVE_UNIFIED_EQUATION.md, WEAVE_TEST_BATTERY.md, and field_tests/results/.

| node | field / seam | what it holds | done (D-notes) | open | its balance condition |
|---|---|---|---|---|---|
| N1 Fold and knots | geometry | Z₆-II, χ = 48, the knots ρ and i, frozen U on tori 1–2, free U₃ | D1847, D1871, D1880, D1922–D1923 | the U₃ value; global tadpole consistency | the geometry is consistent; no hidden free modulus |
| N2 S, the dilaton | S | g_s = 2/√3 at ρ (S at i disfavoured); the plateau E(S, 3/2); n_s, r, the inflaton mass | D1523, D1926, D1926a, D1929, D1941a | g_s > 1 control; the vacuum curvature mass; N* against T_R; the tilt is a fit | n_s and r inside their bands with the tilt labelled honestly; g_s controlled or TRUST |
| N3 T, the volumes | T | σ_vis, N = 6, W₀ = 5.6e-9, 𝒱 = 4e4, m₃/₂ = 2.58e5; the dark cycle σ_d | D1811, D1871, D1937, D1937a | moduli masses shown (not just asserted); a hidden-stack argument for split stacks | KKLT consistent; all moduli heavy (F10) |
| N4 U, matter and flavour | U | one quark spurion with \|u\| in [0.02588, 0.02740]; leptons at ρ; neutrinos at i (TM1) | D1828–D1829, D1922–D1932, D1932a | the spurion's geometric home; Koide δ (TRUST); fluxes (4, 4, 8) | quark, lepton and neutrino naturalness with homes, or TRUST |
| N5 S–T seam: forces | S–T | α_s 0.1140 (−3.75σ with no thresholds; about −1σ with them); Δ₃; split stacks A₃/A₂ ≈ 0.75 (FIT) | D1880–D1881b, D1929, D1937–D1940, D1944a | the D7 threshold spectrum (decides whether α_s is a real test); deriving A₃/A₂; the y_t running fix | α_s predicted within error, or labelled FIT |
| N6 S–T seam: spectrum and dark matter | S–T / T | the wino at 686.5 GeV (INDETERMINATE against 660–700 GeV); the gluino; gravitino → wino (Ω ∝ T_R); m_X = 12.8 GeV | D732, D1941a, D1946, D1947 | the wino edge; indirect detection (E2); B3/B11 Higgs | spectrum allowed by colliders and indirect searches with margin |
| N7 S–T seam: reheating and genesis | S–T | T_R = 3.7e8 (boxed ≲ 3e9); non-thermal leptogenesis through φ → NN | D1931a, D1941, D1946a | **Br(φ → NN) ≤ 5.1 % against 9.5 % needed (FAIL)**; other channels; the CP source | the baryon asymmetry reproduced with a derived mechanism |
| N8 Late universe and the dark thread | S–T / dark | non-Kähler thread, λ ≈ 0.95; ζ = 3.8e-10; equivalence principle; PPN | D1887, D1906, D1906a/b | the thread's slope source; the five must-tests | DESI w₀–w_a matched with all five must-tests passed, or TRUST |
| N9 The battery and data | all | about 75 tests; A8 and F10 passed; E2 open; B5 indeterminate | D1936, D1946, D1947 | B3/B11, B8, C4/C6, A21, the NEED items | every RUN test scored with three sources and a lock |

## What each node agent reports (a JSON block, then at most 200 words)
```json
{"node": "N5", "state": "BALANCED|STRAINED|TRUST|INDETERMINATE",
 "fingerprints": [{"quantity": "...", "value": 0, "target": "...", "direction": "↑!|◔|●|○", "check_flags": ["C1..C7 issues"]}],
 "what_it_is_doing": "one sentence",
 "best_next_move": {"move": "...", "type": "derive|test|relabel", "expected_effect": "...", "cost": "low|med|high"},
 "predicted_knock_ons": [{"node": "N6", "effect": "...", "sign": "+|-|0"}],
 "honesty": ["anything in the D-notes that overclaims for this node"]}
```

## Coordination round (one pass)
1. All node agents run in parallel and report.
2. The coordinator merges the reports into WEAVE_BALANCE_BOARD.md and runs check.py and review.py on it.
3. The coordinator picks the moves whose predicted knock-ons do not strain other nodes. Each move is locked and run.
4. The knock-ons are logged and the compass is updated.
5. The referee reviews every second round.
6. Round k is null if no node changes state. Seven null rounds with every node BALANCED or TRUST means the endpoint is reached, and the full referee runs.
