# PREREG D955: independent reproduction of v3.2's main-branch predictions (Chronos, Kairos) with tools/serapis_calc (selftest must pass)
Model as published (v3.2 Sec. 2-4): along tau = i y (y >= 1), phi = ln(y)/sqrt2, I = ln(1+|j-1728|^2/1728^2)/4pi, I1 = ln(1+|j-1728|/1728)/4pi,
Chronos V = I^2/(I^2+1) + eps I1; Kairos eps = 0. N* counted exactly back from eps_H = 1; Bunch-Davies at k/aH = 200 (toolkit ms.py, 5-point stencil).
Published: Chronos eps = 1.3-1.6e-4, N* ~ 46-49: n_s 0.970-0.975, r 4.8-5.7e-4, y* 23-24.5, alpha_s -(8.8-10.2)e-4. Kairos: n_s 0.959-0.961, r 3.3-3.7e-4, y* 21.9-22.6.
Runs: Chronos (eps, N*) in {1.3e-4, 1.6e-4} x {46, 49}; Kairos N* in {46, 49}.
PASS (fixed now): Chronos corner n_s all in [0.9685, 0.9765] with min/max within 0.0015 of 0.970/0.975; r in [4.66e-4, 5.87e-4] (+-3%); y* in [22.7, 24.8]; alpha_s in [-11.2e-4, -7.9e-4] (+-10%). Kairos: n_s in [0.9575, 0.9625], r in [3.2e-4, 3.8e-4], y* in [21.6, 22.9].
FAIL otherwise: record, trace by reading the original scripts (DEVIATIONS before any rerun). Published numbers unchanged either way.
Script theory/flux/repro_chronos_d955.py; output field_tests/results/repro_chronos_d955.txt.
