# UB-1 deviations (logged before any search ran)

## D1, 2026-11-07T23:55:54Z: integrator LSODA -> DOP853 (`theory/unify_hyperbolic_bg_v2.py`)
Found while building the UB-2 code, before UB-1's search ran anywhere. In the locked code the right-hand side raises an
error when a trial state has H^2 <= 0 or K >= 3. LSODA (stiff mode) probes wild trial states once the angle starts to
oscillate, so many healthy solutions are thrown away: in a 40-point timing sample 8/40 (A) and 9/40 (B) integrations
survived with LSODA against 27/40 and 39/40 with DOP853 (an explicit integrator). A cross-check at one point gave the same
result with Radau (implicit) and DOP853 (ln A = -0.607 both). No requirement, box, seed or search setting changed.

Per the rule, **both** are run and reported: the locked version as written (`unify_hyperbolic_bg.json`) and D1
(`unify_hyperbolic_bg_v2.json`). If they disagree, both verdicts are stated and the reason is the integrator.

## D2, 2026-11-08T01:09:04Z: result file could not be written (numpy bool), re-run with a JSON fix
Both first runs finished the search and computed the verdict, then crashed writing the result (`Object of type bool is
not JSON serializable`): the files stop after the first row. Verdict lines already written: **locked version FAIL**,
**D1 PASS**; the variant B rows were lost. The partial files are kept (`*_crashed_partial.json`). Both are re-run
unchanged through `theory/run_ub1_d2.py`, which only lets json.dump write numpy booleans. The search is seeded and
deterministic, so the re-run must reproduce the same verdicts; if it does not, that is reported.
