<!-- AEGIS-FP EQP7P5GOSX4VULFQ · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# PREREG J6d — large-f_NL comparison on uniform-density slices during slow roll (follows J6c NOT VALIDATED)

Locked 2026-11-17 after J6c's result (J6c stays NOT VALIDATED as recorded) and before any J6d number.
Reason: Byrnes–Choi–Hall Eq. 21 is a slow-roll result evaluated on a final uniform-density slice; J6c compared it
with δN to ε_H = 1, where slow roll fails and the paper itself reports f_NL changing again (Sec. V.1: rise at
N ≈ 30, decrease from N ≈ 45, rise again near N ≈ 58 in fast roll). J6d tests the δN code against Eq. 21 where
Eq. 21 is valid.

Method: same potential, cases A1–A3 and formulas as PREREG_J6c. Final slice = uniform density ρ_c = 3H², with ρ_c
taken from the fiducial trajectory (from φ*, χ*) at N_c = 30, 45, 55 e-folds after the start. δN: N from the
perturbed start (slow-roll velocity) to the first crossing of ρ = ρ_c; same anisotropic steps and halved pair.
Eq. 21 end quantities ^e evaluated at the fiducial point on that slice.

Tests: T7 every case and every N_c: |f_num − f_Eq21| < 0.10 |f_Eq21| or < 0.02 absolute (whichever larger).
T7L: at least one (case, N_c) has |f_NL| ≥ 1. T8 convergence h vs h/2 < 2e-2 relative (or 1e-3 absolute).
Verdict VALIDATED iff T7, T7L, T8 pass; INCONCLUSIVE if only T7L fails; else NOT VALIDATED.
Fixes only via PREREG_J6d_large_fNL_slices_DEVIATIONS.md before any rerun.
