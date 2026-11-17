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
