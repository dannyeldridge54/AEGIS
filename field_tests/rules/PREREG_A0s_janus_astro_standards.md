# PREREG A0s (track X): Janus-Astro vs standard codes and standard values (written before running)
Request: Danny, 17 Nov 2026 05:21 CT, "Test it against standard". A0 (D1052) checked implementations against exact solutions; A0s checks against the field's standard software and canonical published numbers.
Code: tools/janus_astro as committed at D1052 (unchanged), plus a free-neutron-gas EoS written inside the check script (Oppenheimer–Volkoff 1939 test only). No reference value below has been compared with Janus-Astro output before this lock.
Standards: LALSuite 7/lalsimulation (pip lalsuite, LAL 8.0.1.1), galpy 1.12.1, colossus (planck18), astropy 8.0.2, and published numbers listed.
Script theory/janus_astro/a0s_check.py; output field_tests/results/janus_astro_a0s.txt. Cloud, seconds.

Tests and fixed pass criteria:
S1 GW chirp time vs LALSimulation SimInspiralTaylorF2ReducedSpinChirpTime(f, m1, m2, chi = 0, O = 0) (Newtonian order): (m1, m2) ∈ {(1.4, 1.4), (10, 10), (36, 29), (5, 50)} M_⊙, f ∈ {10, 20, 40} Hz: relative ≤ 1e-6.
S2 GW150914 chirp mass from the published source-frame masses 35.6 + 30.6 M_⊙ (GWTC-1): vs published 28.6 M_⊙: relative ≤ 5e-3 (rounding of the inputs).
S3 Halo circular velocity vs galpy NFWPotential (amp = 4π ρ_s r_s³ in M_⊙, a = r_s) and BurkertPotential (amp = ρ₀ in M_⊙/kpc³, a = r₀), r_s = 20 kpc, ρ_s = 5e6 M_⊙/kpc³, r ∈ {1, 8, 20, 100} kpc: relative ≤ 1e-4.
S4 Halo radius vs colossus mass_so.M_to_R(M, z = 0, '200c') for M = 1e10, 1e12, 1e15 M_⊙/h, using colossus's ρ_crit: relative ≤ 1e-6.
S5 Eddington luminosity, pure hydrogen (X = 1), 1 M_⊙: vs the standard 1.26e31 W: relative ≤ 1e-2.
S6 Kepler: Earth's sidereal year from a = 1.00000261 AU (J2000 EMB mean elements), M = M_⊙(1 + 1/328900.56): vs 365.256363 d: relative ≤ 5e-5 (planetary perturbations not modelled).
S7 TOV, Oppenheimer–Volkoff (1939) free neutron gas: maximum mass vs the standard 0.71 M_⊙: relative ≤ 2e-2.
S8 Chandrasekhar mass (μ_e = 2) vs the standard 1.44 M_⊙ quoted with μ_e = 2 and the Chandrasekhar–Milne constant (textbook): REPORTED ONLY, not scored (textbooks differ between 1.44 and 1.46 by constant choices; A0 T3 already scored 1.459).

Verdict: all of S1–S7 pass → A0s VALIDATED AGAINST STANDARDS; any fail → named, no rerun; fixes only via a DEVIATIONS file written first.
