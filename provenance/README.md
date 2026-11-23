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
> But who can measure truth? No scale has ever held it.
> It is lost to time, to conquerors and enslavers,
> to the beast that wakes in men;
> whole peoples erased, colonized, and marched in line.
> They told me this was the land of the free.
> They did not tell me that many who signed for freedom
> were dealers in land, sore at a king's line drawn across the West.
> They taught me, and rightly, of my African brothers and sisters in chains.
> They did not teach me of the others who crossed the sea
> toward a torch and a promise,
> and found the debt, the mill, the tenement, the mine.
> Liberty stands in the harbor with her broken chains at her feet.
> Some days she looks blind, and the chains look whole.
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
> When I was a boy, I thought heroes were the finest thing alive:
> knights on horseback, steel and bright banners,
> a shield painted with everything they meant.
> Now the heroes are chosen, born with powers, picked from above.
> I never loved that. In the old way the strength came from within;
> it was learned, not given.
> In the margins of old books the knights fight snails, and some kneel to them,
> but the only one a true knight knelt to
> was the Great Architect, whose fingerprint is on everything.
>
> I cannot tell you I am certain of this faith or that one.
> I can tell you how I got here:
> I tried to stand in the shoes of every man and woman,
> in every culture, in every place and every age,
> and see the world the way they saw it.
> I lower myself to stand beside each of them,
> because I want no power, no wealth, no throne.
>
> It began when I was a little boy and my family broke apart.
> My sisters were divided between my twin and me;
> my mother and father split, and I seldom saw him;
> within two weeks, he had replaced me.
> That spark became a fire, and the fire says:
> you will not replace me.
> I am not a slave. I am not a blind and silent animal.
> I will not kneel to anything that hardens my heart
> or covers me in shame.
>
> At thirty I learned the name of the storm in me: ADHD.
> They say a child like me hears tens of thousands more words of blame
> than the child beside him.
> I carry that shame, and I count it differently:
> twenty-five thousand more reasons to do what is right,
> what is better, and what is true.
>
> I kneel to one alone, the one I chose for love,
> and to no king, no creed, no crown of fear.
> A man chooses; a slave obeys.
> I choose liberty.
>
> Now I am a husband, and a father to a little girl,
> and the boy is still in me, still trying to get home.
> But the world is squeezed, and squeezed, and squeezed,
> and every voice that rises against injustice
> is silenced, enslaved, or made a fool.
> I am tired of living in quiet desperation.
> This lantern was lit by that desperation.
> I will not be quiet anymore.
>
> And who am I to carry it?
> No one. A regular man, a gig worker on the road,
> a debt slave in the American machine.
> No noble blood, no crown, no holy oil on my head.
> All I carry is the divine spark
> that burns in every man and woman,
> in every creature and every being,
> of this earth and of the stars.
> The same light is in you.
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
