# PREREG D954: independent reproduction of v3.2 SERAPIS-E alpha_s with the upgraded solver
Solver: tools/serapis_calc/ms.py after the level-4 upgrade (5-point stencil +-0.1, quartic fit, rtol 1e-11); selftest must pass (power-law alpha_s = 0 to < 2e-5) before running.
Model and convention: exactly D953 run 2 (paper's E(U,2) = BHK lattice sum, E(rho,2) = 5.7833593; Re tau = 1/2; phi = ln y/sqrt2; V = Ehat/(Ehat+1)(1+C Ehat)).
Runs: (C, N*) in {1.0e-6, 1.3e-6} x {48.4, 49.9}; C = 0 at N* = 49.15.
PASS (same tolerances as D953): corner n_s in [0.969, 0.976] with min/max within 0.0015 of 0.970/0.975; r in [4.46e-4, 5.25e-4]; alpha_s in [-11.7e-4, -8.5e-4] (published -(9.4-10.6)e-4 +-10%); C = 0: |n_s - 0.961| <= 0.0015, |r/3.6e-4 - 1| <= 5%. Also report alpha_s from the D669 relation (p = 2 sqrt2, kappa = 1) at each corner.
FAIL otherwise; no rerun; DEVIATIONS first if anything is fixed.
Script theory/flux/repro_alpha_d954.py; output field_tests/results/repro_alpha_d954.txt.
