# PREREG_RW13_RHO_KNOT — RW12 repeated at the knot the repo's thread actually reaches (ρ, along Re τ = ½)
Locked 21 Nov 2026 before computing. AI-assisted. Script theory/tests/rw13_rho.py; result field_tests/results/rw13_rho.json.
Why: D1641/D1644 (lock + json "reaches_rho", a = 1.89; path along Re τ = ½) put the thread's end at ρ = e^{iπ/3}, while the
mirror table row 1 and the RW brief say i. RW12 tested i. Here the same model at ρ: τ = ½ + iy, k = 1 metric dφ = dy/(√2 y),
G(y) = ln(y |η(½ + iy)|⁴), y_ρ = √3/2. The Z₃ at ρ kills the gradient: check |dG/dy|(y_ρ) < 1e-10.
c = α_em·b/(4π)·|d²G/dφ²|(y_ρ), b ∈ {1, 12}. T1 = c·0.64²/2 < 1e-6; T2 = c·0.467 < 1.66e-6.
Verdict: PASS if both pass at b = 12; FAIL if T1 fails at b = 1; TENSION otherwise. (Only the Re τ = ½ direction is
used, as that is the thread's path; the Z₃ makes the Hessian isotropic, so this is the full curvature.)
