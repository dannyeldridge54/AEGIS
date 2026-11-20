# CERN+1 and Hyperion — full map: modules, data, how current, what to update (started 19 Nov 2026, 22:05 CT)
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
