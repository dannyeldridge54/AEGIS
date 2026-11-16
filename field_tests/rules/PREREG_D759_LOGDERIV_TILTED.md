# PREREG D759: log-derivative Epstein plateau (D758) with the SERAPIS-E BHK tilt: n_s, r
Locked 2026-11-16 before computing. Script: theory/modular/logderiv_tilted_d759.py. Output: field_tests/results/logderiv_tilted_d759.txt.
D758's mpmath slow-roll was stopped (too slow). Its checks stand (V(ρ) = 0; E(ρ) = 5.7833593; plateau approach ∝ y^{−3} read from the printed values). D758's "approach exponent" and "V(i)" print lines were wrong (V∞ = 4 mis-set, and y = 1 sits on Re τ = ½, not at i). D759 supersedes its n_s and r.
## Model (fixed now)
V = y²·(d ln E/dy)²·(1 + C·(E − E(ρ))) along Re τ = ½, with E(½ + iy, 2) = 2ζ(4)y² + πζ(3)/y + Bessel terms. The Bessel terms are dropped for y ≥ 1.2 (size ≲ e^{−2π·1.2} ≈ 5e-4 relative; stated) and kept (10 terms) below.
Canonical field: α = 1 (y = e^{√2φ}) and α = 1/3 (y = e^{√(2/3)φ}).
C ∈ {0, 5e-7, 1e-6, 1.15e-6, 1.3e-6, 2e-6, 4e-6}; N* ∈ {48, 50, 52}.
## Decision
Report n_s, r, y*.
- CANDIDATE if some natural C (≤ 4e-6, i.e. effective volume product ≥ ~60N) puts n_s in 0.970–0.975 with y* ≤ 25.
- Otherwise record it as a new ladder rung (post-hoc; frozen bands unchanged).
