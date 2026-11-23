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

<!-- AEGIS-FP DT6YPL2R3TCKZMVK · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# SERAPIS prediction tracker

Re-scores the frozen SERAPIS predictions (`predictions.yaml`, from the locks) against the Inflation Scorecard's
data file and writes a dated status page: `docs/tracker/STATUS.md` and `docs/tracker/index.html` (static, light/dark).

```bash
pip install ./tools/scorecard
python tools/tracker/track.py            # options: --data other_constraints.yaml --out folder
```
A new data release is one new entry in `tools/scorecard/inflation_scorecard/data/constraints.yaml`; give it a
`date:` after 2026-11-15 and it counts as a real test (the page marks it "after freeze (TEST)"). Earlier data are
shown as consistency only, because the model was fitted to them. Statuses: alive / tension / KILL (a lock's kill
condition met). `pytest tools/tracker/tests` checks that a new release changes the page with no code edits.

## Licence
Dual-licensed: AGPL-3.0-or-later ([LICENSE](LICENSE)) or commercial ([COMMERCIAL.md](COMMERCIAL.md)).
