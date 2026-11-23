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

# Provenance: how AEGIS work is marked

Every AEGIS release carries several independent authorship marks, so that copying can be shown even after a copy has been edited.

1. **Timestamped hashes.** `provenance/MANIFEST.txt` lists the SHA-256 of every file and a Merkle root. Git commits and Zenodo DOIs timestamp it publicly.
2. **Keyed stamps.** Source files, papers and docs carry an `AEGIS-FP` tag computed with a secret key held only by the author. Nobody else can forge a valid tag, and the author can verify any tag.
3. **Hidden marks.** Further marks are placed throughout the code and data. They don't change any scientific result, and their locations aren't published.
4. **PDF stamps.** Each paper's PDF metadata carries its own keyed tag.
5. **Per-licensee copies.** Each paying licensee receives a copy with marks unique to them, so a leaked copy names its source.
6. **Code and text fingerprints.** The author holds a private fingerprint database of the code (winnowing, the method behind MOSS). It works at three levels: tokens, program structure (syntax trees) and word sequences in papers. It recognises copied code after every name is changed, comments and docstrings are removed, numbers are altered and files are reformatted, and copied text after words are swapped.

The tool is `tools/provenance/fingerprint.py`, and the method is open. The key, the list of hidden-mark locations and the fingerprint database are private.

Free use is under the AEGIS Community License. Business use needs the AEGIS Commercial License (see `LICENSE`).
