<!-- AEGIS-FP 65DH4PPUGRHJQ6GO · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# PREREG D981: α_s from a wide ln k grid (follow-up to D974/D980; written before any run)
Motivation (D980, [estimate]): the α_s scatter is consistent with ~1e-6 per-mode noise in ln P amplified by the ±0.2 five-point stencil; a wider grid reduces that amplification by roughly (L_new/L_old)².
Solver: tools/serapis_calc/ms.py spectra(..., ic='ds'), unchanged code (degree-4 fit, deg = min(4, npoints-1)); selftest must pass.
Models/points exactly as PREREG_D960/D975: SERAPIS-E C = 1.0e-6, N* = 48.4; Chronos ε = 1.3e-4, N* = 46.
Grid W (main): dlnk = 9 points equally spaced on [-0.8, +0.8]. Grid M (bias check): 9 points on [-0.4, +0.4].
Runs: grid W at bd = 200, 1000, 5000; grid M at bd = 1000. α_s = 2 × (x² coefficient) at dlnk = 0 (as the code returns).
Converged if |α_W(5000)/α_W(1000) − 1| ≤ 2% AND |α_W(1000)/α_W(200) − 1| ≤ 2%.
Bias check passes if |α_W(1000)/α_M(1000) − 1| ≤ 3% (scale dependence over the wider range is not distorting α_s).
If converged AND bias passes: compare α_W(5000) with the published bands (SERAPIS-E −(9.4–10.6)e-4; Chronos −(8.8–10.2)e-4): inside or within 5% of an edge → "published α_s stands at this precision"; otherwise a correction note.
If either fails: report as NOT CONVERGED / BIASED; no rerun; a method change needs a new lock.
Script theory/flux/alpha_wide_d981.py; output field_tests/results/alpha_wide_d981.txt. Number D981 is the lock label; the result note gets the number the claim script returns.
