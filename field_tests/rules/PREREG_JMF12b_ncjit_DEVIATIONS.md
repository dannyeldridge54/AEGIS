# DEVIATIONS — PREREG_JMF12b_ncjit.md
D1 (2026-11-18 00:38Z): D1 (before any scored number): case d (R=0.7) crashed in the reference (math domain error: the background has fewer than N*=55 e-folds, so N_end-55 < 0). Fix: wrap each case; a case whose reference or nc-jit raises, or whose N_tot < 65, is LISTED with the reason (same as the gate), not scored. Cases, gate and claim unchanged.
