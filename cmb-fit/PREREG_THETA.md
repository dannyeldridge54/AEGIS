# The hilltop test: must the field start near its unstable peak? (rules written 2026-10-29 09:27 CT, before running)

Every Twist best fit starts the field near the top of its cosine hill: θ_i ≈ 2.78 rad ≈ 0.886π (π is the unstable
peak). Question: is a near-peak start *required* by the data, or merely allowed? Danny's idea ("keep a normally
unstable shape still") and a Kapitza-like holding mechanism would need it to be required.

## Runs
Free Twist (as edeP: f_EDE and z_c free, same data: Planck 2018 + DESI DR2 + Pantheon+) with θ_i FIXED at
1.50, 2.00, 2.40, 2.60, 2.95, 3.10 rad. Names `th<value>`, started from edeP's best point. The free-θ_i point
(edeP, θ_i = 2.784) is the reference.

## Rule
Δχ²(θ) = χ²(th θ) − χ²(edeP).
- **Hilltop required:** Δχ² ≥ 4 at θ_i = 2.00 and 1.50 (a start far from the peak is clearly worse).
- **Hilltop preferred:** 1 ≤ Δχ² < 4 at 2.00.
- **Not needed:** Δχ² < 1 at 2.00. Report the whole curve either way.
- Also report f_EDE and H0 along the curve: a lower θ_i may be traded for a larger f_EDE.

Tier: hypothesis. Known context, not ours: early-dark-energy fits in the literature generally prefer θ_i near π for
n = 3, so a "required" result confirms known behaviour. It becomes torsion-specific only if torsion predicts θ_i.
