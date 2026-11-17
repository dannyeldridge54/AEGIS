# PREREG S4b — 6D brane-SUSY-breaking tadpole: exponent check and 6D Dudas–Mourad-type vacuum
Locked 2026-11-17 before any S4b number.
(a) Symbolic check of γ_D = (D+2)/√(8(D−2)) (STRINGS_PLAN S4b note): for D = 4, 6, 10, take a conformally flat Euclidean
string-frame metric g_s = e^{4φ(x)/(D−2)}δ with φ = φ(x⁰); compute R_s directly from Christoffels (sympy); compare the
Euler–Lagrange operator of √g_s e^{−2φ}[R_s + 4(∂φ)²] with that of −k(∂φ)² (Einstein frame flat) to read off k; expect
k = 4/(D−2). Then γ_D = [(D+2)/(D−2)]/√(2k) with canonical φ_c = √(2k)φ. Pass: k and γ_D match the formula exactly for
D = 4, 6, 10 (γ_10 = 3/2 reproduces Dudas–Mourad, D996).
(b) (next step, same lock) 6D Einstein-frame R − ½(∂φ)² − 2α e^{√2 φ} with the S4a ansatz/solver (two routes as S4a/S4a2):
existence of a static solution with finite-length interval and its endpoint behaviour; record, no pass criterion beyond
the two routes agreeing to 1e-8.
