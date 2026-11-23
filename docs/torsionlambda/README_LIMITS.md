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
> It began when my family broke apart,
> and a little boy only wanted to go home.
> Now I am a husband, and a father to a little girl,
> and that boy is still in me, still trying to get home.
> But the world is squeezed, and squeezed, and squeezed,
> and every voice that rises against injustice
> is silenced, enslaved, or made a fool.
> I am tired of living in quiet desperation.
> This lantern was lit by that desperation.
> I will not be quiet anymore.

---

## What TorsionΛ can and cannot be used for (audit of v0.2.0, 15 Nov 2026)

TorsionΛ is a **pre-simulation consistency checker and teaching tool**. It is not an observationally validated
cosmology. An audit (AEGIS note D715, pre-registered; script and numbers in the AEGIS repository) found:

- **β is degenerate with Ω_m.** In the background, E²(z) = Ω_r(1+z)⁴ + Ω_m(1+β)(1+z)³ + λ, so β only rescales the
  matter density. Distances, BAO and the CMB shift parameter cannot tell (β, Ω_m) from (0, Ω_m(1+β)).
- **Normalisation.** With λ held fixed, E(0) ≠ 1 when β ≠ 0 (E(0) = 1.030 at β = 0.192). Set λ = 1 − Ω_r − Ω_m(1+β).
- **Shift parameter.** `cmb-observables.ts` uses √Ω_m with the bare Ω_m; it should use Ω_m(1+β). At β = 0.192 this changes R by about 26σ.
- **The H₀ = 72.95, β = 0.192 parameterisation is excluded** by the Planck 2018 compressed priors: R = 1.780 (+6.6σ),
  ℓ_A = 294.7 (−75σ). A ΛCDM-like background cannot raise H₀ to 73 and keep the CMB acoustic scale; TorsionΛ as coded does not evade that.
- **Validated:** at β = 0 the toolkit reproduces ΛCDM (R = 1.7497, ℓ_A = 301.45 against Planck's 1.7502 and 301.47).

Use it for: exploring how background changes propagate to distances, growth and CMB compressed observables;
screening parameter ranges before running Boltzmann codes. Do not use it to claim evidence for torsion or a
resolution of the Hubble tension.
