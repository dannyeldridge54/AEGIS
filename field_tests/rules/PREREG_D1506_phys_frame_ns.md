# PREREG D1506 — tilt plan T3c: n_s and r in the physical frame (λ = 1/a) vs the λ = 1 frame

Locked 2026-11-19 ~13:51 UTC before computing. Our own file and D-number.
Model exactly as the P3 pipeline convention (tools/serapis_calc/pipeline.py build: e = λ·(E − E_ρ) on the grid, tilt (1 + C·g/λ); DILMIX maps e → P/(1 − P)):
x = λ(E(½ + iy, 3/2) − E_ρ), P = α x/(1+x) + (1 − α)(1 − 1/(1+x)²), g = P/(1 − P), V = P·(1 + (C/λ)·g), φ = ln y/√2, T_R 8.94e8.
Points: DILMIX centre (α 0.375, C 1.5e-6) and form A A1 (α 1, C 1.25e-6) at λ = 1/a, a ∈ {1993, 9931, 49619} (D1505), plus λ = 1 (reference; must reproduce D1491/D1481).
Method: D1485 fast SR (Taylor-based flow parameters, exact background, shared Nstar), grid in y from just above the vacuum to y such that ≥ 200 e-folds exist.
Rule: per point, |Δn_s| ≤ 5e-4 and |Δr/r| ≤ 2 % vs λ = 1 ⇒ "λ = 1 frame adequate"; else "frame-dependent — P3 λ = 1 results need redoing in the physical frame".
Fixes only via PREREG_D1506_DEVIATIONS.md first. No reruns to chase.
