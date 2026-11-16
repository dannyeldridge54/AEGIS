# PREREG D957: independent reproduction of SERAPIS-rho (v3.2 Sec. rho; D816 exact-MS values) with tools/serapis_calc (selftest must pass)
Model as published: along Re tau = 1/2, y >= sqrt3/2, phi = ln(y)/sqrt2; I_rho = ln(1+|j|^2/1728^2)/4pi (toolkit j: E4^3/Delta, full series, independent of the old 4-term q-expansion); L = -ln(2 y |eta|^4), L(rho) from the same code; V = I_rho^2/(I_rho^2+1) + eps (L - L(rho)), eps = 6e-5.
Reference (D816, exact MS, old code): N* = 46.09: n_s 0.9691, r 5.160e-4, alpha_s -9.87e-4; N* = 49.49: n_s 0.9722, r 4.672e-4, alpha_s -8.69e-4. Frozen band (D615): n_s 0.969-0.972, r 4.6-5.1e-4.
Checks first: L(rho) recomputed and compared with the old constant 0.340372354 (report the difference); L has an isotropic minimum at rho (Hessian ratio within 1e-3).
PASS (fixed now): at both N*: |n_s - ref| <= 5e-4, |r/ref - 1| <= 2%, |alpha_s/ref - 1| <= 10%.
FAIL otherwise: record; trace by reading theory/modular/rho_ms_d816.py; DEVIATIONS before any rerun.
Script theory/flux/repro_rho_d957.py; output field_tests/results/repro_rho_d957.txt.
