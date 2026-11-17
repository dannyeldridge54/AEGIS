# Janus String Calculator — goals (set by Danny, 16 Nov 2026): do everything ASPIC does, better, and prove it
Standing Jl-loop track "J". Every stage: lock first, two independent routes, reproduce the previous stage's limit, record a D-note. ASPIC claims are checked against its manual (cp3.irmp.ucl.ac.be/~ringeval/man/libaspic.html) before any comparison is stated.
- J0 DONE (D989): n_s, r validated on 32 points (24 SERAPIS + 8 textbook), ~4e4x faster than the exact solver.
- J0b DONE (D1003): Battery B α_s vs exact 8/8, ≤ 0.30 %; D981c replication converged.
- J1 BUILT 16 Nov (tools/janus_calc/anyV.py; dev checks: Starobinsky, m²φ², φ⁴, exponential, T-model α=1 and 0.1, natural — formal locked validation folds into J7): Any potential: user gives V(φ) as a formula/string or callable (symbolic derivatives via sympy, numeric fallback); automatic start/end of inflation; no per-model code.
- J2 DONE (D995). Exact mode switch: every result can be re-run through the exact Mukhanov–Sasaki solver; report fast−exact gap.
- J3 DONE (D994): n_s median 1.6e-6 (×10 better). Third order: add the next slow-roll order (from the published third-order expressions, verified symbolically and numerically, never from memory); target |Δn_s| ~ 1e-6.
- J4 DONE (D995, N* exact to 1e-3). Reheating → observables in one call: self-consistent N* from (w_reh, T_R or ln R_rad) with the matching equation.
- J5 DONE (D995). Built-in error bars: truncation estimate (order-to-order) + fast/exact gap per result.
- J6 Two-field: DONE (D999, D1000, D1001; observe_multi has per-field steps and a uniform-density end option, reproduces D1001 to 1e-6). Next: adiabatic-limit check; then J7 ASPIC.
- J7a DONE (D1002) and J7b DONE (D1004): real ASPIC built from GitHub; 17 models / 32 points vs exact MS: n_s ~350×, r ~320×, α_s ~50× more accurate (32/32). Next J7c reheating route; two-parameter ASPIC models.
- J7 The jaw-drop benchmark: run Janus on ASPIC's full model list and match their published predictions model by model (Encyclopædia Inflationaris tables), plus everything they cannot do (modular plateaus, exact check, two-field, error bars, speed). Lock the comparison criteria before running.
Outreach is on hold (Danny, 16 Nov: wait 1–2 weeks); release versions to Zenodo as stages land (v1.0 = J0+J0b).
