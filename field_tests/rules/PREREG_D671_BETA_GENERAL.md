# PREREG D671: general closed form for the running of the running (DpL tick 4, Danny "Ddl" 11:36 CT)
Locked before computation, 2026-11-15. Script theory/modular/beta_general_d671.py; output results/beta_general_d671.txt.
Claim (by hand, leading order: β_s ≈ 2ηξ² + 2ϖ³, all other terms higher order in the slow-roll scale): for V ≈ 1 − Ae^{−pφ} + δe^{qφ}, κ = q/p,
  β_s = −¼(1 − n_s)³ (1+x)[(1 − κx)(1 + κ²x) + (1+x)(1 − κ³x)] / (1 − κx)³, with x from (n_s, r) as in D669.
Checks: SERAPIS (p = 2√2, κ = ½) equals D666's 128u⁶(1+x)(2x² − 5x − 16) (algebra in code, sympy); x = 0 gives −4/N³.
Numerical test: D669's Kallosh–Linde singular T-models (α = 1/3, γ = 1, β ∈ {1, ½}, δ ∈ {3e-6, 1e-5, 3e-5}, N ∈ {50, 55}) with exact first-order slow-roll β_s = −192ε³ + 192ε²η − 32εη² − 24εξ² + 2ηξ² + 2ϖ³; predict β_s from (n_s, r). PASS if |error| ≤ 15% at all converged points. No tuning.
