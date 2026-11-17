# PREREG A4 (track X, Hyperion; manual Djl 17 Nov 06:10 CT): growth, σ(M, z) and halo mass functions vs colossus (written before running)
Code: tools/janus_astro/hmf.py (sigma_R, unchanged since D1060) + tools/janus_lt/growth.py (growth, validated vs CAMB in D1027) with Janus-LT Cosmo matched to colossus 'planck18' (Ω_m 0.3111, Ω_b 0.049, H0 67.66, N_eff 3.046 massless, T_CMB 2.7255, flat); P(k, z = 0) table from colossus; σ(M, z) = σ(M, 0) D(z). Multiplicity functions taken from colossus (modelPress74, modelSheth99 with mdef 'fof'; modelTinker08 with '200m') — no coefficient retyped. Script theory/janus_astro/a4_check.py (never run before this lock).
Tests:
M1 growth D(z)/D(0): Janus-LT vs colossus growthFactor at z = 0.5, 1, 2, 5: relative ≤ 1e-3.
M2 dn/dlnM, our assembly (our σ, our growth) vs colossus massFunction(q_out = 'dndlnM'), models press74, sheth99, tinker08: z = 0 at M = 1e12, 1e13, 1e14, 1e15 M_⊙/h; z = 1 and 2 at 1e12, 1e13, 1e14 M_⊙/h: relative ≤ 2e-2 (the exponential tail amplifies the ≤ 1e-3 growth difference; stated).
Pass M1–M2 → A4 VALIDATED. Reported: the same comparison with colossus's own growth (isolates the growth contribution).
Output field_tests/results/janus_astro_a4.txt. No reruns to chase; DEVIATIONS first.
