# PREREG D960: alpha_s convergence in the Bunch-Davies start (follows D958)
Points: SERAPIS-E (paper convention) C = 1.0e-6, N* = 48.4; Chronos eps = 1.3e-4, N* = 46. Same models/code as D953/D955 (tools/serapis_calc; selftest must pass).
Runs: bd = k/aH at the mode start in {200, 1000, 5000}; 5-point +-0.1 stencil unchanged.
Converged value: alpha_s(5000), accepted as converged if |alpha_s(5000)/alpha_s(1000) - 1| <= 2%.
Outcomes (fixed now): if converged, compare with the published bands (SERAPIS-E -(9.4-10.6)e-4 at C 1.0-1.3e-6; Chronos -(8.8-10.2)e-4):
 - converged value inside the published band at this point's end of it, or within 5% of it -> "published alpha_s stands";
 - otherwise -> a correction note for the published alpha_s (frozen predictions are not edited; the correction is stated alongside).
If not converged at 5000: report, no rerun (a new lock with larger bd or a different method).
Script theory/flux/alpha_conv_d960.py; output field_tests/results/alpha_conv_d960.txt.
