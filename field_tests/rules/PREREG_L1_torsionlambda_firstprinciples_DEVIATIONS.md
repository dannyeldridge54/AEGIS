# DEVIATIONS — PREREG_L1_torsionlambda_firstprinciples
D1 (before any output): crash — Recomb.z_star called self._tau (the module function name) instead of the bound
method self.tau. Fixed the name only.
D2 (after the first run printed V = FAIL): the validation line converted CAMB's DAstar with ×1000 ("Gpc") — wrong:
CAMB returns DAstar in Mpc (12.7 Mpc = D_M(z*)/(1+z*)); the printed CAMB D_M = 1.5e7 Mpc and l_A = 3.3e5 are that units bug,
not a physics mismatch. Fix: D_M,CAMB = DAstar·(1 + zstar) with no factor. The (a′)/(b) science lines do not use CAMB
and are unchanged; only the V comparison is regenerated.
