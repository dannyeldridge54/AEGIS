# PROM-3 deviations from R86 (1 MAJOR, 4 MINOR), written before fixes
- DEV-1 (MAJOR M1) E3 used the S3 point at f_G 0.987, above the 0.94 cap E4 enforces. E3 is rebuilt on the best FEASIBLE point (E4) and the
  old number is kept, labelled "over Greenwald".
- DEV-2 (M2) house loads: ITER AC auxiliaries ~100 MW (cooling water 40, cryoplant 30, tritium plant 10, buildings 10; iter.org). Report P_net
  for P_other = 0, 50, 100 MW; the headline uses 100 MW.
- DEV-3 (M3) pumping: PROCESS DEMO A deposits 14 MW of pump power in the coolant (P_th 2072 MW incl.) — under 1% of P_th, not the 0.085
  helium simple-model fraction. The DEMO-style plant uses f_pump = 14/2058 with the pump power added to P_th; 0.085 is reported as a
  sensitivity row.
- DEV-4 (M4) the binding limit is computed: for the best P_aux, density is bisected to the exact edge where a limit first fails, and the
  limit is named.
- DEV-5 (M5) wording: "the dials pick P_aux = 50 of five allowed values and sit at the Greenwald cap; Q = 10 there follows from 500/50 and the
  S3 calibration to ITER, so this is partly circular, and the density (f_G 0.94) is above ITER's ~0.85."
- DEV-6 (F1 note) IPB99 at n_line 1.0e20 gives 48.5 MW (Snipes 2001: 49 MW for ITER-FEAT) — reported beside the model-point value.
- DEV-7 E1 relabelled: M = 1.345 is implied, not ARC data; ARC's 93 MW recirculation cannot follow this node's formula (38.6/0.4 alone = 96.5).
One rerun of PROM-3 (fast path, SPEED-fusion PASS).
