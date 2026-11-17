# PREREG A2c2 (track X, Hyperion; manual Djl 17 Nov 06:02 CT): cosmological horizon and range for next-generation detectors (written before running)
Code: tools/janus_astro/gw.py theta_samples / snr_opt_z as committed with this lock; distances from Janus-LT (tools/janus_lt/background.py Cosmo, validated vs CAMB in D997) with astropy's Planck18 parameters (H0, Ω_b h², Ω_c h², Σm_ν = 0.06 eV, N_eff = 3.046, T_CMB 2.7255) — the cosmological model is Planck18, not SERAPIS.
Definitions (fixed now): optimal SNR with redshifted chirp mass M_c(1+z) and the inspiral cut at f_ISCO/(1+z), leading-order (0PN) amplitude; detection threshold SNR 8; horizon z_h where the optimal SNR = 8; range R = [3 V_eff/(4π)]^{1/3}, V_eff = ∫ dV_c/dz (1+z)^{-1} P_det(z) dz with P_det = fraction of Finn–Chernoff orientations with Θ/4 ≥ 8/ρ_opt(z) (the time-dilated sensitive comoving volume, as in Chen et al. 2017, arXiv:1709.08079 — definition cited, not fetched).
Tests:
C1 D_L(z) Janus-LT vs astropy Planck18 at z = 0.1, 1, 3, 10: relative ≤ 1e-4.
C2 Monte Carlo orientation factor ⟨(Θ/4)³⟩^{1/3} (1e6 samples) vs 1/2.2648: relative ≤ 3e-3.
C3 low-z consistency: the cosmological range for the aLIGO 175-Mpc curve (1.4 + 1.4 M_⊙) vs its Euclidean range from A2c (180.5 Mpc): relative ≤ 5e-2.
Pass C1–C3 → A2c2 VALIDATED.
Application (reported): z_h and R for A+ design, Einstein Telescope, Cosmic Explorer: BNS (1.4 + 1.4) and BBH (30 + 30, inspiral-only amplitude — a LOWER bound for heavy binaries whose merger is in band; stated).
Output field_tests/results/janus_astro_a2c2.txt via theory/janus_astro/a2c2_check.py. No reruns to chase; DEVIATIONS first.
