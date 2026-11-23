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

<!-- AEGIS-FP XTH3X427LFK62N36 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# CERN+1 — an independent, validated toolkit that redoes the LHC chain and checks itself

*Independent work by Danny Eldridge (AEGIS project), built with Claude (Anthropic). Not affiliated with, produced by, or endorsed by
CERN or any LHC experiment; "CERN+1" is our working name for "the CERN chain, plus one more independent check at every step".*
Code path: `tools/lhc/` (registry tools `lhc_xsec`, `lhc_ul`, `lhc_lifetime`, `lhc_dt_limit`).

## What the LHC chain does, and what CERN+1 does at each step
| Step | Standard practice | CERN+1 | Measured result |
|---|---|---|---|
| Production cross section | Resummino / Prospino: one heavy run per mass and energy, tables at 13 and 13.6 TeV | Two independent routes: (1) ln σ–ln m spline of the reference tables; (2) Drell–Yan scaling with one universal evolution exponent — needs no PDF file | Route 1 reproduces left-out table points to 0.016% median, 0.30% max. Route 2 predicts the 13.6 TeV table from 13 TeV alone to ≤1.0%, ≤0.29% with κ = −0.163 (same for all three wino channels). At 14 TeV the routes agree to ≤1%; the spread is quoted as the error. Microseconds per call. |
| Particle lifetime | A single benchmark lifetime (τ ≈ 0.2 ns) | Mass-dependent pure-wino lifetime from the two-loop mass splitting, with π, eν and μν widths (μν phase space added) | δm(1 TeV) = 164.1 MeV, cτ = 5.83 cm, BR(π) = 97.9%; τ at the ATLAS limit 0.197 ns |
| Statistics | pyhf asymptotic CLs | pyhf AND exact Poisson CLs side by side; the exact value is used at low counts | Asymptotics are off by up to 8% at low counts (5.00 vs 5.40 events for b = n = 3) |
| Reinterpretation (recast) | SModelS / CheckMATE / full experiment likelihoods | Benchmark-anchored recast that combines our cross sections, our lifetimes and the published signal-region numbers | Two ATLAS disappearing-track searches reproduced with ONE method, no retuning: 136 fb⁻¹ → 666.6 GeV vs 660 (+1.0%); 36.1 fb⁻¹ → 447.8 GeV vs 460 (−2.7%); with the computed boost distribution (kinematics.py, D1307) they become 661.5 GeV (+0.2%) and 446.6 GeV (−2.9%); with the Resummino scale+PDF and δm theory band (theory_band.py, D1309) 661.5 ± 10 GeV (660 inside) and 446.4 ± 5.5 GeV (460 outside); the 36 fb⁻¹ gap is explained by that search's mass-dependent acceptance and its fixed 0.2 ns lifetime: with both, 457.2 GeV (−0.6%, D1311); HL-LHC like-for-like ≈ 975 GeV |
| Symmetry self-tests | — (not standard) | Charge asymmetry (u/d), Drell–Yan scaling of ratios, SU(2) charged/neutral ratio checked on every table | Ratios scale with τ₀ to 0.1% / 0.05%; the charge asymmetry turns over above 1.5 TeV — flagged as the PDF-limited region (our locked monotonic prediction failed there) |
| Model vs collider | — (experiments test generic models) | Reads the SERAPIS wino window from the theory map and overlays CERN+1 reach | Window 0.67–1.85 TeV begins at the Run-2 limit (666.6 GeV); HL-LHC tests 26% (to ≈975 GeV); the rest needs other probes |
| Future colliders | Dedicated projection studies (one per collider) | One module for any √s and luminosity, anchored on the Run-2 recast | HL-LHC 0.97 TeV vs published 0.9; HE-LHC 1.36–1.68 vs 1.5–2.1; FCC-hh 2.9–3.7 vs 4.5–6.5 TeV (short — cross-section extrapolation to 100 TeV is the weak link); FCC-hh covers the whole SERAPIS window |
| Event generation, detector simulation | MadGraph5_aMC@NLO, Pythia8, Delphes | Not yet (planned, heavy) | — |
| Parton distributions | LHAPDF global sets | Pending (one PDF file to fetch) — then an independent LO calculation as a third cross-section route | — |

**Higgsinos (D1313):** `tools/lhc/higgsino.py` adds the four higgsino channels (100–1500 GeV); the wino-fitted scaling exponent predicts the 13.6 TeV higgsino tables to ≤ 0.34% without refitting.

## Our process (how we work, and why it is more accurate)
1. **Lock before computing.** Every prediction (what a check should give, and what counts as a pass) is written down, hashed (SHA-256)
   and published to the repository BEFORE the calculation runs (field_tests/rules/PREREG_LHC*.md). Failures are reported as failures —
   e.g. LHC2's first prediction of the wino mass splitting was 1 MeV too low and is recorded as a partial FAIL.
2. **Two independent routes for every number.** A number is only trusted when two methods that share no shortcut agree, and the
   disagreement becomes the quoted error (cross sections: table spline vs physical scaling; limits: pyhf vs exact Poisson).
3. **Reproduce the experiment before predicting.** A recast is only used after it reproduces the experiment's own published limit
   (ATLAS 660 GeV → ours 666.6 GeV) — only then is it extrapolated (HL-LHC).
4. **Replace fixed benchmarks with computed physics.** Where the standard chain uses one benchmark value (a single lifetime), we compute
   it as a function of the model parameters from the published formulas.
5. **Everything is checked, logged and connected.** Each result has a derivation note (D1299–D1301), runs in the shared registry used by
   the Janus app and by the CubeMind learning system, and appears as a node in the AEGIS web.

## Why it is better — stated precisely
- **Faster:** µs–seconds per answer vs minutes–hours per point for the reference codes, with the error bar attached.
- **More honest errors:** every answer carries a measured interpolation or route-spread error instead of an implicit one.
- **More accurate where the standard shortcut is weak:** exact CLs at low counts (up to 8% better than asymptotics); mass-dependent
  lifetimes instead of one benchmark.
- **Not yet better at:** full event simulation and detector response — CERN+1 currently relies on the experiments' published
  efficiencies and on the reference cross-section tables. These are the next steps.

## How we came up with it
It grew out of the AEGIS/SERAPIS research, which predicts wino dark matter with a mass window that LHC searches can test. To score that
prediction honestly we needed the same numbers the experiments use, fast and with errors. The cross-section download was blocked, so we
asked what the physics alone fixes: Drell–Yan scaling says s·σ depends only on 4m²/s, which turned one energy's table into a predictor
for every energy — and the leftover correction came out identical for all three channels, showing it is parton evolution, not a fudge.
The same habits that built the Janus calculator (lock first, two routes, reproduce before predicting) were applied to each LHC step.

## References
Resummino 13.6 TeV tables: arXiv:2304.11915 · Wino mass splitting and widths: arXiv:1212.5989 · ATLAS disappearing tracks (136 fb⁻¹):
arXiv:2201.02472 · CERN+1 cross-section note: doi:10.5281/zenodo.24342227 · Lock workflow: doi:10.5281/zenodo.24291026.

## Support this work

All of this (the research, the toolkits and the papers) is built by one person, Danny Eldridge, an independent, self-taught researcher in Oklahoma City, working with the help of AI. He is trying to change his circumstances in life, and he promises to keep doing what he is doing now: releasing the work openly, free to individuals, scientists and students, and using it to try to make the world a better place. If it helps you, a donation of any size keeps it going: **email dannyeldridge54@gmail.com to donate** (a direct donation link is coming). Businesses: please license through the AEGIS Commercial License instead.
