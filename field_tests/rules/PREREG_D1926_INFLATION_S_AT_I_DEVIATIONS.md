# DEVIATIONS for PREREG D1926 (written 21 Nov 2026 BEFORE any rerun)
The first run was **VOID** by the lock's own validation rule. It gave E(ρ) = 8.9503 against 8.893 required to 1e-3. Its printed "PASS" is ignored: the script's verdict line left the validation out, which was a second bug.
Diagnosis, from an independent direct lattice sum Σ' y^{3/2}/|m+nτ|³ with the tail ∝ 1/R extrapolated:
- E(ρ) → 8.8927 and E(i) → 9.0336.
- The Fourier non-zero-mode coefficient must be 16π√y Σ N σ₋₂(N) K₁(2πNy) cos(2πNx), not 8π. The ±m modes were counted only once.
- With 16π the series gives 8.89275 and 9.03362, matching the lattice sum.
- The S-invariance check was trivial: both sides were reduced to the same point.
Fixes (no change to model, thresholds or rules):
1. 8π → 16π.
2. The S-invariance check compares E(τ) with E(−1/τ) evaluated directly, with no reduction.
3. The verdict requires the validation, as the lock already said.
One rerun only.
