"""Kaplunovsky–Louis drift for a rolling field with K ⊃ −3 ln(X + X̄), MSSM content, matter metrics Z_r ∝ (X+X̄)^(−n_r).
16π² d(1/g_a²)/d ln x = −3 c_a + 2 Σ_r n_r T_a(r) − δ_GS   (c_a = Σ_r T_a(r) − T(G_a); universal GS shift δ, GUT normalisation).
Physical Yukawa ∝ x^(−3/2 + (n_i+n_j+n_k)/2); physical μ ∝ x^(−3/2 + (n_Hu+n_Hd)/2). AI-assisted."""
import sympy as sp
reps = ["Q", "u", "d", "L", "e", "Hu", "Hd"]
gen = {"Q": 3, "u": 3, "d": 3, "L": 3, "e": 3, "Hu": 1, "Hd": 1}
T = {  # Dynkin indices per family (U(1) GUT-normalised 3/5 Y^2 summed over components)
 "Q": (sp.Rational(1, 10), sp.Rational(3, 2), 1), "u": (sp.Rational(4, 5), 0, sp.Rational(1, 2)), "d": (sp.Rational(1, 5), 0, sp.Rational(1, 2)),
 "L": (sp.Rational(3, 10), sp.Rational(1, 2), 0), "e": (sp.Rational(3, 5), 0, 0), "Hu": (sp.Rational(3, 10), sp.Rational(1, 2), 0), "Hd": (sp.Rational(3, 10), sp.Rational(1, 2), 0)}
TG = (0, 2, 3)
b = [sum(gen[r]*T[r][a] for r in reps) - 3*TG[a] for a in range(3)]
print("b_a =", b)
n = {r: sp.Symbol("n_"+r) for r in reps}; dGS = sp.Symbol("delta")
drift = [-3*(sum(gen[r]*T[r][a] for r in reps) - TG[a]) + 2*sum(gen[r]*n[r]*T[r][a] for r in reps) - dGS for a in range(3)]
# 1) locality weights n=1 for all, no GS
sub1 = {**{n[r]: 1 for r in reps}, dGS: 0}
d1 = [sp.nsimplify(e.subs(sub1)) for e in drift]; print("weights=1: 16π² d(1/g²)/dln x =", d1, " equals −b_a:", d1 == [-x for x in b])
inv_aem = lambda dd: (dd[1] + sp.Rational(5, 3)*dd[0])  # 1/α_em = 1/α_2 + (5/3)/α_1 (GUT α_1)
k = sp.N(4*sp.pi*inv_aem(d1)/(16*sp.pi**2)); print("d(1/α_em)/d ln x =", k, "  d ln α_em/d ln x =", sp.N(-k/137.036))
# 2) can weights + universal GS cancel all three, with Yukawas and μ x-independent?
eqs = drift + [n["Hu"]+n["Q"]+n["u"]-3, n["Hd"]+n["Q"]+n["d"]-3, n["Hd"]+n["L"]+n["e"]-3, n["Hu"]+n["Hd"]-3]
sol = sp.linsolve(eqs, list(n.values())+[dGS]); print("full system (3 gauge + 3 Yukawa + μ):", sol)
sol2 = sp.linsolve(drift + eqs[3:6], list(n.values())+[dGS]); print("without μ condition:", sol2)
