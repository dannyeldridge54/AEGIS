#!/usr/bin/env python3
"""D2120b: Z_n test on the exact integral even lattice E = F cap ker(R-1)."""
import os, sys, itertools, math, random; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2z6p as Z
from fractions import Fraction as Fr
pm = lambda s: tuple(0 if c == '+' else 1 for c in s)
VAR = [(t, tau, sig) for t in [(a, b, (a + b) % 2) for a in (0, 1) for b in (0, 1)] for tau in itertools.product((0, 1), repeat=3) for sig in itertools.product((0, 1), repeat=3)]
def vec(c): X, Y, ex = c; return [X, Y] + [ex[k][a][0] for k in (1, 2, 3) for a in range(1, 6)] + [ex[k][a][1] for k in (1, 2, 3) for a in range(1, 6)]
def unvec(u): ex = {k: {a: (u[2 + 5*(k-1) + a - 1], u[17 + 5*(k-1) + a - 1]) for a in range(1, 6)} for k in (1, 2, 3)}; return (u[0], u[1], ex)
def omega(u, v): return Z.chi(unvec(u), unvec(v))
def hnf_add(B, v):   # maintain row-echelon integer basis (dict pivot->row)
    v = list(v)
    for p in sorted(B):
        if v[p] == 0: continue
        r = B[p]
        while v[p] != 0:
            q = r[p] // v[p] if v[p] else 0
            r = [a - q*b for a, b in zip(r, v)]; r, v = v, r
            if v[p] == 0: break
        B[p] = r if r[p] > 0 else [-a for a in r]
    if any(v):
        p = next(i for i, x in enumerate(v) if x); 
        if p in B: return hnf_add(B, v)
        B[p] = v if v[p] > 0 else [-a for a in v]
def lattice(R, sample=None):
    B = {}; n = 0
    ws = [w for w in itertools.product(range(-R, R + 1), repeat=6) if all(math.gcd(w[2*i], w[2*i+1]) == 1 for i in range(3))]
    items = [(w, v) for w in ws for v in VAR]
    if sample: random.seed(2120); items = random.sample(items, sample)
    for w, v in items:
        X, Y = Z.XY(w); hnf_add(B, vec((X, Y, Z.exceptional(w, v[0], v[1], v[2], 'P2'))))
    return B
def basis_rows(B): return [B[p] for p in sorted(B)]
def int_kernel(M):   # M: list of rows (m x r); return integer basis of {c in Z^r : M c = 0}
    r = len(M[0]); cols = [[M[i][j] for i in range(len(M))] for j in range(r)]; U = [[int(i == j) for i in range(r)] for j in range(r)]
    piv_row = 0; done = 0
    for i in range(len(M)):
        while True:
            nz = [j for j in range(done, r) if cols[j][i] != 0]
            if len(nz) <= 1: break
            j0 = min(nz, key=lambda j: abs(cols[j][i]))
            for j in nz:
                if j == j0: continue
                q = cols[j][i] // cols[j0][i]
                cols[j] = [a - q*b for a, b in zip(cols[j], cols[j0])]; U[j] = [a - q*b for a, b in zip(U[j], U[j0])]
        nz = [j for j in range(done, r) if cols[j][i] != 0]
        if nz:
            j = nz[0]; cols[done], cols[j] = cols[j], cols[done]; U[done], U[j] = U[j], U[done]; done += 1
    return [U[j] for j in range(done, r)]
Bf = lattice(2); FB = basis_rows(Bf); print('rank F (|n,m|<=2):', len(FB))
Bs = dict(Bf); 
for w_v in [None]: pass
B3 = lattice(3, sample=20000); added = 0
for row in basis_rows(B3):
    before = {p: list(r) for p, r in Bs.items()}; hnf_add(Bs, row)
    if Bs != before: added += 1
print('saturation (|n,m|<=3 sample): basis changed by', added, 'vectors; same index' if added == 0 else '')
FB = basis_rows(Bs)
def Rmap(u): X, Y, ex = Z.image(*unvec(u)); return vec((X, Y, ex))
M = [[Rmap(b)[i] - b[i] for b in FB] for i in range(32)]          # (R-1) B as 32 x r
K = int_kernel(M); E = [[sum(c[j]*FB[j][i] for j in range(len(FB))) for i in range(32)] for c in K]
print('rank E (integral even):', len(E))
def run(name, stacks):
    S = [(N, vec((lambda X, Y: (X, Y, Z.exceptional(w, pm(z), t, s, 'P2')))(*Z.XY(w)))) for N, w, z, t, s in stacks]
    W = [[N*omega(u, e) for N, u in S] for e in E]
    assert all(x.denominator == 1 for r in W for x in r), 'non-integral'
    W = [[int(x) for x in r] for r in W]; out = {}
    for n in range(2, 9):
        surv = [k for k in itertools.product(range(n), repeat=len(S)) if math.gcd(n, *k) == 1 and all(sum(a*b for a, b in zip(k, r)) % n == 0 for r in W)]
        if surv: out[n] = surv
    print('==', name); [print('  Z_%d: %d primitive k, e.g. %s' % (n, len(s), s[:6])) for n, s in out.items()]
    return out
T27 = [(4, (0,1,1,0,1,-1), '+++', (0,0,1), (1,1,1)), (2, (0,1,1,0,1,-1), '--+', (0,1,1), (1,1,1)), (2, (0,1,1,0,1,-1), '-+-', (1,0,1), (1,1,1)),
       (2, (-1,2,2,-1,1,-1), '--+', (0,0,1), (1,1,1)), (2, (1,0,1,0,1,0), '+--', (1,1,1), (1,1,0))]
SIX = [(4, (1,0,1,0,1,0), '+++', (0,1,0), (1,1,0)), (2, (0,1,1,0,1,-1), '--+', (1,1,0), (1,1,0)), (2, (0,1,1,0,1,-1), '+--', (1,1,0), (1,1,0)),
       (4, (1,0,1,0,1,0), '-+-', (0,1,0), (1,1,1)), (2, (1,0,1,0,1,0), '+++', (0,1,0), (0,1,1)), (2, (1,0,1,0,1,0), '+--', (0,1,1), (0,1,0))]
o5 = run('five-stack (Table 27)', T27)
Yk = {'ac.bc.ab': (0,0,0,0,0), "ac'.bc.ab'": (0,2,-2,0,0), "ac.bc.ab'": (0,2,0,0,0), "ac'.bc.ab": (0,0,-2,0,0)}
for n, s in o5.items():
    print('  Z_%d Yukawa forbidden by some survivor:' % n, {y: any(sum(a*b for a, b in zip(k, q)) % n for k in s) for y, q in Yk.items()})
o6 = run('six-stack (cross-check vs 1303.6845 Table 5)', SIX)
