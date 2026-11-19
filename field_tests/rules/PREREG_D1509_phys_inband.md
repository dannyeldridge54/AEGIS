# PREREG D1509 — tilt plan T3d: DILMIX in-band search in the PHYSICAL frame (λ = 1/9931)

Locked 2026-11-19 ~14:00 UTC before computing. Our own file and D-number. Model exactly as D1506 (after its DEVIATIONS D1): x = λ(E(½+iy,3/2) − E_ρ),
P = α x/(1+x) + (1 − α)(1 − 1/(1+x)²), g = P/(1 − P), V = P(1 + C g), λ = 1/9930.90 (D1505 benchmark (200, 1000); D1506 showed convergence in a), T_R 8.94e8.
Grid: α ∈ {0, 0.125, …, 1} (9) × C ∈ {1, 2, 3, 4, 6, 8, 12, 16}e-6 (8) = 72 points; fast SR (field_tests/scripts/d1506/phys_ns.py point()).
Output [estimate]: the in-band set (n_s 0.969–0.975, r 4.55–5.7e-4) and the needed C per α; failed points recorded, not fatal.
Expectation stated now: C larger than the λ = 1 strip's 1–2e-6; r higher at fixed n_s (D1506: +29–41 %), so in-band, if any, at small α.
Fixes only via PREREG_D1509_DEVIATIONS.md first. No reruns to chase.
