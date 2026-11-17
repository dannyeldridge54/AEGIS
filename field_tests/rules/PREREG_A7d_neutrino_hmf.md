# PREREG A7d (track X, Hyperion; AEGIS application; manual Djl 17 Nov 05:54 CT): SERAPIS's Σm_ν = 0.0587 eV in σ8 and the halo mass function (written before running)
Code: tools/janus_astro/hmf.py as committed with this lock (never run before it). Referees: CAMB 1.5.9 (pip) for P(k) and σ8; colossus for the Tinker et al. (2008) multiplicity (modelTinker08, Δ = 200m) and its own massFunction.
Cosmology: Planck 2018 best fit (H0 67.66, ω_b 0.02242, ω_c 0.11933, n_s 0.9665, A_s 2.105e-9); massive case: one massive eigenstate Σm_ν = 0.0587 eV (the frozen SERAPIS value = normal-ordering floor), Ω_m held fixed (ω_c lowered by ω_ν = Σm_ν/93.14 eV). Mass function uses P_cb and ρ_cb (Costanzi et al. 2013 convention).
Validation:
H1 σ8 by direct integration of CAMB's P_m vs CAMB's own σ8, both cosmologies: relative ≤ 2e-3.
H2 assembly check: our dn/dlnM using colossus's own (eisenstein98) σ(M) machinery inputs — i.e. our sigma_R on colossus's P(k) table, ρ_m, Tinker08 f — vs colossus massFunction(M, z = 0, mdef = '200m', model = 'tinker08', q_out = 'dndlnM') for M = 1e12, 1e13, 1e14, 1e15 M_⊙/h (colossus 'planck18' cosmology): relative ≤ 1e-2.
Pass H1–H2 → A7d machinery VALIDATED.
Application [computed]: Δσ8/σ8 (total matter and cb) and the ratio n(>M; 0.0587 eV)/n(>M; 0) at M = 1e13, 1e14, 1e15 M_⊙/h, z = 0; compared with the standard expectation ΔP/P ≈ −8 f_ν on small scales (f_ν = Ω_ν/Ω_m; reported, not scored).
Output field_tests/results/janus_astro_a7d.txt via theory/janus_astro/a7d_check.py. No reruns to chase; DEVIATIONS first.
