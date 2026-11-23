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
> To the kings: the Mandate of Heaven was never yours to keep;
> it leaves the throne the day the throne stops serving.
> To the priests: no temple owns the sky,
> and grace was never sold at a door.
> To the judges: your heart is weighed on Ma'at's scale
> against a single feather, like every heart.
> To the scientists: Galileo stood alone and was right;
> a consensus is not a measurement. Show me the data.
> To the generals, the presidents, the bankers and the lords:
> remember the seventh generation; remember ubuntu, I am because we are;
> the emperor has no clothes, and the children can see it.
> Diogenes walked Athens at noon with a lamp, looking for one honest man.
> I carry the same lamp. I am still looking.
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

# The AEGIS Method (portable kit)

A way to do research that cannot quietly fool itself, usable in any field: physics, medicine, psychology, AI
evaluation, citizen science. Developed by Danny Lee Eldridge in the AEGIS / Twist cosmology project (2026).

## The rules
1. **Write the rule before the data.** Question, model, data, method, a code gate, and the exact thresholds that turn
   numbers into words (`RULE_TEMPLATE.md`).
2. **Lock it.** SHA-256 fingerprint + UTC time (`python lock_rule.py lock RULE.md`), then publish the fingerprint
   (git push, Zenodo, Software Heritage) before looking.
3. **Gate the code.** Before any result, the code must reproduce a known answer within a stated tolerance.
4. **Never edit a locked rule.** Changes go in a deviation log, written before rerunning (`DEVIATION_TEMPLATE.md`).
5. **Report failures at full size.** A failed test gets the same space as a pass and stays on record.
6. **Count your attempts.** Report local and global significance (look-elsewhere correction) side by side.
7. **Keep a ledger.** Every rule, its fingerprint re-verified, every verdict (`python lock_rule.py verify FOLDER`).
8. **State what is derived, chosen and fitted.** Every number in a model is labelled.
9. **Lock predictions before new data arrive,** and score them mechanically when the data are public.
10. **Make it reproducible:** one command from public data to the headline number.

## In practice (AEGIS, as of 8 Nov 2026)
50 locked files re-verified (47 exact, 3 Windows line endings only, 0 content changes); 72 verdicts on record,
16 of them failures. See `field_tests/ledger/LEDGER.md`.

## Licence
Same as the repository.
