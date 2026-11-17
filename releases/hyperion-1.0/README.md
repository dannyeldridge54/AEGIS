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
