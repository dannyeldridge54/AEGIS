# DEVIATIONS for PREREG D1929 (written 21 Nov 2026 BEFORE the one rerun)
Run 1 was VOID by validation: the baseline gave α_s(unif) = 0.11420 against 0.1147 ± 5e-4, a miss of 5.0e-4.
Cause: the lock's baseline spectrum was mis-specified. The quoted 0.1147 comes from D1816's call weave_rg2({'m_gluino': 5565}), with the default wino 700 GeV and scalars 4.7e5 GeV. The lock instead used the later referee-corrected gluino of 4.93 TeV.
Fix: the baseline becomes {'m_gluino': 5565} (D1816's exact call). The heavy spectrum, the PASS rule and the code are unchanged. One rerun.
Run 1 output (heavy α_s = 0.11122) is kept as *_run1_VOID.*.
