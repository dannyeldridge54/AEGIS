# PREREG D1419 — are band_e_audited's N* 50.07–51.22 (D1262) and D1234's corrected 49.88–50.64 the same physics?

Locked 2026-11-19 (UTC) before computing (JANUS tick 16, arithmetic only, no engine).
Inputs (read from the notes): D1234 (C 1.15e-6, SM g*): T_R 3e8 → N* 49.878, 3e9 → 50.642. D1262: MSSM g* shifts N* by −0.063;
box: C 1.0–1.3e-6, T_R 5.46e8–1.65e10 → N* 50.07–51.22.
Test: slope s = (50.642 − 49.878)/1 decade; compare with ln10/3 = 0.7675 (N* ∝ ⅓ ln T_R for matter-like reheating — stated as the
expectation, not used as input). Extrapolate D1234's line with the −0.063 MSSM shift to the box's T_R ends.
Rule: "same chain" if both ends agree with the box within 0.10 e-folds (the C spread 1.0–1.3e-6 is not modelled here, so this
tolerance is the budget for it); "conflict" if either end differs by more than 0.20; else "unclear". Arithmetic, recorded.
No reruns to chase results; fixes only via PREREG_D1419_DEVIATIONS.md written first.
