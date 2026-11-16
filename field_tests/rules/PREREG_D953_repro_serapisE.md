# PREREG D953: independent reproduction of v3.2's SERAPIS-E predictions with new code (tools/serapis_calc, selftest 14/14 required first)
Published (v3.2, doi:10.5281/zenodo.24289118, SERAPIS-E Predictions): C = (1.0-1.3)e-6, N* = 48.4-49.9: n_s = 0.970-0.975, r = (4.6-5.1)e-4, alpha_s = -(9.4-10.6)e-4; C = 0: n_s ~ 0.961, r ~ 3.6e-4.
Model as published: path Re tau = 1/2, phi = ln(y)/sqrt2, V = Ehat/(Ehat+1)(1 + C Ehat), Ehat = E(tau,2) - E(rho,2) (toolkit Fourier E, lattice-checked).
Runs: corners (C, N*) in {1.0e-6, 1.3e-6} x {48.4, 49.9}; plus C = 0, N* = 49.15.
PASS (fixed now): all four corner n_s in [0.969, 0.976] with computed min within 0.0015 of 0.970 and max within 0.0015 of 0.975; all corner r in [4.46e-4, 5.25e-4] (published range +-3%); all corner alpha_s in [-11.7e-4, -8.5e-4] (+-10%); C = 0: |n_s - 0.961| <= 0.0015 and |r/3.6e-4 - 1| <= 5%.
FAIL otherwise: then the discrepancy is recorded and traced (old script vs new) via a DEVIATIONS file before any rerun; the published numbers are not changed by this check either way.
Script theory/flux/repro_serapisE_d953.py; output field_tests/results/repro_serapisE_d953.txt.
