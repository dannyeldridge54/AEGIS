"""D325: does a Giudice-Masiero mu-term lift D293's obstruction? Uses D293's conditions minus the holomorphic mu condition.
GM: K ⊃ lam (T+Tb)^{-q} Hu Hd  ->  mu_phys ∝ m32 (2x)^{-q} / sqrt(Z_u Z_d) ∝ (2x)^{-q + (pHu+pHd)/2}; m32 x-independent (D292) -> q = (pHu+pHd)/2.
Also: size of the GS-induced change of the T kinetic metric (alpha shift). Exact algebra. AI-assisted."""
import sympy as sp, itertools, math
src = open("/home/claude/aegis/theory/review/weights_shield_d293.py").read().split("sol = sp.solve")[0]
ns = {}; exec(src, ns)
pQ,pU,pD,pL,pE,pHu,pHd,d = [ns[k] for k in "pQ pU pD pL pE pHu pHd d".split()]
eqs = [e for i, e in enumerate(ns["eqs"]) if i != 3]
sol = sp.solve(eqs, [pQ,pU,pD,pL,pE,pHu,pHd,d], dict=True)[0]
print("family (no holomorphic mu condition):", sol)
free = sorted({s for v in sol.values() for s in v.free_symbols}, key=str); print("free:", free)
best = None
R = [sp.Rational(k, 3) for k in range(-27, 28)]
for vals in itertools.product(R, repeat=len(free)):
    sub = dict(zip(free, vals)); full = {k: v.subs(sub) for k, v in sol.items()}; full.update(sub)
    m = max(abs(full[k]) for k in [pQ,pU,pD,pL,pE,pHu,pHd])
    if best is None or m < best[0]: best = (m, full)
print("smallest max|p| on a 1/3 grid:", best[0], {str(k): v for k, v in best[1].items()})
q = (best[1][pHu] + best[1][pHd]) / 2; print("GM weight q =", q)
# GS: 16pi^2/g^2 ⊃ delta ln(T+Tb) absorbed by a dilaton: K ⊃ -ln(S+Sb - (delta/16pi^2) ln(T+Tb)) [linear-multiplet form, normalisation f = S]
dl = abs(best[1][d]) / (16 * math.pi ** 2); X = 2 * 25 / (4 * math.pi)   # S+Sb = 2/g^2 at alpha_GUT = 1/25
print(f"GS strength delta/16pi^2 = {dl:.3f}; S+Sb = {X:.2f}; K_TTb shift ≈ (delta'/X)/(T+Tb)^2 -> effective alpha change ≈ {dl/(3*X):.4f}")
