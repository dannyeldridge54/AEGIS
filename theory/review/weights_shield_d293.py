"""D293: can modular weights alone keep the Standard Model (MSSM) constants independent of x = Re T?
Conditions (generation-universal weights p_Q, p_U, p_D, p_L, p_E, p_Hu, p_Hd; K_r = (T+Tb)^{-p_r}):
 Yukawas: physical Y = e^{K/2} Y0 / (K K K)^{1/2} ∝ (2x)^{(p_i+p_j+p_k-3)/2} -> p_i + p_j + p_k = 3 for QUHu, QDHd, LEHd; mu-term: p_Hu + p_Hd = 3 (or mu = 0)
 Gauge (Kaplunovsky-Louis, coefficient of ln(T+Tb) in 16 pi^2 / g_a^2 must vanish up to a universal Green-Schwarz term delta k_a):
   -3 (sum_r T_a(r) - T(G_a)) + 2 sum_r T_a(r) p_r = delta * k_a   (k_3 = k_2 = 1, k_1 = 5/3 GUT normalisation)
Exact rational linear algebra (sympy). AI-assisted."""
import sympy as sp
pQ, pU, pD, pL, pE, pHu, pHd, d = sp.symbols("pQ pU pD pL pE pHu pHd delta")
# Dynkin indices per generation (x3) and Higgs; U(1)_Y uses (3/5)Y^2 with Y = hypercharge (Q=1/6,...)
ng = 3
T3 = {pQ: 2 * sp.Rational(1, 2), pU: sp.Rational(1, 2), pD: sp.Rational(1, 2)}           # SU(3): Q doublet of triplets -> 2 x 1/2
T2 = {pQ: 3 * sp.Rational(1, 2), pL: sp.Rational(1, 2)}; T2h = {pHu: sp.Rational(1, 2), pHd: sp.Rational(1, 2)}
Y = {pQ: (6, sp.Rational(1, 6)), pU: (3, sp.Rational(-2, 3)), pD: (3, sp.Rational(1, 3)), pL: (2, sp.Rational(-1, 2)), pE: (1, 1)}
Yh = {pHu: (2, sp.Rational(1, 2)), pHd: (2, sp.Rational(-1, 2))}
def gauge(Tmap, Th, TG):
    S = ng * sum(Tmap.values()) + sum(Th.values())
    P = ng * sum(v * k for k, v in Tmap.items()) + sum(v * k for k, v in Th.items())
    return -3 * (S - TG) + 2 * P
g3 = gauge(T3, {}, 3)
g2 = gauge(T2, T2h, 2)
T1 = {k: sp.Rational(3, 5) * n * y ** 2 for k, (n, y) in Y.items()}; T1h = {k: sp.Rational(3, 5) * n * y ** 2 for k, (n, y) in Yh.items()}
g1 = gauge(T1, T1h, 0)
eqs = [sp.Eq(pQ + pU + pHu, 3), sp.Eq(pQ + pD + pHd, 3), sp.Eq(pL + pE + pHd, 3), sp.Eq(pHu + pHd, 3),
       sp.Eq(g3, d), sp.Eq(g2, d), sp.Eq(g1, d * sp.Rational(5, 3) * 0 + d)]   # k_1 = 1 after 3/5 normalisation already applied
sol = sp.solve(eqs, [pQ, pU, pD, pL, pE, pHu, pHd, d], dict=True)
print("with mu-term and universal GS:", sol)
sol2 = sp.solve(eqs[:3] + eqs[4:], [pQ, pU, pD, pL, pE, pHu, pHd, d], dict=True)
print("without mu-term condition:", sol2)
sol3 = sp.solve([e.subs(d, 0) for e in eqs], [pQ, pU, pD, pL, pE, pHu, pHd], dict=True)
print("no GS term, with mu:", sol3)
