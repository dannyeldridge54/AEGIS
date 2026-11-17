# PREREG A0 (track X): Janus-Astro first validation battery (written before running)
Request: Danny, 17 Nov 2026 05:15 CT: "make an astrophysics calculator like we did to string theory", scope "toolbox of all of these" (stars, compact objects & GW, galaxies & dark matter, orbits).
Code: tools/janus_astro/ as committed with this lock (const, stars, compact, gw, halos, binaries). Disclosure: before this lock a smoke run checked only that each function executes (it printed Lane–Emden n = 1.5, a Kerr ISCO, a GW time, one TOV run, and one low-resolution Roche radius for q = 1, 0.3799); no reference was compared and no code was changed after it.
Referees: exact analytic solutions; independent numerical routes; Chandrasekhar (1939)/Horedt tables; astropy 8.0.2 constants; colossus (Diemer 2018) profiles.
Script: theory/janus_astro/a0_check.py; output field_tests/results/janus_astro_a0.txt. Cloud, minutes.

Tests and fixed pass criteria:
T1 Lane–Emden vs exact solutions n = 0, 1, 5: max |θ_num − θ_exact| over 200 points in [1e-3, min(ξ₁, 20)] ≤ 1e-9; ξ₁(0) = √6, ξ₁(1) = π to |Δ| ≤ 1e-9.
T2 Lane–Emden two routes (DOP853 rtol 1e-12 vs RK45 rtol 1e-10) for n = 1.5, 2, 3, 4: |Δξ₁|/ξ₁ and |Δω|/ω ≤ 1e-6; and vs tabulated (ξ₁, ω_n): n = 1.5 (3.65375, 2.71406), 2 (4.35287, 2.41105), 3 (6.89685, 2.01824), 4 (14.97155, 1.79723): relative ≤ 5e-6.
T3 Chandrasekhar mass (μ_e = 2): route A (ω₃ from the solver) vs route B (ω₃ = 2.01824): relative ≤ 1e-5; vs literature 5.836/μ_e² M_⊙ = 1.459 M_⊙: relative ≤ 5e-3.
T4 TOV: uniform-density stars at 2GM/(Rc²) = 0.1, 0.3, 0.6, 0.8 (ρ = 1e18 kg/m³), exact P_c from the Schwarzschild interior: TOV R and M vs exact, relative ≤ 1e-6. Newtonian limit: n = 1 polytrope (K = 1e-2 SI, ρ_c = 1e3 kg/m³; rest-mass density, 2GM/Rc² ~ 1e-10 scale) TOV vs Lane–Emden mass and radius: relative ≤ 1e-3.
T5 Kerr ISCO: closed form (BPT 1972) vs numerical minimum of E(r), a ∈ {0, 0.3, 0.5, 0.7, 0.9, 0.99}, prograde and retrograde: |Δr| ≤ 1e-5 (units GM/c²); exact limits r(0) = 6, r(1, pro) = 1, r(1, retro) = 9 to 1e-10.
T6 GW 0PN time to coalescence: closed form vs numerical integral of df/dt, M_c ∈ {1.2, 10, 30} M_⊙, f ∈ {10, 30, 100} Hz: relative ≤ 1e-8.
T7 Halos: closed-form vs quadrature enclosed mass for NFW, Einasto (α = 0.16, 0.3), Burkert at r/r_s ∈ {0.1, 1, 5, 20}: relative ≤ 1e-8. Referee colossus NFWProfile(rhos, rs) and EinastoProfile(rhos, rs, alpha) enclosed mass at the same radii (colossus units M_⊙/h, kpc/h used consistently): relative ≤ 1e-6.
T8 Roche lobe: numerical volume radius (96 × 192 rays) vs Eggleton (1983) fit for q ∈ {0.1, 0.3, 1, 3, 10}: relative ≤ 1e-2 (Eggleton's stated accuracy); resolution check 48 × 96 vs 96 × 192: relative ≤ 1e-3.
T9 Constants vs astropy: G, c, M_⊙, R_⊙, L_⊙, pc, and R_s(M_⊙): relative ≤ 1e-9.

Verdict: all of T1–T9 pass → A0 VALIDATED. Any fail → NOT VALIDATED for that quantity (named in the output); the rest stand. No reruns to chase; fixes only via PREREG_A0_janus_astro_DEVIATIONS.md written before any rerun. Timings reported, not scored.
