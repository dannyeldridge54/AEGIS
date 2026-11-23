# SPEED-Zurvan result and DEVIATIONS, 2026-11-23 ~09:35 CT
Z1 FAILED as locked: worst 5.9e-5 relative (P3 sbottom/stau Sigma_d^d), 14.8x faster. The locked tolerance assumed the reference's
finite-difference error was 1e-7-1e-9; it is not: at P3 (scalars ~159 TeV) the float64 central difference loses digits to
roundoff (V ~ m^4 ~ 1e21 GeV^4). Diagnostic (not a locked test): a 50-digit mpmath central difference of Sigma_d^d(sbottom1) at
P3 agrees with the exact path to 1e-17, while the float64 reference is off by 6e-5; Richardson extrapolation of the float64
reference does not converge (7.8e-5), as expected for roundoff.
DEV-1: the exact eigenvalue derivative becomes Zurvan's primary path (more accurate and 14.8x faster); the finite-difference path
is kept as a cross-check and its stated accuracy in the docs is corrected (up to ~1e-4 at multi-hundred-TeV scales).
