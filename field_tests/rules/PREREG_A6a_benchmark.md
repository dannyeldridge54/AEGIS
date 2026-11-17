# PREREG A6a (track X, Hyperion; manual Djl 17 Nov 06:15 CT): speed and accuracy benchmark vs the referee codes (written before running)
Why A6a now: A2b2 needs the explicit 3PN spin–spin and 3.5PN spin phase terms; the sources found (arXiv:1601.05588, 1501.01529) are reachable only as rendered pages from which the fetch tool will not quote full equations (its quote-length limit), so the coefficients cannot be sourced this tick; A2b2 waits for a reachable table (e.g. the LAL source on GitHub via pip sdist, or Danny attaching the paper). A1 (realistic stars) needs opacity/nuclear tables not reachable from the shell. A6a uses only code already validated.
Same machine, same Python process, best of 5 repetitions, wall-clock (time.perf_counter):
T1 Milky Way circular speed at 1000 radii: Hyperion galaxy.MW.vcirc loop vs galpy vcirc(MWPotential2014, array).
T2 Halo mass function dn/dlnM (Tinker08, z = 0) at 50 masses: Hyperion (sigma_R on a P(k) table + colossus f) vs colossus massFunction(array).
T3 TaylorF2 3.5PN phase at 1e5 frequencies (1.4 + 1.4 M_⊙): Hyperion taylorf2_phase vs LAL SimInspiralChooseFDWaveformSequence (TaylorF2, same 1e5 frequencies; LAL also computes the amplitude — stated).
T4 Optimal SNR for 1.4 + 1.4 M_⊙ on a tabulated aLIGO 175-Mpc PSD: Hyperion snr_opt vs the same integral with LAL's TaylorF2 amplitude.
Accuracy check (scored): in each test the two codes' outputs agree within the tolerance already validated for that quantity (T1 1e-6, T2 1e-2, T3 phase residual after a + b f ≤ 1e-2 rad, T4 SNR 1e-3) → A6a VALIDATED. Speed ratios are reported, not scored; no claim beyond "on this machine".
Output field_tests/results/janus_astro_a6a.txt via theory/janus_astro/a6a_check.py. No reruns to chase; DEVIATIONS first.
