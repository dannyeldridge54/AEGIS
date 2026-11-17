# PREREG A5a (track X, Hyperion; manual Djl 17 Nov 05:57 CT): Milky Way potential and orbits vs galpy (written before running)
Why A5 not A7e: apps/skymap/data/stars.json has names, magnitudes, B−V and positions but no parallaxes, so stellar distances/luminosities need an external catalogue (not reachable from the shell); A7e is deferred.
Code: tools/janus_astro/galaxy.py as committed with this lock (never run before it). Parameters read from galpy's MWPotential2014 (Bovy 2015) objects; force laws implemented independently (formulas in the module docstring).
Tests:
G1 circular speed v_c(R), R = 0.5, 1, 2, 4, 8, 16, 30 kpc vs galpy vcirc(MWPotential2014): relative ≤ 1e-6.
G2 forces off the plane: (F_R, F_z) at (R, z) = (8, 1), (4, 0.5), (12, 3) kpc vs galpy evaluateRforces / evaluatezforces: relative ≤ 1e-6.
G3 v_c(8 kpc) = 220 km/s (the model's normalisation): relative ≤ 1e-4.
G4 orbit: (R, vR, vT, z, vz, φ) = (1, 0.1, 1.1, 0, 0.05, 0) natural units for 1 Gyr: energy drift (ours) ≤ 1e-8 relative; final (R, z) vs galpy Orbit.integrate(method = 'dop853_c'): |Δ| ≤ 1e-4 kpc.
Pass G1–G4 → A5a VALIDATED.
Application (AEGIS, reported): local dark-matter density ρ_DM(R₀ = 8 kpc) of MWPotential2014 in GeV/cm³, compared with the ρ_⊙ = 0.39 GeV/cm³ used for the wino J-factors (A7a/A7b); J ∝ ρ_⊙², so the wino fraction limits scale as f_max ∝ 1/ρ_⊙ (report the factor). Escape speed at R₀ (reported; literature value ~ 530–580 km/s from RAVE/Gaia stated as context only).
Output field_tests/results/janus_astro_a5a.txt via theory/janus_astro/a5a_check.py. No reruns to chase; DEVIATIONS first.
