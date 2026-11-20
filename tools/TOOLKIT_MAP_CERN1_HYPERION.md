# CERN+1, Hyperion and Janus — full map: modules, data, how current, what to update (started 19 Nov 2026, 22:05 CT)
Danny 22:01: "CERN plus one and Hyperion only — get them up to date and fully mapped out with new data." Loop: one gap per 15 min, top of the queue first.
Rules: lock before recomputing; data-file downloads need Danny's OK; each row's "status" changes only with a D-note.

## CERN+1 (tools/lhc) — electroweakino collider toolkit
| module | what it does | data / references it runs on | newest public data to check | gap | status |
|---|---|---|---|---|---|
| xsec.py | wino pair cross sections 13 / 13.6 TeV (Resummino tables + Drell–Yan route) | Resummino 2304.11915 tables | any 2025–26 NNLL+approx-NNLO electroweakino tables; 13.6 TeV Run-3 official LHC SUSY xsec WG numbers | check | current (2023 tables) |
| higgsino.py | higgsino cross sections | 2304.11915 Table 4 | same as above | check | current |
| theory_band.py | scale+PDF band | 2304.11915 Table 6 | PDF4LHC21 band updates | low | current |
| lifetime.py | wino Δm and cτ | Ibe–Matsumoto–Sato 1212.5989 two-loop fit | 3-loop Δm (if published) | check | current |
| recast_dt.py | disappearing-track recast + HL-LHC projection | ATLAS 2201.02472 (136 fb⁻¹, Run 2) | **ATLAS/CMS Run-3 disappearing-track results (2025–26)**; CMS Run-2 full combination | **HIGH** | Run-2: 2201.02472 anchored; NEW 2603.08315 (670 obs / 770 exp GeV) found D1722, re-anchor NULL (no benchmark yield quoted; needs HEPData, D1723) |
| future.py | reach at any √s, lumi | DY scaling; FCC-hh study | 2026 European Strategy Briefing Book numbers (arXiv:2511.03883) | medium | pre-ESPP |
| settings.py (NEW 19 Nov) | run presets (Run 2, Run 3, Run 2+3, HL-LHC, HL ultimate, HE-LHC, FCC-hh); exports pyhf JSON, HEPData YAML, SLHA | all modules above | — | none | 6 tests PASS |
| stats.py | CLs (pyhf + independent) | — | — | none | validated |
| kinematics.py | boost distribution from the xsec table | 2304.11915 | — | none | validated |
| selftest.py / panel.py | symmetry tests; SERAPIS window vs reach | theory map | wino window now 0.67–1.25 TeV (D1324) | low | check panel label |

## Hyperion (tools/janus_astro) — astrophysics toolkit
| module | what it does | data / references | newest public data to check | gap | status |
|---|---|---|---|---|---|
| bbn.py / bbn_net.py | Y_p, D/H (PRIMAT, PArthENoPE, LINX) | CAMB tables, PRIMAT 2021/2023 | LBT 2026 Y_p = 0.2458 ± 0.0013 (in use); new D/H 2025–26; n-lifetime 2025–26 | medium | current to Nov 2026 |
| relic.py / sommerfeld*.py | wino relic + Sommerfeld LO/NLO | Hisano 0610249; Beneke 2009.00640 | per-channel matrices (1303.0200 supplement) still unreachable | parked | 2.0% Born, 4.4% LO |
| jfactor.py | J-factors, H.E.S.S. inner Galaxy | H.E.S.S. IGS 2026 limits; Singh–Desai 2605.16994 halos | CTA first data? new H.E.S.S./MAGIC/LST line limits 2026 | **HIGH** | Nov 2026 |
| galaxy.py / jeans.py / halos.py | Milky Way potential, Jeans, profiles | MWPotential2014, McMillan17 (default), Horta+2026 v_c | **Gaia DR4 (due Dec 2026)**; Eilers-type rotation curves 2026 | HIGH (Dec) | McMillan17 |
| mapper_feed / mapper_orbits / mapper_dust | Star Mapper: Gaia DR3 → orbits; dust | Gaia DR3; SFD/Bayestar (dust maps not downloaded) | Gaia DR4; dust maps need Danny's OK | HIGH (Dec) | DR3 |
| ns.py / compact.py | NS M–R, Love numbers (SLy, AP4) | Read+ 0812.2163 | **NICER 2025–26 radii (J0437, J0740, J0614 updates)**; GW230529-type events | medium | 2024-era checks |
| gw.py / gw_imr.py / gwb.py | inspiral phase, horizons, GW background | LAL; 7PN tides (Mandal 2412.01706) | **GWTC-4 (O4) catalogue**; O5 sensitivity curves | medium | validated physics; curves older |
| settings.py (NEW 19 Nov) | presets: BBN codes + datasets (LBT2026, Aver2021 Y_p; Cooke2018 D/H; Planck ω_b), NS EoS, MW models, halo profiles, H.E.S.S. IGS ROI, GW detector PSD names; pulls vs data; JSON/CSV/ECSV export | modules above | — | none | 4 tests PASS |
| hmf.py | halo mass function with Σm_ν | CAMB, Tinker08 | — | none | validated |
| stars.py / binaries.py / const.py | basic stellar physics | CODATA 2018 | CODATA 2022 constants | low | — |
| serapis_inputs.py | single source of SERAPIS inputs | D-notes | latest D-notes (D1716–D1721) | low | check |

## Queue (top first)
1. [found D1722] CERN+1: ATLAS 2603.08315 (670/770 GeV); no Run-3 DT result yet. 1b: NULL (D1723).
2. Hyperion: 2026 gamma-ray line limits (H.E.S.S./MAGIC/LST/CTA) → jfactor/wino window.
3. Hyperion: NICER 2025–26 radii → ns.py checks.
4. Hyperion: GWTC-4 / O4 → gw horizon curves and the NS tidal check.
5. CERN+1: ESPP 2026 future-collider numbers → future.py.
6. Hyperion: new D/H and neutron lifetime 2025–26 → bbn.
7. Gaia DR4 (Dec 2026) → galaxy + Star Mapper (scheduled for the release; data download needs Danny's OK).
8. CODATA 2022 → const.py.

## What working scientists ask of such tools (LHC Reinterpretation Forum, arXiv:2003.07868) → CERN+1 build list
| complaint / request | CERN+1 feature | status |
|---|---|---|
| full likelihoods in JSON (pyhf) | export one-bin pyhf workspace | DONE (settings.py) |
| read published likelihoods / HEPData tables directly | import pyhf workspaces + patchsets and HEPData YAML/JSON tables | DONE R1 (importers.py: load_workspace, apply_patch with digest check, cls, upper_limit, load_hepdata_table; 4 tests) |
| SLHA files for models | SLHA export | DONE; SLHA IMPORT DONE R2 (slha_in.py: MASS/NMIX/DECAY → character, Δm, xsec for a run, lifetime vs file; 2 tests) |
| efficiency maps per topology, ≥ 3 mass/lifetime points; LLP specifics | lifetime-dependent acceptance grid (τ, m) from the validated window model, exportable as HEPData | queued R3 |
| reference cross sections versioned and citable | Resummino tables with arXiv refs + theory band; version stamp in every output | partial (add version stamp R4) |
| statistics fully documented | CLs with stated test statistic, two independent routes (pyhf + exact Poisson) | DONE (stats.py); doc page R4 |
| covariance / simplified likelihoods (CMS) | multi-bin simplified likelihood with covariance | queued R5 |
| systematic validation against the experiments | validation report: every recast vs published limit (ATLAS 36, 136, 137) | partial (selftest); report R6 |

## Janus (tools/janus_calc = inflation calculator; tools/janus_lt = late-universe) — added Danny 22:10 "get them Janus too"
| module | what it does | data / references | newest data to check | gap | status |
|---|---|---|---|---|---|
| janus_calc core / core_jit | exact single-field Mukhanov–Sasaki n_s, r, α_s | validated vs slow-roll + published models | ACT DR6 / SPT-3G 2025–26 n_s, BICEP/Keck r | HIGH (data) | validated physics |
| anyV / models / observe | any potential; SERAPIS branches; reheating → N* → observables with error bars | — | — | none | validated |
| mfms / mfms_nc / mf_jit / twofield | multi-field MS, curved field space, δN f_NL | MultiModeCode, Kaiser+ | — | none | validated |
| janus_lt background / recomb / growth / transfer | expansion, recombination, growth, EH98 transfer | first principles; RECFAST | — | low | validated |
| janus_lt desi | DESI DR2 BAO likelihood | 2503.14738 Table IV | DESI DR3 (when public) | medium (future) | DR2 |
| settings.py (DONE J1, 20 Nov) | model library (φ², φ^{2/3}, Starobinsky, α = 1/3, Weave leading plateau) + n_s/r constraints (Planck 2018, CMB-SPA, CMB-SPA+DESI, BK18) with pulls; exports; 3 tests | — | ACT DR6 / SPT-3G 2026 updates (J3) | — | DONE |
| (old row) settings | presets: CMB datasets (Planck, ACT DR6, SPT-3G, CMB-SPA), BAO (DESI DR2), SN (Pantheon+, DESY5, Union3); model library; exports | — | — | queued J1 | — |
Janus queue (interleaved with CERN+1/Hyperion): J1 settings + exports; J2 complaints search (CAMB/CLASS/Cobaya/inflation-calculator users) → build list; J3 newest n_s/r data (ACT DR6, SPT-3G, BK) into the presets with pulls.

## Mapper (AEGIS Star Mapper + Sky Map: apps/skymap, ufe-v2/cosmos_map, Hyperion mapper_*) — added Danny 22:11 "mapper as well, that's for telescopes"
| part | what it does | data | newest data to check | gap | status |
|---|---|---|---|---|---|
| Star Mapper (cosmos_map) | re-verifies Gaia stars (192,208,838 re-checked) and flags unusual ones | Gaia DR3 | **Gaia DR4 (2 Dec 2026)** | HIGH (Dec) | DR3 |
| mapper_feed / mapper_orbits | Gaia → Galactocentric phase space, orbits (McMillan17) | Gaia DR3 + Bailer-Jones distances | DR4 astrometry, RVs | HIGH (Dec) | validated |
| mapper_dust | E(B−V) per star | SFD / Bayestar (not downloaded) | Bayestar19 / newer 3D dust maps (downloads now OK'd) | medium | prep only |
| Sky Map (apps/skymap) | browser sky atlas: surveys (Planck, Fermi, Gaia), objects, tonight's sky, lessons | HiPS surveys | new HiPS (Euclid Q1/DR1, SPHEREx all-sky, Rubin DP1) | medium | live |
| telescope tools (to build) | observability planner (alt/airmass for a site), target lists in standard formats (CSV/VOTable), cross-match with SIMBAD/Gaia IDs | — | — | queued M1 | — |
Mapper queue: M1 complaints search (amateur + professional observers: Stellarium, Aladin, astropy/astroplan, Gaia archive users) → build list; M2 observability/target-list export (astroplan-compatible, VOTable); M3 newest surveys into Sky Map (Euclid, SPHEREx, Rubin) as HiPS layers; M4 3D dust map download + validate mapper_dust; M5 Gaia DR4 ingest plan (release 2 Dec).

## M1 (20 Nov 04:25 UTC): what observers say is missing in sky tools → Mapper build list
Sources: SF Bay amateur list thread "Astro software seems like garbage"; KStars observation-workflow discussion (kstars-devel 2020-10); SkySafari / Stellarium feature-request boards.
| complaint | Mapper feature | id |
|---|---|---|
| no tool makes "a list of targets my telescope can do tonight from my location" (e.g. doubles a 60 mm can split) | target finder: filter by aperture (Dawes limit / limiting magnitude), site, date, altitude window | M1a |
| no single printable chart with designations, magnitudes, separations | printable PDF finder chart for a target list (labels on, one page) | M1b |
| only one Telrad/FOV circle, can't rotate FOV or place several | multiple FOV overlays (eyepiece/camera), rotatable, placeable anywhere | M1c |
| fixed meridian-transit scheduling breaks when plans shift; Dobsonian zenith hole | session plan sorted by "% of max altitude now", live re-sort, zenith-hole demotion | M1d |
| wish list grows unmanageable; can't mark observed; no projects | wish list + per-project lists, "observed" checkbox that demotes, filters (constellation, catalog, magnitude, culminating tonight) | M1e |
| tools don't talk to each other (coordinates to imaging/control software) | export CSV / VOTable / astroplan target table / N.I.N.A. & Stellarium-compatible lists | M1f (= M2) |
| download reference images before going to a dark site | offline pack: DSS/HiPS cutouts for the session list | M1g |
These join M2 (observability planner + target-list export) in the rotation; M1a + M1d + M1f are built first (one tick each).

## H1 (20 Nov 04:28 UTC): what astronomers say they need from analysis tools → Hyperion build list
Source: European astronomer survey (arXiv:2012.07686; ~1,000 respondents): reproducibility/transparency is the top concern (58.9%); findability + interoperability of data 59.3% (73.3% want IVOA standards enforced); cross-matching a barrier for 44.9%; visual analytics the top missing capability (71.7%); 82% want archives and computing integrated; 70% expect cloud processing on open-source tools. Plus installation pain for LALSuite/galpy-type stacks (versioned environments, arXiv:1407.3063).
| need | Hyperion feature | id |
|---|---|---|
| reproducibility | every result carries a provenance block: code version/commit, inputs, referee code + version, tolerance, D-note | H1a |
| interoperability / IVOA | ECSV + VOTable output with units (astropy-compatible); accept astropy Quantity/SkyCoord inputs | H1b |
| cross-matching | Gaia DR3/DR4 ↔ SIMBAD/2MASS cross-match helper (TAP/ADQL query builder) in mapper_feed | H1c |
| visual analytics | quick-look plots for every preset (rotation curve, M–R curve, GW horizon, BBN pulls) saved as PNG/SVG | H1d |
| installation pain | one-line install profile (pip extras: core / gw / galaxy / full) + `hyperion doctor` that checks optional deps (lalsuite, galpy, colossus, CAMB) and says what each unlocks | H1e |
| archive + compute | TAP queries to the Gaia archive from inside Hyperion (downloads OK'd) | H1f |

## UI (Danny 22:14: "make sure UIs are pro grade")
| id | item | status |
|---|---|---|
| U1 | one CLI for all toolkits: `--format json|csv|table` on every command, `aegis <toolkit> help`, exit code 2 + plain message for unknown commands/bad input, `--version`; new commands janus models/score/table, hyperion pulls/ns/jfactor, cern runs/point/reach/export/slha | DONE (20 Nov) |
| U2 | Sky Map web UI vs Aladin Lite / Stellarium Web | queued |
| U3 | web dashboard for the toolkits, Playwright-checked desktop + phone | queued |
