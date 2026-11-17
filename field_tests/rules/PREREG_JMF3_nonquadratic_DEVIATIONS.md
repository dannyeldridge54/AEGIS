# DEVIATIONS — JMF3 (written before any rerun; first run gave no scored model, both LISTED because MMC refused to run)
D1 (both models): MMC stopped M1 with "Need to set third derivative" — the running-of-running output (get_runningofrunning) needs V''' that
   MMC's case 3 does not code. Set get_runningofrunning = .false. for both models. Output option only; n_s and r are unaffected.
D2 (M2 axions): MMC stopped with "too many efolds before pivot" (634.9 e-folds from φ_init (8, 12); a_end underflows). Fix by a fixed rule,
   decided before any n_s/r is seen: step both φ_init components up by +1 together from (8, 12) until the Janus background (multifield.run)
   gives 70 ≤ N_tot ≤ 200; use the first such point for both codes. If no point up to (30, 34) qualifies, M2 is LISTED.
Claims, tolerances and everything else unchanged.
