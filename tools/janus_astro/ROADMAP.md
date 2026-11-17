# Janus-Astro — astrophysics toolbox (track X; Danny 17 Nov 2026: "like we did to string theory", scope: all)
Pattern as Janus: fast route + independent second route or reference code; every stage locked before running; D-note; Zenodo versions as stages land.
- A0 DONE (D-note "Janus-Astro A0 validated"): Lane–Emden (exact n = 0, 1, 5; tables n = 1.5–4), Chandrasekhar mass, Eddington luminosity, Kelvin–Helmholtz time; TOV (exact Schwarzschild interior, Newtonian polytrope limit); Kerr ISCO, horizon; 0PN chirp, time to merger, cycles, strain; NFW/Einasto/Burkert (closed vs quadrature vs colossus); Kepler, escape, Hill, Roche lobe (numerical vs Eggleton); constants vs astropy. 9/9 PASS.
- A1 Realistic stars: main-sequence models with tabulated opacities and nuclear rates; mass–luminosity–radius vs MESA/MIST tracks.
- A2 Gravitational waves beyond 0PN: 3.5PN TaylorF2 phase, then a referee comparison with LALSuite/PyCBC waveforms; SNR and match for LIGO/ET/LISA noise curves.
- A3 Neutron stars: tabulated EoS (SLy, APR, …) → mass–radius, tidal deformability Λ; vs published tables and GW170817/NICER bounds.
- A4 Halos in cosmology: σ(M), mass functions (Press–Schechter, Sheth–Tormen, Tinker) and concentration relations vs colossus; links to Janus-LT growth.
- A5 Galactic dynamics: rotation-curve fits (SPARC), Jeans equation, orbits in Milky Way potentials vs galpy.
- A6 Benchmark: speed and accuracy vs the reference codes, plus things they don't do in one call.
