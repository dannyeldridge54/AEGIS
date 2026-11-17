"""S4b(a) (locked PREREG_S4b_6d_tadpole): Einstein-frame dilaton kinetic coefficient and tadpole exponent in D dims."""
import sympy as sp
x = sp.symbols('x'); phi = sp.Function('phi')(x); out = []
def ricci_conf(D, sig):
    X = sp.symbols(f'x0:{D}'); g = sp.diag(*[sp.exp(2*sig.subs(x, X[0]))]*D); gi = g.inv()
    Gam = [[[sum(gi[a, d]*(sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(D))/2
             for c in range(D)] for b in range(D)] for a in range(D)]
    Ric = lambda b, c: sum(sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c]) +
                            sum(Gam[a][a][d]*Gam[d][b][c] - Gam[a][c][d]*Gam[d][b][a] for d in range(D)) for a in range(D))
    R = sp.simplify(sum(gi[b, b]*Ric(b, b) for b in range(D)))
    return R.subs(X[0], x), g[0, 0].subs(X[0], x)
for D in (4, 6, 10):
    sig = 2*phi/(D - 2)                       # g_s = e^{2 sig} delta, e^{2 sig} = e^{4 phi/(D-2)}
    R, g00 = ricci_conf(D, sig)
    sqrtg = sp.exp(D*sig); dphi2 = sp.diff(phi, x)**2*sp.exp(-2*sig)   # (d phi)^2 with g_s^{-1}
    Ls = sqrtg*sp.exp(-2*phi)*(R + 4*dphi2)
    k = sp.symbols('k'); LE = -k*sp.diff(phi, x)**2
    EL = lambda L: sp.simplify(sp.diff(L, phi) - sp.diff(sp.diff(L, sp.diff(phi, x)), x) + sp.diff(sp.diff(L, sp.diff(phi, x, 2)), x, 2))
    ksol = sp.solve(sp.simplify(EL(Ls) - EL(LE)), k)
    tad = sp.simplify(sqrtg*sp.exp(-phi))   # tadpole density in Einstein frame
    expo = sp.simplify(sp.log(tad)/phi)
    kv = ksol[0] if ksol else None
    gam = sp.simplify(expo/sp.sqrt(2*kv)) if kv is not None else None
    form = sp.Rational(D + 2)/sp.sqrt(8*(D - 2))
    out.append(f"D={D}: k = {kv} (expect {sp.Rational(4, D-2)}); tadpole exponent in phi = {expo}; gamma_D = {gam} (formula {sp.nsimplify(form)}) match: {sp.simplify(gam - form) == 0 if gam is not None else False}")
    print(out[-1], flush=True)
open('field_tests/results/s4b_gamma.txt', 'w').write('\n'.join(out)+'\n')
