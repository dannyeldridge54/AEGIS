# PREREG R2 — full Kähler structure of the Green–Schwarz tilt (follows D1010)
Locked 2026-11-17 before the sympy run.
K = −ln Y − 3 ln(2 Im T), Y = S + S̄ − δ L, L = −ln(2 Im T |η(T)|⁴) (2212.03876 Eq. C.1 with −i(T−T̄) = 2 Im T).
Checks (sympy, symbolic; η enters only via ln|η|⁴ = ln η² + ln η̄², harmonic, so ∂_T∂_T̄ ln|η|⁴ = 0 is used and also
verified numerically at one point with mpmath to 1e-12):
K1: K_TT̄ = 3/(4 y²) + δ/(4 y² Y) + δ²|L_T|²/Y² (y = Im T) — symbolic identity check.
K2: K_SS̄ = 1/Y², K_ST̄ = −δ L_T̄ /Y² · (−1)… (record the exact symbolic forms).
K3 (numbers): with δ/Y = 1.2e-4 (D1009: δ/(2ReS) = 6e-5), the relative kinetic correction δ/(3Y) and
δ²|L_T|²/(Y² K⁰_TT̄) at y = 4.4–26.7 (the last 60 e-folds, D1007a); claim: both < 1e-4 → canonical-field change negligible.
K4 (structure): Ã = K^{SS̄}|F̃_S|²/|Ω|² with F̃_S = Ω_S − Ω/Y (C.2): show symbolically that Ã depends on T only through Y,
so its L-dependence is linear at O(δ L/Y): the Ã-term adds a tilt ∝ L with a model-dependent O(1) coefficient c_A = −Y ∂_Y Ã
(relative to the e^K tilt). Report form only; c_A needs a specific Ω(S).
Outcome recorded as derived/computed; no pass/fail beyond K1 identity and the K3 < 1e-4 claim.
