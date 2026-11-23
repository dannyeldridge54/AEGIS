- R89 (23 Nov 2026, PROM-6 devices): misses = T root + SPARC dilution proxy + ARC peaking; ARC tau_E target internally inconsistent; negative
  line radiation unclipped. -> DEV-1..5. Locked FAIL kept.
- R90 (23 Nov 2026, PROM-7 profiles): PASS with caveats; SPARC P2 pass rested on Z_eff 1.32 vs published 1.5 (Be proxy) -> DEV-1 (3He + Z9
  mix meets both); P1 near-unfalsifiable -> consistency check; ARC T_ped 4 keV; "marginal H-mode".
- R91 (23 Nov 2026, PROM-8 SPARC ash/composition): A1 pass not like-with-like (ITER-calibrated 0.6 P_rad,core vs POPCON all-radiation
  separatrix P_loss; synchrotron included vs omitted). -> DEV-1/2 rerun; A2 relabelled composition check.
- R92 (23 Nov 2026, PROM-9 tree): L1/L8/L3 stale goalposts (already corrected in FUSION-1 DEVs); L4 SPARC popcon branch matches cfspopcon
  (tau 0.674 vs 0.673 s at 7.3 keV) yet runs hot (218 MW): steep point, ~20-30% tau optimism amplified. No bug. -> DEV-1 relock, DEV-2 V/n/kappa_A.
- R93 (23 Nov 2026, N1 birth spectrum): sound; shift agreement within MC noise at 5 keV; B2/B4 weak; check FWHM definition -> DEV-1/2 rerun.
- R94 (23 Nov 2026, N3/N4 resonances): BUG - channel-spin sign of AJ ignored (Mn-55 l=1) -> 32% max error in an interference minimum; R3 336 eV
  unsourced (tape ER 340.79 eV). Agreement genuine (NJOY reconr grid). -> DEV-1/2 rerun.
- R95 (23 Nov 2026, N5 Doppler): holds; discriminating; second exponential untested (>1 eV) and thermal check self-referential; edge leak top ~100 eV.
  -> DEV-1 (extend to 1e-5 eV vs NJOY), DEV-2 (exclude top 200 eV).
- R96 (23 Nov 2026, N6-N8 transport): BUG Kalbach-Mann branches swapped (TBR-blind); T4 strawman -> yield-1 can-fail; 8 batches thin;
  "consistent with", not "validated"; target-at-rest is the main untested approximation.
- R97 (23 Nov 2026, N9/N10): no bug; He/dpa failure from the workshop steel's 5 wt% C (78% of He) -> Fe-only scoring; front cm 10.7 dpa/fpy/MWm2.
- R100 (23 Nov 2026, N11 activation): sound, no bug; goalposts weak (A4 tautology, A2 by half-life, A1 T-dependent); headline is the 0 s total.
- R101 (23 Nov 2026, N12): C1/C2 failures are my test errors (pump term omitted; hold = 1 + lambda I0/b, not t_d -> inf); idealised TBR margin ~1%.
- R102 (23 Nov 2026, JET-1 beam-target): model correct; J4 definition mismatch (FAIL stands; sigma peak 108 keV); thermal targets +12.5% (fair fix);
  open: fraction type (current vs power), losses, inputs n_i/n_e, E_b, Te -> overshoot is model+input, not a bug.
- R103 (23 Nov 2026, HARDEN-1): balance real but bookkeeping-only; B3 not independent (Li-6 MT205 == MT105) - not claimed.
