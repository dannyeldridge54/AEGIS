# PREREG_FLAV_RHO5 — strong CP and CKM phase at the tie-off points (locked D1600, 2026-11-19 12:30 CT)
Structure: the standard A4 modular mass matrix M = diag(α,β,γ)·[[Y₁,Y₃,Y₂],[Y₂,Y₁,Y₃],[Y₃,Y₂,Y₁]] (weight-2 triplet, Feruglio 1706.08749), for up and down sectors, at τ = ρ and τ = i.
Compute: (a) arg det of the Y-matrix at ρ and at i (numerically, with the run-1 Y(τ)); (b) whether ρ and i are CP-symmetric points (τ ↦ −τ̄ maps them to SL(2,Z)-equivalent points); (c) with generalized CP (real α, β, γ): the set of allowed arg det(M_u M_d) and θ̄ = π − arg det; (d) whether a CKM CP phase can arise with all quark moduli at CP-symmetric points and real couplings (Jarlskog J of V = U_u† U_d for random real couplings, 2000 samples; report max |J|).
Pass rules: (c) θ̄ = 0 reachable by a discrete sign choice ⇒ "θ̄ quantised: PASS"; (d) max |J| > 1e-6 ⇒ CKM phase possible (PASS), else FAIL (no CP violation; observed J ≈ 3.1e-5).
Script: field_tests/scripts/flav_rho/run5.py.
