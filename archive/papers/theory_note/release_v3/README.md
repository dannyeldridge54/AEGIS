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

# Spiral Twist theory note, Zenodo version 3

This release adds a bounded QCD-anomaly scale assessment to the BI axion-dilaton theory note. It preserves the
distinction between the derived supergravity kinetic geometry, the hypothesized Spiral Twist potential, and the
separate Nieh–Yan/QCD candidate.

## Files prepared for the Zenodo record

- `spiral_twist_note_v3.pdf` — compiled manuscript.
- `spiral_twist_note_v3.tex` — manuscript source.
- `spiral_twist_v3_supplement.zip` — version 2 supplement contents plus the reproducible QCD derivation, its
  parameter-scaling tests, the updated theory README, and the v3 manuscript source.
- `METADATA_v3.json` — proposed Zenodo metadata; it is a local form reference, not a record file.
- `SHA256SUMS.txt` — hashes for the files prepared for upload.

The QCD scale calculation uses the zero-temperature susceptibility and a fixed relativistic-degree-of-freedom
approximation. Its equality fraction is an analytic, small-angle estimate relative to total density; it is not a
thermal-QCD likelihood fit. No result from the still-running combined likelihood minimization is included.

Focused validation command:

```powershell
python -m pytest theory\test_bi_supergravity.py theory\test_bi_qcd_axion.py -q
```
