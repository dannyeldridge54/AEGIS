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

# Hyperion 1.0 — validated astrophysics toolbox (AEGIS)
Hyperion is the late-universe and astrophysics calculator of AEGIS (its early-universe twin is Chronos Clock). Every module is checked against the field's standard code or an exact solution under a pre-registered lock (rules written and hashed before each run); failures are kept on record.
Author: Danny Lee Eldridge (dannyeldridge54@gmail.com). Code written with AI assistance (Claude); see the D-notes for every run.

## Validated (locked tests passed)
| Module | What it does | Checked against | Note |
|---|---|---|---|
| stars | Lane–Emden polytropes, Chandrasekhar mass, Eddington luminosity | exact solutions, Chandrasekhar tables | D1052 |
| compact | TOV structure, Kerr ISCO | exact Schwarzschild interior; two routes | D1052 |
| standards | GW timing, halo profiles, Kepler, Oppenheimer–Volkoff 0.7102 M_⊙ | LALSuite, galpy, colossus, astropy | D1053 |
| gw | TaylorF2 phase to 3.5PN; aligned spins to 2.5PN | LALSuite (≤ 6.5e-10 rad) | D1054, D1066 |
| gw (detectors) | amplitude, SNR, horizons, BNS ranges, cosmological ranges, IMRPhenomD horizons | LALSuite PSDs, astropy | D1062–D1064 |
| jfactor | dark-matter J-factors (Einasto, NFW, Burkert, cored) | two routes | D1055 |
| sommerfeld | wino Sommerfeld enhancement | Coulomb exact, resonance 2.38 TeV | D1056 |
| gwb | primordial GW background through any reheating history | analytic slopes, radiation plateau | D1057 |
| hmf | σ8, halo mass functions (PS, ST, Tinker08), neutrino-mass effects | CAMB, colossus | D1060, D1068 |
| galaxy | Milky Way potential (MWPotential2014), orbits | galpy (1e-15) | D1061 |
| mapper_feed | Gaia astrometry → Galactic coordinates (Gaia DR3 convention), orbits | Gaia DR3 matrix A_G' (2e-16), exact turning points | D1072, D1077 |
| fast | compiled orbits 0.4–0.5 ms/star | regression vs Python (5e-10) | D1076 |
| speed | vectorised paths 1.9–3.3× faster than galpy/colossus/LAL | same answers | D1070 |
| mapper_orbits | Star Mapper → orbits CLI + Windows launcher | synthetic Mapper tiles | D1078 |
| wiring | Chronos Clock ⇄ Hyperion; Mapper ⇄ Milky Way ⇄ wino | lossless, closes | D1079, D1080 |

## NOT validated as locked (kept on record)
- Neutron stars (SLy/AP4): physics reproduced (M_max 2.048 M_⊙, R_1.4 11.71 km, Λ_1.4 296) but the integrator cross-check missed its radius tolerance (surface definition) — D1058, D1059.
- First mass-function battery: colossus δ_c convention mismatch (fixed and validated in D1068) — D1067.
- First benchmark (test-grid error; fixed in D1070) — D1069.
- Mapper coordinates vs astropy (25 mas: astropy's Galactic frame differs from Gaia's; Gaia convention validated in D1072) — D1071.
- Early fast-orbit versions (superseded by D1077) — D1073–D1075.
- Fast J-factor path (cored halos; dropped) — D1076.
- Spin phase at 3PN spin–spin and above: terms not yet sourced — D1066.

## Run the Star Mapper feed on a PC
Double-click `ufe-v2/START_HYPERION_ORBITS.bat` (installs numpy, scipy, numba, galpy if missing; reads cosmos_map/tiles read-only; writes cosmos_map/hyperion and apps/skymap/data/hyperion_orbits.json; resumable). About 0.45 ms per star after a 2 s compile.

## License
Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV), as for the whole AEGIS repository — see LICENSE.
