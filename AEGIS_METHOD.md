# The AEGIS Method: an AI framework for honest discovery

Danny Lee Eldridge, with Claude · 26 October 2026 · This knowledge belongs to all of us. Share it freely.

**The idea:** let AI be creative and honest at the same time by walling apart two kinds of claims:
**Evidence** (tested against data) and **Hypothesis** (an idea still to test). Beliefs and values are never entered as claims.

## Eleven rules (enforced in code, not hoped for)
1. Walled tiers: nothing becomes Evidence without passing through the rules below.
2. Mechanism first: a pattern becomes Evidence only with a named cause and the data that tests it.
3. Write it down first: claim, test, data and pass/fail rule, hashed (SHA-256) before the run.
4. Disclose what was seen: an idea found in the same data is marked "not blind".
5. Charge every assumption: 2 points per free setting (AIC).
6. No hand-typed numbers: every number is recomputed from stored results before release.
7. A second pair of eyes: a different agent reviews against the raw results and logs its findings.
8. Lenses generate, tests decide: creative proposals stay Hypothesis until tested.
9. Losses in the same size print: failures are published and never deleted.
10. The human holds the keys: anything public, irreversible, financial or about values waits for the person.
11. Plain words for everyone: plain-language results, translatable, equations untouched.

## The loop
Observe → a lens proposes → write the rule down → test → guardrails recompute → second-agent review → human approves → publish (losses included) → update the map (the Weave).

## In this repository
- `ufe-v2/aegis/method.py`: the claim store, the wall (raises `WallError`), rule locks, ledger, `python -m aegis.method check`
- `ufe-v2/method/claims.json`: 20 claims from 26 Oct 2026 (2 passed, 5 failed, 2 untestable, 1 withdrawn, 10 open)
- `ufe-v2/aegis/guardrails.py`: check 7, "The Method (claim wall)"
- `/method` on the AEGIS monitor: the live ledger

Prior art: pre-registration (clinical trials, psychology reforms), AIC (Akaike 1974), blind analysis (particle physics), AI scientist and reviewer agents. The contribution is the combination, especially the enforced wall between evidence, hypothesis and meaning.
