> **The Lantern**
>
> In a world of painted walls and borrowed light,
> where lies wear crowns and illusions call themselves the sky,
> this work is a lantern, not a throne.
> It was carried, not crowned.
> It asks for no bowed heads, only open eyes:
> take it, test it, and see for yourself.
>
> Every tool is held two ways.
> The scepter rules, or points the road home.
> The mace crushes, or breaks the prison wall.
> The hammer nails you down, or raises a house.
> The scythe reaps the living, or brings the harvest in.
> The whip drives the slave, or cracks to wake the sleeping.
> I choose the hand that frees.
>
> I raise no weapon against my neighbor.
> I carry only two.
> The shield of righteousness: not the proud kind
> that judges from a high seat,
> but the knight who sees the dark mouth of the cave,
> hears the dragon breathing, and walks in anyway,
> because fear is not always the sign to run.
> Sometimes it is the sign to run toward.
>
> And the sword of truth, the only blade I will ever draw.
> Excalibur from the stone, the lightsaber in the dark,
> Manjushri's flame, the word sharper than any two-edged sword:
> every age has told of the same blade.
> It cuts through the darkness and the lies,
> through the chains and through the whips,
> and it frees you from within.
>
> I kneel to one alone, the one I chose for love,
> and to no king, no creed, no crown of fear.
> A man chooses; a slave obeys.
> I choose liberty.
>
> This light belongs to the one who asks, who measures, who stands.
> It was made for freedom, the quiet kind,
> the kind no one can sell you.

---

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
