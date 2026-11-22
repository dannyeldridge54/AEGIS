#!/usr/bin/env python3
"""D2128: per-sector intersections and non-chiral multiplicities for the Table-27 model (HRS formulas)."""
import os, sys, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2z6p as Z
from fractions import Fraction as Fr
pm = lambda s: [0 if c == '+' else 1 for c in s]
T27 = {'a': (4, (0,1,1,0,1,-1), '+++', (0,0,1), (1,1,1)), 'b': (2, (0,1,1,0,1,-1), '--+', (0,1,1), (1,1,1)),
       'c': (2, (0,1,1,0,1,-1), '-+-', (1,0,1), (1,1,1)), 'd': (2, (-1,2,2,-1,1,-1), '--+', (0,0,1), (1,1,1)),
       'e': (2, (1,0,1,0,1,0), '+--', (1,1,1), (1,1,0))}
L = 'abcde'; N = {k: v[0] for k, v in T27.items()}
def brane(k):
    n, w, z, t, s = T27[k]; return dict(nm=[(w[0], w[1]), (w[2], w[3]), (w[4], w[5])], tz=pm(z), tau=list(t), sig=list(s))
def omega(B): return dict(B, nm=[(m, -(n + m)) for n, m in B['nm']])
def image(B): return dict(B, nm=[(n + m, -m) for n, m in B['nm']], tz=[(B['tz'][i] + B['sig'][i]*B['tau'][i]) % 2 for i in range(3)])
P = lambda v: 'o' if v % 2 else 'e'
def par(nm): return P(nm[0]) + P(nm[1])
CASE = {('oo','oo'):1, ('oe','oe'):1, ('eo','eo'):1, ('oo','oe'):2, ('oe','eo'):2, ('eo','oo'):2, ('oo','eo'):3, ('oe','oo'):3, ('eo','oe'):3}
def f(A, B, i):   # tab:Wilson_signs, torus i, relative Z2^(i) eigenvalue
    c = CASE[(par(A['nm'][i]), par(B['nm'][i]))]; sa, sb = A['sig'][i], B['sig'][i]; ta, tb = A['tau'][i], B['tau'][i]
    e = (-1)**(A['tz'][i] + B['tz'][i]); tab = (-1)**(ta + tb)
    if c == 1: return e*(1 + tab) if sa == sb else 0
    if c == 2: return e*{(0,0): 1, (0,1): tab, (1,0): (-1)**tb, (1,1): (-1)**ta}[(sa, sb)]
    return e*{(0,0): 1, (0,1): (-1)**ta, (1,0): tab, (1,1): (-1)**tb}[(sa, sb)]
def sector(A, B):
    Ii = [A['nm'][i][0]*B['nm'][i][1] - A['nm'][i][1]*B['nm'][i][0] for i in range(3)]; fs = [f(A, B, i) for i in range(3)]
    I = Ii[0]*Ii[1]*Ii[2]; IZ = [Ii[i]*fs[(i+1) % 3]*fs[(i+2) % 3] for i in range(3)]
    chi = Fr(-(I + sum(IZ)), 4); zero = [i for i in range(3) if Ii[i] == 0]
    if not zero: phi = Fr(abs(I + sum(IZ)), 4)
    elif len(zero) == 1:
        i = zero[0]; j, k = (i+1) % 3, (i+2) % 3; dd = int(A['sig'][i] == B['sig'][i] and A['tau'][i] == B['tau'][i])
        phi = Fr(dd, 2)*(abs(Ii[j]*Ii[k]) + (1 if Ii[j]*Ii[k] > 0 else -1)*fs[j]*fs[k])   # D2128 DEVIATION 2
    elif len(zero) == 3:
        phi = Fr(-1, 2)*sum(int(A['sig'][i] == B['sig'][i] and A['tau'][i] == B['tau'][i])*fs[(i+1) % 3]*fs[(i+2) % 3] for i in range(3))
    else: phi = None
    return chi, phi, len(zero)
Bn = {k: brane(k) for k in L}
pmz = lambda s: tuple(0 if c == '+' else 1 for c in s)
C = {k: (lambda X, Y: (X, Y, Z.exceptional(w, pmz(z), t, s, 'P2')))(*Z.XY(w)) for k, (n, w, z, t, s) in T27.items()}
Ci = {k: Z.image(*C[k]) for k in L}
R = {'P0_mismatch': [], 'pairs': {}}
for x in L:
    for y in L:
        for prime in (False, True):
            if x == y and not prime: continue
            Y0 = image(Bn[y]) if prime else Bn[y]; imgs = [Y0, omega(Y0), omega(omega(Y0))]
            secs = [sector(Bn[x], Yk) for Yk in imgs]
            chis = sum(s[0] for s in secs); eng = Z.chi(C[x], Ci[y] if prime else C[y])
            if chis != eng: R['P0_mismatch'].append((x, y + ("'" if prime else ''), str(chis), str(eng)))
            R['pairs'][x + y + ("'" if prime else '')] = dict(chi=str(chis), phi=str(sum(s[1] for s in secs)) if all(s[1] is not None for s in secs) else 'n/a',
                                                             sectors=[(str(s[0]), str(s[1]), s[2]) for s in secs])
R['adjoints'] = {x: str(abs(sector(Bn[x], omega(Bn[x]))[0])) for x in L}
tgt = {'ab': 1, "ab'": 2, 'ac': 1, "ac'": 2, 'bc': 1, 'bd': 1, "bd'": 3, "be'": 1, 'cd': 1, "cd'": 3, "ce'": 1, 'ad': None, "de'": 2}
p1 = []
for key, v in R['pairs'].items():
    if key[0] == key[1].rstrip("'") : continue   # xx' secondary
    a, b = key[0], key[1:]; canon = key if key in tgt else (b.rstrip("'") + a + ("'" if b.endswith("'") else '') if (b.rstrip("'") + a + ("'" if b.endswith("'") else '')) in tgt else key)
    want = tgt.get(canon, 0)
    if canon in ('ad', 'da'): continue
    if v['phi'] != str(want): p1.append((key, v['phi'], want))
R['P1_mismatch'] = p1; R['P2'] = R['adjoints']
R['P3_phi_ad'] = (R['pairs']['ad']['phi'], R['pairs']['da']['phi']); R['P4_phi_de_prime'] = R['pairs']["de'"]['phi']
R['VERDICT'] = dict(P0=not R['P0_mismatch'], P1=not p1, P2=R['adjoints'] == {'a': '0', 'b': '0', 'c': '0', 'd': '1', 'e': '0'}  # D2128 DEVIATION 1, P4=R['P4_phi_de_prime'] == '2')
print(json.dumps(R, indent=1, default=str))
