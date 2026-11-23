# PROM-8 DEVIATIONS (written before the rerun). Locked run: A1 PASS (120 MW, 7.17 keV, Q 9.4), A2 PASS, A4 PASS.
Referee R91 (sonnet, read-only; scratch runs in /tmp): A1 passes as pre-registered but NOT like-with-like.
- DEV-1 (like-with-like; decisive) loss-power convention: our P_loss = P_alpha + P_aux - 0.6 P_rad,core (Lux, calibrated on ITER);
  Creely's POPCON P_loss is the power through the separatrix, ALL radiation excluded (H10). R91 scratch: all radiation subtracted ->
  60.6 MW / 5.65 keV (FAIL). Rerun uses the POPCON convention for SPARC (rad_C3 1.0, rho_core 1.0).
- DEV-2 (like-with-like) POPCON omits synchrotron (H9): rerun drops it for SPARC (f_reflect irrelevant; P_synch set 0).
- DEV-3 (label) A2 changes two things (He 6% -> 2.7% self-consistent, f_DT 0.85 -> 0.915): it is a "composition matters" check, not an
  ash-only check. Kept as can-fail; relabelled.
- Notes, no change: W coronal line ~2.9 MW vs POPCON average-ion (model difference; without W line 128.7 MW); ohmic 1.7 MW counted in heating
  as POPCON does; W fully stripped in Z_eff brems leaves a ~0.15 MW phantom (negligible); n_ped 2.7e20 is from arXiv:2502.00187 (pedestal top),
  T_ped 0.39<T> is an ITER carry-over (not SPARC data).
The locked A1 PASS stays on the record WITH this caveat. The like-with-like rerun result is the cycle verdict.
