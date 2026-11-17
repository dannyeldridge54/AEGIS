# DEVIATIONS — PREREG_L1_torsionlambda_firstprinciples
D1 (before any output): crash — Recomb.z_star called self._tau (the module function name) instead of the bound
method self.tau. Fixed the name only.
D2 (after the first run printed V = FAIL): the validation line converted CAMB's DAstar with ×1000 ("Gpc") — wrong:
CAMB returns DAstar in Mpc (12.7 Mpc = D_M(z*)/(1+z*)); the printed CAMB D_M = 1.5e7 Mpc and l_A = 3.3e5 are that units bug,
not a physics mismatch. Fix: D_M,CAMB = DAstar·(1 + zstar) with no factor. The (a′)/(b) science lines do not use CAMB
and are unchanged; only the V comparison is regenerated.
D3 (after the second run, V still FAIL): D2's diagnosis was itself wrong. Checked directly in CAMB: DAstar = 13.8672 =
comoving_radial_distance(zstar)/1000, i.e. CAMB's DAstar is the COMOVING distance D_M(z*) in Gpc (angular_diameter_distance
is 12.71 Mpc). Correct conversion: D_M,CAMB = 1000·DAstar Mpc, no (1+z*) factor. Both earlier V lines are kept
(first run file and the second run in git history of janus_lt_l1_torsion.txt); only the V line changes.
