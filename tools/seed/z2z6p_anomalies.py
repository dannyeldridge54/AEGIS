#!/usr/bin/env python3
"""D2122: anomaly checks for the Table-27 PS model (P2)."""
import os, sys, itertools; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2z6p as Z
from fractions import Fraction as Fr
pm = lambda s: tuple(0 if c == '+' else 1 for c in s)
T27 = {'a': (4, (0,1,1,0,1,-1), '+++', (0,0,1), (1,1,1)), 'b': (2, (0,1,1,0,1,-1), '--+', (0,1,1), (1,1,1)),
       'c': (2, (0,1,1,0,1,-1), '-+-', (1,0,1), (1,1,1)), 'd': (2, (-1,2,2,-1,1,-1), '--+', (0,0,1), (1,1,1)),
       'e': (2, (1,0,1,0,1,0), '+--', (1,1,1), (1,1,0))}
L = 'abcde'; N = {k: v[0] for k, v in T27.items()}
C = {k: (lambda X, Y: (X, Y, Z.exceptional(w, pm(z), t, s, 'P2')))(*Z.XY(w)) for k, (n, w, z, t, s) in T27.items()}
I = {k: Z.image(*C[k]) for k in L}
# Table 28 chiral multiplets: (multiplicity, {stack: +1 fund / -1 antifund})
TAB = [(1, {'a': 1, 'b': -1}), (2, {'a': 1, 'b': 1}), (1, {'a': -1, 'c': 1}), (2, {'a': -1, 'c': -1}), (1, {'b': 1, 'c': -1}),
       (1, {'b': 1, 'd': -1}), (3, {'b': -1, 'd': -1}), (1, {'b': -1, 'e': -1}), (1, {'c': -1, 'd': 1}), (3, {'c': 1, 'd': 1}), (1, {'c': 1, 'e': 1})]
dim = lambda m, skip=(): eval('*'.join(str(N[s]) for s in m if s not in skip) or '1')
R = {}
# T1 SU(4)^3: sum over reps of (+/-1) * dim(others) for a-fundamentals
R['T1_SU4cubed'] = sum(mu*m['a']*dim(m, ('a',)) for mu, m in TAB if 'a' in m)
# T2 generalised U(N)^3
R['T2_generalised'] = {x: str(sum(N[a]*(Z.chi(C[x], C[a]) + Z.chi(C[x], I[a])) for a in L)) for x in L}
# T3 mixed U(1)_x - SU(N_y)^2
ft = {(x, y): Fr(sum(mu*m[x]*Fr(1, 2)*dim(m, (y,)) for mu, m in TAB if x in m and y in m and x != y)) for x in L for y in L}
geo = {(x, y): Fr(N[x], 2)*(Z.chi(C[x], C[y]) - Z.chi(I[x], C[y])) for x in L for y in L}
# field-theory diagonal (x=y): U(1)_x SU(N_x)^2 = sum q_x T(fund) dim(others), q_x=+-1
for x in L: ft[(x, x)] = Fr(sum(mu*m[x]*Fr(1, 2)*dim(m, (x,)) for mu, m in TAB if x in m))
R['T3_mismatches'] = [(x, y, str(ft[(x, y)]), str(geo[(x, y)])) for x in L for y in L if ft[(x, y)] != geo[(x, y)]]
R['T3_matrix_ft'] = {x: [str(ft[(x, y)]) for y in L] for x in L}
# T4 GS factorisation: coordinates. vec layout (X,Y,x_k,a..., y_k,a...)
def vec(c): X, Y, ex = c; return [Fr(X), Fr(Y)] + [Fr(ex[k][a][0]) for k in (1, 2, 3) for a in range(1, 6)] + [Fr(ex[k][a][1]) for k in (1, 2, 3) for a in range(1, 6)]
def basis_chi():
    B = []  # 16 odd cycles in (rho1,rho2,eps,epst) coefficient space == (X,Y,x,y) slots
    z = lambda: [Fr(0)]*32
    v = z(); v[0] = Fr(-1); v[1] = Fr(2); B.append(('0', v))
    for k in (1, 2, 3):
        for a in (1, 2, 3):
            v = z(); v[2 + 5*(k-1) + a - 1] = Fr(-1); v[17 + 5*(k-1) + a - 1] = Fr(2); B.append(('%d.%d' % (k, a), v))
        v = z(); v[2 + 5*(k-1) + 3] = Fr(1); v[2 + 5*(k-1) + 4] = Fr(-1); B.append(('%d.45a' % k, v))
        v = z(); v[17 + 5*(k-1) + 3] = Fr(1); v[17 + 5*(k-1) + 4] = Fr(1); v[2 + 5*(k-1) + 3] = Fr(-1, 2); v[2 + 5*(k-1) + 4] = Fr(-1, 2); B.append(('%d.45b' % k, v))
    return B
B = basis_chi()
import sympy
Mb = sympy.Matrix([[b[1][i] for b in B] for i in range(32)])
PAPER = [[0,0,0,0,2],[0,0,0,0,0],[0,0,0,-2,0],[2,0,-2,-3,-1],[0,0,0,2,-2],[0,0,0,0,-2],[0,0,0,0,0],[0,0,0,2,0],[-2,2,0,3,1],[0,0,0,-2,2],
         [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,2,-1,-1,0],[-2,0,-2,2,0]]   # rows: k=1..3 x (a1,a2,a3,45a,45b)
order = [i for i, b in enumerate(B) if b[0] != '0']
coef = {}; resid_ok = True
for xi, x in enumerate(L):
    d = sympy.Matrix([a - b for a, b in zip(vec(C[x]), vec(I[x]))])
    sol, params = Mb.gauss_jordan_solve(d)
    sol = sol.subs({p: 0 for p in params}); resid_ok &= (Mb*sol - d).is_zero_matrix
    coef[x] = [sol[i] for i in order]
ratios = set()
for xi, x in enumerate(L):
    for r, i in enumerate(range(15)):
        p = PAPER[r][xi]; c = coef[x][r]
        if p == 0 and c != 0: ratios.add('nonzero-vs-zero')
        if p != 0: ratios.add(sympy.nsimplify(c/p))
R['T4_exact_representation'] = bool(resid_ok); R['T4_ratios_coef/paper_c'] = sorted(map(str, ratios))
R['T4_universal_kappa'] = len(ratios) == 1 and 'nonzero-vs-zero' not in ratios
# T5 gravitational
R['T5_grav'] = {x: sum(mu*m[x]*dim(m) for mu, m in TAB if x in m) for x in L}
# T6 Witten: chiral doublets per SU(2)
R['T6_doublets'] = {x: sum(mu*dim(m, (x,)) for mu, m in TAB if x in m) for x in 'bcde'}
# T7 report
R['T7_U1cubed'] = {x: sum(mu*m[x]**3*dim(m) for mu, m in TAB if x in m) for x in L}
R['T7_U1xU1y2'] = {x + y: sum(mu*m[x]*m[y]**2*dim(m) for mu, m in TAB if x in m and y in m) for x in L for y in L if x != y}
v = dict(T1=R['T1_SU4cubed'] == 0, T2=all(R['T2_generalised'][x] == '0' for x in L), T3=not R['T3_mismatches'], T4=R['T4_universal_kappa'] and R['T4_exact_representation'],
         T5=all(R['T5_grav'][x] == 0 for x in L), T6=all(R['T6_doublets'][x] % 2 == 0 for x in 'bcde'))
R['verdicts'] = v; R['ITEM4'] = 'PASS' if all(v.values()) else 'FAIL'
import json; print(json.dumps(R, indent=1, default=str))
