# PROM-5 deviations after R88 (1 MAJOR, 1 MINOR), written before the one rerun
- DEV-1 (MAJOR) the lock dropped ADAS PRB ("would double-count Z_eff bremsstrahlung"). Only partly true: PRB = recombination +
  bremsstrahlung, and at 5-15 keV Ar recombination exceeds its line radiation. Rerun uses impurity radiation
  P_imp = n_e n_imp [ sum_z f_z PLT_z + sum_z f_{z+1} PRB_z ] - C_B n_e n_imp <z^2> sqrt(T_e)   (the last term = the impurity part of the
  Z_eff bremsstrahlung S3 already counts). This is the quantity ITER's "line" most likely denotes (all impurity radiation beyond Z_eff
  bremsstrahlung) — assumed, not checked against the FDR text. Run-1 L2 FAIL stands as locked; D2196's "edge and/or W" reading is withdrawn.
- DEV-2 (MINOR) L_interp holds n_e = 1e20 m^-3 (pedestal/separatrix 4-8e19); labelled (89 data: SCD has no n_e dependence for Ar).
- DEV-3 W: the year-50 ADF11 files are the recommended W set; the catalogue and L4 switch W to year 50.
- DEV-4 PULSE-ELEMENTS C4: the four flags (He, F, Ne, Cl) sit at 1-2.7 eV where neutral emission switches on (exp(-E_exc/T));
  post-hoc C4' restricts the jump check to T > 5 eV; the locked C4 result stays recorded.
