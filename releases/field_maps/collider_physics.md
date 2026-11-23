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

# Field map: collider physics and searches for new particles (CERN+1's field)

Rotation rung 5, 2026-11-23. Toolkit: **CERN+1** (tools/lhc). Speed rung: the whole suite runs in 2.5 s; nothing to speed up.

## What the field says it needs (US P5 report, Dec 2023)
- [study] Highest priority: finish the ongoing projects - the High-Luminosity LHC, DUNE, Rubin/LSST. Then CMB-S4, DUNE Phase II,
  a G3 dark-matter experiment, IceCube-Gen2; an offshore Higgs factory (Europe or Japan); R&D toward a 10 TeV parton
  centre-of-mass collider including a 10 TeV muon collider (a demonstrator possibly at Fermilab); a new agile small-project
  program (ASTAE); more support for theory, instrumentation and computing.
- [study] Science drivers: neutrinos; the Higgs boson; direct evidence of new particles; quantum imprints of new phenomena;
  dark matter; what drives cosmic evolution.
- [study] Long-lived particles and compressed spectra are where much of the remaining natural-SUSY space hides (see the
  SUSY map); recasting published searches and reusable likelihoods (HEPData, pyhf) are community needs.

## Oklahoma
- OU and OSU high-energy physics on ATLAS (Oklahoma Center for High Energy Physics); H. Baer (OU), K. S. Babu (OSU) in theory.

## What CERN+1 covers
- [ours] Cross sections, kinematics, lifetime/displaced-track recasts (recast_dt), higgsino tools, HL-LHC and future-collider
  reach (future.py), statistics with pyhf workspace round-trips, HEPData importers, theory bands, SLHA input.

## Gaps and build order
1. Same-sign dilepton (k++) reach from Aion's Zee-Babu flavour predictions -> a collider target for Babu.
2. Muon-collider higgsino reach on top of future.py (ties to Baer's 2510.20920).
3. Long-lived wino/higgsino lifetimes from Zurvan spectra -> disappearing-track recasts.

## Sources
P5 2023 Executive Summary (usparticlephysics.org); CERN+1 USER_GUIDE.md.
