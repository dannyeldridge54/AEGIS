# PREREG Y4b — optimiser on the Y4 setup (T²/Z3 at omega, M = 9 SS 1/6 → M = 18)
Locked 21 Nov 2026 before running. Y4 sampled the Higgs directions only (D1790); this decides impossible vs unnatural.
- Same basis, eigenbases and selection rule as y4_oddflux.py (DEVIATIONS D1 applied). All 9 (class_L, class_R) pairs; Higgs = 6 complex components in the allowed class.
- Nelder–Mead on 12 real parameters, 40 starts per pair (seed 12), loss = (ln r12/4.84e-3)² + (ln r23/5.95e-2)².
- Verdict: HOSTED if the best fit is within 10 % on both ratios for some pair; FAIL (impossible at this flux) if it is worse than ×2 on either ratio for every pair; otherwise "between".
- Control: the same optimiser on the down-quark ratios (0.050, 0.0137) is reported alongside.
No rerun with other seeds or settings.
