# PREREG D1418 — D1415's ρ offset model through exact Mukhanov–Sasaki, solved to A1's (n_s, r)

Locked 2026-11-19 (UTC) before computing (JANUS tick 15, node janus). Removes the slow-roll-order question of D1415/D1416.
Model (unchanged from D1415): V = (1 − 1/E₁)(1 + C(E₁ − 1)), E₁ = 2ζ(4)y² + B + πζ(3)/y, B = −4.7833, y = e^{√2 φ}.
Engine: apps/aegis_studio/engine/tools/serapis_calc/ms.py (Background, spectra; unchanged), M_P = 1, inflation ends at ε = 1.
Pivot: the mode exiting at the field value φ* (Nstar = N_end − N(φ*)). Solve (C, φ*) by Newton with finite differences,
≤ 6 iterations, start at D1415's (C 1.255e-6, y* 14.818), targets A1 n_s 0.974393, r 4.82095e-4; converged if |Δn_s| < 2e-6 and
|Δr/r| < 2e-4. Control: the same with B = D = 0 (pure plateau, start at D1415's C 1.248e-6, y* 14.613).
Rule: PASS if converged and |α_s/(−9.9814e-4) − 1| < 1 %; FAIL if converged and ≥ 1 %; "no result" if not converged in time
(CPU cap 150 s). Caveat stated now: the model is the large-y asymptotic form; its small-y end of inflation differs from the full
SERAPIS-E potential, which shifts N but not the local spectra at fixed (n_s, r).
No reruns to chase results; fixes only via PREREG_D1418_DEVIATIONS.md written first.
