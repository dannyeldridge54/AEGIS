# MATTER: does the Twist make the observed matter? (full calculation)

**Status: LOCKED** on Danny's word ("Start trsting them", 12 Nov 2026, 18:14 CT, replying to the pending draft rules), before any of its numbers were computed. Drafted:, written 12 Nov 2026 during the matter-formation work Danny asked for ("Start developing it",
"keep going", 17:25–17:42 CT). AI-assisted. Cloud.

**Why.** Developments 1–5 (doc "How matter formed: the Twist hypothesis"; `theory/matter/`) give an order-of-magnitude
route: the Barbero–Immirzi angle, rolling after inflation, couples to the fermion spin current with the derived
strength c_A = √(3/8) (Nieh–Yan; Mercuri 2009, Calcagni & Mercuri 2009). Neutrino-mass (Weinberg-operator) processes
turn the tilt into leptons, and sphalerons turn leptons into baryons. This rule fixes the full calculation before
it is run.

**Not blind.** Known at writing: the estimates in `twist_baryogenesis_estimates.py` and `chemical_balance.py`
(μ_ℓ/μ_A = 0.52; needed μ_A/T ≈ 2.2 × 10⁻⁸ at T_F ≈ 2 × 10¹³ GeV; needed φ̇ ≈ 1.9 × 10²⁴ GeV²). The calculation
below can only confirm or move these; it cannot be tuned, because its one free input (the starting speed) is
reported, not fitted.

## Target (fixed now)
n_B/s = 8.7 × 10⁻¹¹ (Planck + BBN), today.

## Calculation
- Boltzmann equation for n_(B−L)/s with the Weinberg-operator rate (thermal average, neutrino masses: normal ordering,
  lightest 0, oscillation values) and the source μ_A(T) = c_A φ̇(T)/M_P from a freely rolling angle,
  φ̇ ∝ a⁻³, from reheating T_RH down to the electroweak scale; sphaleron conversion 28/79 afterwards.
- The equilibrium coefficient from `chemical_balance.py` (gauge, top Yukawa, strong sphalerons; electroweak sphalerons
  off above 10¹² GeV), recomputed in each temperature band where the set of fast processes changes.
- Inputs scanned, not fitted: T_RH ∈ {10¹³, 3 × 10¹³, 10¹⁴, 10¹⁵} GeV; φ̇ at T_RH expressed as r = φ̇/(H M_P).

## Readings
- **K-TEMP (decides):** the minimum T_RH at which some r ≤ 0.3 gives the target.
  **VIABLE** if that T_RH ≤ 10¹⁵ GeV (below the CMB B-mode bound on the inflation scale); **NOT VIABLE** otherwise.
- **K-SPEED (reported):** the required r at each T_RH (a natural value is r ≲ 0.1).
- **K-GRAV (reported):** the gravitino yield at the minimum T_RH, and the gravitino mass above which it decays before
  BBN; the reading names which escape (Development 3) is then required.
- **K-KIN (reported):** the angle's peak share of the energy; above 1% it is flagged for the BBN energy bound.

## What may not happen
No change of target, rates, coupling (c_A is derived, not chosen), temperature bands or bands of the readings after
any number is computed. The direction of the roll (the sign of the result) is not predicted and is not claimed.

## Code
`theory/matter/boltzmann_leptogenesis.py` (to be written after the lock) → `field_tests/results/matter.json`.
