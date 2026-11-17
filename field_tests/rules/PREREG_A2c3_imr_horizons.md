# PREREG A2c3 (track X, Hyperion; manual Djl 17 Nov 06:06 CT): horizons with inspiral–merger–ringdown waveforms; resolve the D1063 flag (written before running)
Code: tools/janus_astro/gw_imr.py as committed with this lock (IMRPhenomD amplitude from lalsimulation on a log grid); distances, Θ distribution and range definition exactly as PREREG_A2c2 (Janus-LT + Planck18; Chen et al. 2017 range).
Validation:
D1 inspiral limit: IMRPhenomD optimal SNR for 1.4 + 1.4 M_⊙ at 100 Mpc on the aLIGO 175-Mpc curve (10 Hz–2048 Hz) vs A2c's 0PN SNR 32.707: relative ≤ 5e-2 (BNS SNR is inspiral-dominated; PN amplitude corrections and the post-ISCO tail allowed).
D2 grid: the same SNR with n = 3000 vs n = 12000 log points: relative ≤ 1e-3.
Pass D1–D2 → A2c3 VALIDATED.
Flag test (scored as the resolution of D1063's flag): with IMRPhenomD, the Cosmic Explorer (P1600143) 30 + 30 BBH horizon must exceed its 1.4 + 1.4 BNS horizon. If yes → the D1063 ordering was an inspiral-only artefact (flag RESOLVED); if no → the flag stays OPEN and the CE curve/definition is suspected.
Literature comparison (sourced, CE Horizon Study arXiv:2109.09882; qualitative, reported): CE gives access to BNS at z > 1 and to stellar-mass BBH beyond z ~ 10; A+ cannot see 50 + 50 BBH beyond z ~ 3. Note the study uses the 2021 40-km CE design; LAL's P1600143 is the 2017 CE curve.
Reported: horizons and ranges for A+, ET, CE — BNS 1.4 + 1.4, BBH 30 + 30, BBH 50 + 50 (A+).
Output field_tests/results/janus_astro_a2c3.txt via theory/janus_astro/a2c3_check.py. No reruns to chase; DEVIATIONS first.
