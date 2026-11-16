# PREREG D771: P2 with exotic O3′ planes — which placements keep the SERAPIS-E tilt?
Locked 2026-11-16 before computing. Script: theory/modular/o3prime_d771.py. Output: field_tests/results/o3prime_d771.txt.
Inputs:
- 2405.18813: n_flux + 2n_D3 + n_O3′ = 32 (eq 3.8); odd flux quanta need exotic O3′ (App. A, no counts given); the minimum CP-violating n_flux = 12 (odd b₃), or 24 with all-even fluxes (f = ½, a⁰ = 4, b₃ = −6).
- D696: tilt ∝ N_eff = N − N0 for stuck stacks (N at each of the three half-periods of the inflaton torus, N0 at its origin); mobile D3s roll to the origin (D694), so n_D3 = 3N + N0 exactly.
- Assumption (stated): exotic O3′ planes must be spread EVENLY over the 4 fixed points of the inflaton torus (equal count on each 16-point slice of tori 2–3), so they add no U-asymmetry of their own. Hence n_O3′ ≡ 0 (mod 4). Uneven placements are listed but flagged as changing the tilt formula (not computed).
Enumerate n_O3′ ∈ {0, 4, …, 20} and n_flux ∈ {12, 24}; solve 3N + N0 = n_D3 = (32 − n_flux − n_O3′)/2 with N, N0 ≥ 0 integers. Keep N_eff ≥ 1 and report Im S·Im ρ = 750–975 × N_eff/4 (D696 scaling; ×½ for half-unit branes).
Decision:
- P2 SURVIVES (restricted) if at least one even-placement configuration with odd flux (n_O3′ > 0) has N_eff ≥ 1 and Im S·Im ρ ≥ 150.
- RETIRED if none does, and the all-even n_flux = 24 case also fails.
