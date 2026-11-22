#!/usr/bin/env python3
"""D2120b addendum 2: unimodularity of F (saturation proof) + six-stack triviality classification of all survivors."""
import os, sys, itertools, math, pickle; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'z2z6p_Zn_exact.py')).read().split("Bf = lattice(2)")[0]; exec(src)
from sympy import Matrix
Bf = lattice(2); FB = basis_rows(Bf); pickle.dump(FB, open('/tmp/claude-0/F_basis.pkl', 'wb'))
G = Matrix([[omega(u, v) for v in FB] for u in FB]); print('rank F', len(FB), '| det Gram(omega) on F =', G.det(), '(unimodular => F = H3(Z))')
def Rmap(u): X, Y, ex = Z.image(*unvec(u)); return vec((X, Y, ex))
M = [[Rmap(b)[i] - b[i] for b in FB] for i in range(32)]; K = int_kernel(M)
E = [[sum(c[j]*FB[j][i] for j in range(len(FB))) for i in range(32)] for c in K]; print('rank E', len(E))
SIX = [(4, (1,0,1,0,1,0), '+++', (0,1,0), (1,1,0)), (2, (0,1,1,0,1,-1), '--+', (1,1,0), (1,1,0)), (2, (0,1,1,0,1,-1), '+--', (1,1,0), (1,1,0)),
       (4, (1,0,1,0,1,0), '-+-', (0,1,0), (1,1,1)), (2, (1,0,1,0,1,0), '+++', (0,1,0), (0,1,1)), (2, (1,0,1,0,1,0), '+--', (0,1,1), (0,1,0))]
Ns = [s[0] for s in SIX]; QZ = (0, 1, -1, 0, 1, 1)
S = [(N, vec((lambda X, Y: (X, Y, Z.exceptional(w, pm(z), t, s, 'P2')))(*Z.XY(w)))) for N, w, z, t, s in SIX]
W = [[int(N*omega(u, e)) for N, u in S] for e in E]
print('massless U(1)_Z check (Q_Z rows zero over E):', all(sum(q*r for q, r in zip(QZ, row)) == 0 for row in W))
bad_total = 0
for n in range(2, 9):
    surv = [k for k in itertools.product(range(n), repeat=6) if math.gcd(n, *k) == 1 and all(sum(a*b for a, b in zip(k, r)) % n == 0 for r in W)]
    # trivial group T_n = { sum_x m_x * (n/gcd(n,N_x)) e_x + t*QZ } mod n
    gens = [tuple((n // math.gcd(n, Ns[x])) if y == x else 0 for y in range(6)) for x in range(6)] + [tuple(q % n for q in QZ)]
    T = {tuple([0]*6)}; frontier = list(T)
    while frontier:
        new = []
        for t in frontier:
            for g in gens:
                s_ = tuple((a + b) % n for a, b in zip(t, g))
                if s_ not in T: T.add(s_); new.append(s_)
        frontier = new
    bad = [k for k in surv if k not in T]; bad_total += len(bad)
    print('n=%d survivors %d, non-trivial %d %s' % (n, len(surv), len(bad), bad[:4]))
print('SIX-STACK CRITERION:', 'PASS' if bad_total == 0 else 'FAIL')
