<!-- AEGIS-FP M6GEZBQ5KBEYSTS5 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# Hyperion — astrophysics module (was Janus-Astro; track X; names: docs/TOOL_NAMES.md)
Goals (Danny, 17 Nov 2026): an astrophysics calculator built "like we did Janus" — every result validated against the field's gold-standard code or exact solution, faster and with error bars, then turned on AEGIS's own predictions and data.
Pattern (same as Janus / Janus-LT): fast route + independent second route + gold-standard referee; every stage locked before running (PREREG + sha256 pushed), D-note, no reruns to chase; Zenodo versions only on Danny's "Publish".

## Done
- A0 (D1052): stars (Lane–Emden, Chandrasekhar, Eddington, KH), TOV (exact interior), Kerr ISCO, 0PN GW, NFW/Einasto/Burkert, Kepler/Hill/Roche, constants — 9/9.
- A0s (D1053): vs LALSuite, galpy, colossus, astropy, Oppenheimer–Volkoff 1939 (0.7102 M_⊙), Kepler sidereal year — 7/7.
- A2a (D1054): TaylorF2 3.5PN phase vs LALSuite ≤ 6e-10 rad (4 binaries, 2PN and 3.5PN).

- A7a DONE (D1055): J-factors for the H.E.S.S. inner-Galaxy region (two routes ≤ 8e-8); wino window per halo profile.

- A7b DONE (D1056): wino Sommerfeld solver (Coulomb 3e-5, resonance 2.38 TeV); line rate ×6 from 1 to 1.85 TeV; window per halo profile.

- A7c DONE (D1057): SERAPIS GW background per reheating history (route B mode evolution; plateau 6.5–7.2e-19; knee 0.03–0.08 Hz τ=i vs 8–80 Hz ρ).

- A3a/A3b (D1058): NOT VALIDATED as locked (crash; N4 surface-definition 1.5e-5); SLy M_max 2.048, R_1.4 11.71 km, Λ_1.4 296; AP4 2.188, 11.32 km, 248. Next A3c.

- A3c (D1059): NOT VALIDATED (N4 R 1.1e-5 vs 1e-5; surface ill-conditioned); EoS vs GW170817 (both OK) and NICER (J0740 wants larger R, J0614 smaller).

- A7d DONE (D1060): Σm_ν = 0.0587 eV: σ8 −1.72%, n(>1e15 M_⊙/h) −11% vs massless (CAMB + colossus, H1 1e-4, H2 ≤ 5e-4).

- A5a DONE (D1061): Milky Way (MWPotential2014) vs galpy to 1e-15; orbit 1 Gyr to 1e-11 kpc; ρ_DM,⊙ = 0.286 GeV/cm³ → wino limits ×1.36 looser. A7e deferred (no parallaxes in stars.json).

- A2c DONE (D1062): amplitude vs LAL 5e-15; SNR; BNS ranges of 5 LIGO/KAGRA curves within ≤ 4.8%.

- A2c2 DONE (D1063): cosmological horizons/ranges (D_L vs astropy 7e-7; Finn–Chernoff MC 1.4e-4); A+, ET, CE reported; CE BNS z_h ≈ 19 flagged (inspiral-only).

- A2c3 DONE (D1064): IMRPhenomD horizons; CE flag resolved; A+ 50+50 z_h 3.04 matches the CE Horizon Study's 'not beyond 3'.

- A2b DONE (D1066): aligned-spin TaylorF2 vs LAL ≤ 6.5e-10 rad through 2.5PN spin order; 3PN spin–spin terms missing (A2b2).

- A4 (D1067): NOT VALIDATED as locked — growth ≤ 7e-4, Tinker08 ≤ 2.2e-3, but PS/ST up to 6% at 1e15 (colossus wrapper vs its own model function; A4b).

- A4b DONE (D1068): PS/ST/Tinker08 vs colossus ≤ 1e-2 at z = 0–2 after matching colossus's δ_c convention (1.686 vs corrected 1.676).

- A6a (D1069): NOT VALIDATED (T3 grid too coarse to unwrap); accuracy matches referees but Hyperion is slower than galpy/colossus (Python loops) — A6b vectorise. A2b2 blocked on sourcing the 3PN SS terms.

- A6b DONE (D1070): vectorised; 1.9–3.3× faster than galpy/colossus/LAL on the benchmark tasks, same accuracy.

- A8a (D1071): Star Mapper feed — orbits vs galpy 5e-10; NOT VALIDATED on the Galactic-pole convention (7e-6 deg vs astropy); 0.5 s/star too slow → A8b (Gaia A_G matrix) + A8c (vectorised orbits).

- A8b DONE (D1072): mapper coordinates = Gaia DR3 convention (A_G' to 2e-16); astropy differs by 25 mas (D1071a corrects D1071).

- A8c (D1073): batch orbits 2.9 ms/star (70×) but r_peri off 2.5% → NOT VALIDATED; A8c2 (adaptive step / turning-point refinement).

- A8c2 (D1074): adaptive orbits meet accuracy for disk stars (≤ 1e-3), r_peri 1.3e-3 for extreme stars; 15–26 ms/star → NOT VALIDATED on cost; A8c3 (faster forces).

- A8c3 (D1075): disk stars PASS at 8.8 ms/star; extreme r_peri 1.3e-3 (reference sampling suspected) → NOT VALIDATED; A8c4 exact turning points in the reference.

- A6c (D1076): compiled orbits 0.41–0.50 ms/star (identical to batch3 to 5e-10); fast J path fails on cored halos (dropped) → NOT VALIDATED as locked.

- A8c4 DONE (D1077): Mapper fast orbits VALIDATED vs exact turning points (≤ 9.4e-4); D1075's miss was the sampled reference.

- A8d DONE (D1078): PC version — mapper_orbits CLI + START_HYPERION_ORBITS.bat, validated on synthetic tiles.

- A5b DONE (D1083): spherical Jeans σ_r (constant β) vs galpy ≤ 1.5e-11; exact point-mass check 3e-16.
- A3d (D1086): NOT VALIDATED — a common finite surface leaves R 1e-5 apart (masses 1e-11); the A3c surface diagnosis was wrong; next A3e diagnostic.
- A3e/A3f DONE (D1090, D1094): mismatch was the referee compact.tov's absolute P tolerance; fixed via DEVIATIONS; NS module VALIDATED (≤ 8e-11 common surface).
- A2d DONE (D1098): TaylorF2 tidal phase 5PN+6PN (VFH 2011) vs LAL ≤ 8.8e-10 rad; 6.5/7PN tidal (0.03 rad) not yet included.
- BBN: bbn (PRIMAT table, D1082/D1082a), three-code check (D1107), bbn_net LINX module VALIDATED (D1109; dNeff_init is LINX's initial ΔN).
- Since D1102 (D1103–D1124): NLO CMB band (D1103); γγ line (D1110/D1114) → full line incl. γZ (D1118) → NLL-resummed line (D1121), scale band (D1124); 6.5PN tides VALIDATED, 7PN PARKED (0.33% vs LAL; HFB erratum; D1111–D1120); MW bracket MWPotential2014–McMillan17 (D1105–D1112); three-code BBN + bbn_net + τ=i ΔN (D1104–D1122); v3.3 paragraph (D1123).
- OPEN: 7PN coefficient (needs character-exact source); A1e blind NLO-wino check; Mapper per-star + dust (Danny's PC); H.E.S.S. limits below/above 1 TeV (only 1 TeV quoted); NLL′/endpoint line; McMillan17 J with real H.E.S.S. ROI geometry.
- Release 1.1 DRAFT notes: releases/hyperion-1.1/CHANGES_SINCE_1.0.md (D1102; not packaged/uploaded).

## Gold-standard stages (referee in brackets)
- A2b GW amplitude + spins (aligned) + tides [LALSuite TaylorF2, IMRPhenomD for inspiral match]; A2c detector noise curves, SNR, match, horizon distance [PyCBC/LALSuite PSDs, published BNS ranges]; A2d stochastic backgrounds Ω_GW(f) from inflation, PTA/LISA/ET power-law sensitivity curves [published PLS curves].
- A3 Neutron stars: tabulated EoS (SLy, APR4) → M–R, tidal Λ [published tables; GW170817 Λ̃, NICER radii].
- A4 Halos in cosmology: σ(M), Press–Schechter / Sheth–Tormen / Tinker mass functions, c(M) [colossus], linked to Janus-LT growth.
- A5 Galactic dynamics: rotation-curve fits, Jeans, orbits in Milky Way potentials [galpy MWPotential2014].
- A1 Realistic stars: main-sequence models, opacities, nuclear rates [MESA/MIST tracks, standard solar model].
- A6 Benchmark: speed and accuracy vs the referees, plus one-call things they don't do.

## AEGIS applications (our best data and predictions)
- A7a SERAPIS-E wino DM and the Galactic halo: exact J-factors for the H.E.S.S. inner-Galaxy region, Einasto vs NFW vs cored profiles, upgrading D735's order-of-magnitude "cores weaken limits by 1e2–1e3" (halo_profile node; Gaia DR3 prefers Einasto/cored, D982).
- A7b Wino line spectrum + Sommerfeld σv(M) [literature tables 1307.4400 / 2507.15934] → CTA sensitivity for the 0.66–0.80 TeV window (D736).
- A7c SERAPIS tensor background Ω_GW(f) with r = (4.6–5.7)e-4, n_t = −r/8 vs LISA/ET/DECIGO/BBO (D710 null re-derived with A2d).
- A7d Neutrino mass (Σm_ν = 0.0587 eV) in astrophysics: effect on halo mass function / σ8 through A4 and Janus-LT.
- A7e Sky Map / Star Mapper (Gaia DR3 stars in apps/skymap): physical stellar parameters (luminosity, radius, mass estimates) for the catalogued stars.
