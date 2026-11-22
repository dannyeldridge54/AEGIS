#!/usr/bin/env python3
"""Seed v6 core: T6/(Z2xZ6'xOR) with discrete torsion, AAA lattice (1209.3010). Bulk X,Y (cyclic), exceptional wrappings
(full appendix table), orientifold images, twisted + bulk tadpoles, chiral intersections."""
from fractions import Fraction as Fr
import itertools
ETA = {1: -1, 2: -1, 3: -1}                     # eta_(k) = eta_OR * eta_ORZ2(k), eta_OR = -1
def XY(w):
    n = (w[0], w[2], w[4]); m = (w[1], w[3], w[5]); cyc = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    X = n[0]*n[1]*n[2] - m[0]*m[1]*m[2] - sum(n[i]*m[j]*m[k] for i, j, k in cyc)
    Y = sum(n[i]*n[j]*m[k] + n[i]*m[j]*m[k] for i, j, k in cyc)
    return X, Y
P = lambda v: 'O' if v % 2 else 'E'
# formulas (z = z_alpha, z0 = Z2^(i) eigenvalue sign)
F = {'nm': lambda n, m, z, z0: (z*n, z*m), 'm': lambda n, m, z, z0: (z*m, -z*(n + m)), 's': lambda n, m, z, z0: (-z*(n + m), z*n),
     'IIa': lambda n, m, z, z0: (-z0*n + (z - z0)*m, (z0 - z)*n - z*m), 'IIb': lambda n, m, z, z0: ((z0 - z)*n - z*m, z0*m + z*n),
     'IIc': lambda n, m, z, z0: (z*n + z0*m, -z0*n + (z - z0)*m)}
B1 = lambda sj, sk: (1 + sk*(3 + sj), 2 + sj*(3 - sk), 3 + sj + 2*sk - 3*sj*sk)
B2 = lambda sj, sk: (1 + sk*(2 + sj), 2 + sj*(2 - sk), 5 - 2*sj - sk + 3*sj*sk)
B3 = lambda sj, sk: (1 + sk*(4 - 2*sj), 2 + sj*(1 + 2*sk), 4 + sj - sk)          # alpha1 typo-corrected (see PREREG D2110)
TAB = {  # row (parity of n^j m^j n^k m^k): (block, {(sj,sk): [(formula, [alphas])]})
 'OOOO': (B1, {(0,0): [('m',[1,2,3])], (1,0): [('IIb',[1]),('nm',[5]),('s',[4])], (0,1): [('m',[4,5]),('IIb',[2])], (1,1): [('s',[5]),('nm',[4]),('IIb',[3])]}),
 'OEOE': (B1, {(0,0): [('nm',[1,2,3])], (1,0): [('IIa',[1]),('s',[5]),('m',[4])], (0,1): [('nm',[4,5]),('IIa',[2])], (1,1): [('m',[5]),('s',[4]),('IIa',[3])]}),
 'EOEO': (B1, {(0,0): [('s',[1,2,3])], (1,0): [('IIc',[1]),('m',[5]),('nm',[4])], (0,1): [('s',[4,5]),('IIc',[2])], (1,1): [('nm',[5]),('m',[4]),('IIc',[3])]}),
 'OEOO': (B2, {(0,0): [('nm',[1,5]),('m',[2])], (1,0): [('IIa',[1]),('s',[4]),('m',[3])], (0,1): [('nm',[3,4]),('IIb',[2])], (1,1): [('m',[4]),('s',[3]),('IIa',[5])]}),
 'EOOE': (B2, {(0,0): [('s',[1,5]),('nm',[2])], (1,0): [('IIc',[1]),('m',[4]),('nm',[3])], (0,1): [('s',[3,4]),('IIa',[2])], (1,1): [('nm',[4]),('m',[3]),('IIc',[5])]}),
 'OOEO': (B2, {(0,0): [('m',[1,5]),('s',[2])], (1,0): [('IIb',[1]),('nm',[4]),('s',[3])], (0,1): [('m',[3,4]),('IIc',[2])], (1,1): [('s',[4]),('nm',[3]),('IIb',[5])]}),
 'EOOO': (B3, {(0,0): [('s',[1,4]),('m',[2])], (1,0): [('IIc',[1]),('m',[3]),('nm',[5])], (0,1): [('s',[5,3]),('IIb',[2])], (1,1): [('nm',[3]),('m',[5]),('IIc',[4])]}),
 'OOOE': (B3, {(0,0): [('m',[1,4]),('nm',[2])], (1,0): [('IIb',[1]),('nm',[3]),('s',[5])], (0,1): [('m',[5,3]),('IIa',[2])], (1,1): [('s',[3]),('nm',[5]),('IIb',[4])]}),
 'OEEO': (B3, {(0,0): [('nm',[1,4]),('s',[2])], (1,0): [('IIa',[1]),('s',[3]),('m',[5])], (0,1): [('nm',[5,3]),('IIc',[2])], (1,1): [('m',[3]),('s',[5]),('IIa',[4])]}),
}
JK = {'P1': {1: (2, 3), 2: (3, 1), 3: (1, 2)}, 'P2': {1: (2, 3), 2: (1, 3), 3: (1, 2)}}
def exceptional(w, tZ2, tau, sig, jk='P1'):
    """w = (n1,m1,n2,m2,n3,m3); tZ2 = (t1,t2,t3) Z2 eigenvalue exponents; tau, sig per torus. Returns {k: {alpha: (x,y)}}"""
    out = {}
    for i in (1, 2, 3):
        j, k = JK[jk][i]; n, m = w[2*(i-1)], w[2*(i-1)+1]
        row = P(w[2*(j-1)]) + P(w[2*(j-1)+1]) + P(w[2*(k-1)]) + P(w[2*(k-1)+1])
        blk, cells = TAB[row]; sj, sk = sig[j-1], sig[k-1]; z0 = (-1)**tZ2[i-1]
        a1, a2, a3 = blk(sj, sk); zf = {a1: z0*(-1)**tau[j-1], a2: z0*(-1)**tau[k-1], a3: z0*(-1)**(tau[j-1] + tau[k-1])}
        d = {a: (0, 0) for a in range(1, 6)}
        for f, als in cells[(sj, sk)]:
            for a in als: d[a] = F[f](n, m, zf[a], z0)
        out[i] = d
    return out
def image(X, Y, ex):
    exi = {}
    for k, d in ex.items():
        e = {a: (0, 0) for a in range(1, 6)}
        for a, (x, y) in d.items():
            ap = {4: 5, 5: 4}.get(a, a); e[ap] = (-ETA[k]*(x + y), ETA[k]*y)
        exi[k] = e
    return X + Y, -Y, exi
def chi(A, B):
    (Xa, Ya, ea), (Xb, Yb, eb) = A, B
    s = sum(ea[k][a][0]*eb[k][a][1] - ea[k][a][1]*eb[k][a][0] for k in (1, 2, 3) for a in range(1, 6))
    return Fr(Xa*Yb - Ya*Xb - s, 4)
def tadpoles(stacks):
    """stacks: list of (N, (X,Y,ex)). Returns (bulk, list of twisted residuals) for AAA."""
    bulk = sum(N*(2*X + Y) for N, (X, Y, ex) in stacks); res = []
    for i in (1, 2, 3):
        eta = ETA[i]
        for a in (1, 2, 3):
            res.append(sum(N*(ex[i][a][0] - eta*(ex[i][a][0] + ex[i][a][1])) for N, (X, Y, ex) in stacks))
            res.append(sum(N*(1 + eta)*ex[i][a][1] for N, (X, Y, ex) in stacks))
        res.append(sum(N*((2*ex[i][4][0] + ex[i][4][1]) - eta*(2*ex[i][5][0] + ex[i][5][1])) for N, (X, Y, ex) in stacks))
        res.append(sum(N*(ex[i][4][1] + eta*ex[i][5][1]) for N, (X, Y, ex) in stacks))
    return bulk, res
