# Janus String Calculator — goals (set by Danny, 16 Nov 2026): do everything ASPIC does, better, and prove it
Standing Jl-loop track "J". Every stage: lock first, two independent routes, reproduce the previous stage's limit, record a D-note. ASPIC claims are checked against its manual (cp3.irmp.ucl.ac.be/~ringeval/man/libaspic.html) before any comparison is stated.
- J0 DONE (D989): n_s, r validated on 32 points (24 SERAPIS + 8 textbook), ~4e4x faster than the exact solver.
- J0b IN PROGRESS: α_s vs exact solver (PREREG_D989, PC run); then Zenodo v1.0.
- J1 BUILT 16 Nov (tools/janus_calc/anyV.py; dev checks: Starobinsky, m²φ², φ⁴, exponential, T-model α=1 and 0.1, natural — formal locked validation folds into J7): Any potential: user gives V(φ) as a formula/string or callable (symbolic derivatives via sympy, numeric fallback); automatic start/end of inflation; no per-model code.
- J2 DONE (D995). Exact mode switch: every result can be re-run through the exact Mukhanov–Sasaki solver; report fast−exact gap.
- J3 DONE (D994): n_s median 1.6e-6 (×10 better). Third order: add the next slow-roll order (from the published third-order expressions, verified symbolically and numerically, never from memory); target |Δn_s| ~ 1e-6.
- J4 DONE (D995, N* exact to 1e-3). Reheating → observables in one call: self-consistent N* from (w_reh, T_R or ln R_rad) with the matching equation.
- J5 DONE (D995). Built-in error bars: truncation estimate (order-to-order) + fast/exact gap per result.
- J6 Two-field: DONE (D999 f_NL vs VW 0.6 %; D1000 NLO r 9e-5 VALIDATED; twofield.observe_multi). Next: T5 large-f_NL reference, isocurvature.
- J7 The jaw-drop benchmark: run Janus on ASPIC's full model list and match their published predictions model by model (Encyclopædia Inflationaris tables), plus everything they cannot do (modular plateaus, exact check, two-field, error bars, speed). Lock the comparison criteria before running.
Outreach is on hold (Danny, 16 Nov: wait 1–2 weeks); release versions to Zenodo as stages land (v1.0 = J0+J0b).
