#!/usr/bin/env python3
"""D2112: staged derivation checklist for the unique Z2xZ6' global PS model (1209.3010 Table 27)."""
import os, sys, math, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2z6p as Z, mpmath as mp
from fractions import Fraction as Fr
pm = lambda s: tuple(0 if c == '+' else 1 for c in s)
T27 = {'a': (4, (0,1,1,0,1,-1), '+++', (0,0,1), (1,1,1)), 'b': (2, (0,1,1,0,1,-1), '--+', (0,1,1), (1,1,1)),
       'c': (2, (0,1,1,0,1,-1), '-+-', (1,0,1), (1,1,1)), 'd': (2, (-1,2,2,-1,1,-1), '--+', (0,0,1), (1,1,1)),
       'e': (2, (1,0,1,0,1,0), '+--', (1,1,1), (1,1,0))}
C = {}; I = {}
for k, (N, w, z2, tau, sig) in T27.items():
    X, Y = Z.XY(w); ex = Z.exceptional(w, pm(z2), tau, sig); C[k] = (X, Y, ex); I[k] = Z.image(X, Y, ex)
R = {}
# K3
R['K3'] = {k: str(Fr(1, 2)*Z.chi(C[k], I[k])) for k in 'abcde'}
# K4 GS matrix
rows = []
for kk in (1, 2, 3):
    for a in (1, 2, 3): rows.append([C[x][2][kk][a][1] for x in 'abcde'])
    rows.append([Fr(C[x][2][kk][4][0] - C[x][2][kk][5][0]) + Fr(C[x][2][kk][4][1] - C[x][2][kk][5][1], 2) for x in 'abcde'])
    rows.append([C[x][2][kk][4][1] + C[x][2][kk][5][1] for x in 'abcde'])
PAPER = [[0,0,0,0,2],[0]*5,[0,0,0,-2,0],[2,0,-2,-3,-1],[0,0,0,2,-2],[0,0,0,0,-2],[0]*5,[0,0,0,2,0],[-2,2,0,3,1],[0,0,0,-2,2],
         [0]*5,[0]*5,[0]*5,[1,2,-1,-1,0],[-2,0,-2,2,0]]
ours = [[int(v) if Fr(v).denominator == 1 else str(v) for v in r] for r in rows]
exact = any(all(Fr(o)*s == p for ro, rp in zip(rows, PAPER) for o, p in zip(ro, rp)) for s in (1, -1))
perm = all(sorted(map(tuple, [[Fr(v) for v in r] for r in rows[5*s:5*s+5]])) == sorted(map(tuple, [[Fr(v) for v in r] for r in PAPER[5*s:5*s+5]])) or
           sorted(map(tuple, [[-Fr(v) for v in r] for r in rows[5*s:5*s+5]])) == sorted(map(tuple, [[Fr(v) for v in r] for r in PAPER[5*s:5*s+5]])) for s in range(3))
import numpy as np
Nv = np.array([4, 2, 2, 2, 2]); M = np.array([[float(Fr(v)) for v in r] for r in rows])*Nv
R['K4'] = {'ours': ours, 'exact_match': exact, 'match_up_to_row_perm_per_sector': perm, 'rank_ours': int(np.linalg.matrix_rank(M)),
           'rank_paper': int(np.linalg.matrix_rank(np.array(PAPER, float)*Nv))}
# K5 beta coefficients (multiplet counts incl. h.c.) from Tables 28+29
N = dict(a=4, b=2, c=2, d=2, e=2)
adj = dict(a=0, b=0, c=0, d=4, e=0); sym = dict(a=0, b=0, c=0, d=4, e=2); anti = dict(a=0, b=0, c=0, d=4, e=2)
bif = {('a','b'): 3, ('a','c'): 3, ('a','d'): 4, ('b','c'): 1, ('b','d'): 4, ('b','e'): 1, ('c','d'): 4, ('c','e'): 1, ('d','e'): 2}
def beta(x):
    s = N[x]*(-3 + adj[x]) + Fr(N[x], 2)*(sym[x] + anti[x]) + (sym[x] - anti[x])
    for (p, q), n in bif.items():
        if x == p: s += Fr(N[q], 2)*n
        if x == q: s += Fr(N[p], 2)*n
    return s
R['K5'] = {x: str(beta(x)) for x in 'abcde'}
# K6 thresholds, exact theta/eta. theta1(nu|tau) with nu-period 1: mpmath jtheta(1, pi*nu, q=e^{i pi tau})
def eta(v): q = mp.e**(-2*mp.pi*v); return q**(mp.mpf(1)/24)*mp.qp(q)
def Lh(v): return mp.log(abs(mp.jtheta(1, mp.pi/2, mp.e**(-mp.pi*v)))/eta(v))              # ln th1(1/2,iv)/eta
def Lt(v): return mp.log(mp.e**(-mp.pi*v/4)*abs(mp.jtheta(1, mp.pi*(-1j*v/2), mp.e**(-mp.pi*v)))/eta(v))
ln2 = mp.log(2)
def fa(v1, v2, v3):
    return sum(-Lh(v)/mp.pi**2 + 3*mp.log(eta(v))/(4*mp.pi**2) for v in (v1, v2)) - 3*Lt(v3)/(8*mp.pi**2) + mp.log(eta(v3))/(2*mp.pi**2)
def fbc(vm, vn, v3, literal):
    pref = 1/(2*mp.pi) if literal else 1/(2*mp.pi**2)
    return (-Lh(vm)/(4*mp.pi**2) + pref*mp.log(eta(vm)) - 3*Lh(vn)/(2*mp.pi**2) + mp.log(eta(vn))/mp.pi**2
            - Lt(v3)/(2*mp.pi**2) - mp.log(eta(v3))/(4*mp.pi**2) + ln2/(24*mp.pi**2))
asy_a = lambda v1, v2, v3: 5*(v1 + v2)/(48*mp.pi) - 7*v3/(96*mp.pi) - 2*ln2/mp.pi**2
asy_b = lambda vn, v3: vn/(6*mp.pi) - v3/(16*mp.pi) - 41*ln2/(24*mp.pi**2)
k6 = {'check_a_exact_vs_asym_at_(5,5,5)': [float(fa(5, 5, 5)), float(asy_a(5, 5, 5))],
      'check_b_corrected_vs_asym_at_(5,5,5)': [float(fbc(5, 5, 5, False)), float(asy_b(5, 5))],
      'check_b_literal_vs_asym_at_(5,5,5)': [float(fbc(5, 5, 5, True)), float(asy_b(5, 5))]}
for v3 in (2, 5, 10):
    for lit in (False, True):
        try: v = mp.findroot(lambda v: fa(v, v, v3) - fbc(v, v, v3, lit), 5*v3 + 5)
        except Exception as e: v = None
        k6['unif_v1=v2_at_v3=%d_%s' % (v3, 'literal' if lit else 'corrected')] = float(v) if v is not None else 'no root'
    k6['paper_printed_at_v3=%d' % v3] = float(4*v3 + 168*ln2/mp.pi)
    k6['paper_asymptotic_implies_at_v3=%d' % v3] = float(v3/4 + 7*ln2/mp.pi)
R['K6'] = k6
# K7 string scale
Cc = 1/(4*math.sqrt(4*math.pi)*(2*math.pi**2*math.sqrt(3))**1.5)
aem, s2, MZ = 127.951, 0.23122, 91.1876
a1, a2 = 0.6*(1 - s2)*aem, s2*aem
b = (33/5, 1, -3); L = 2*math.pi*(a1 - a2)/(b[0] - b[1]); MX = MZ*math.exp(L); aX = a2 - b[1]*L/(2*math.pi)
R['K7'] = {'C': Cc, 'MGUT_1loop': MX, 'alphaX_inv': aX}
for nm, MP in (('reduced', 2.435e18), ('nonreduced', 1.221e19)):
    Ms = Cc*MP/aX; R['K7']['Ms_needed_' + nm] = Ms; R['K7']['MGUT/Ms_' + nm] = MX/Ms
# K8 alpha_s one loop
def alphas(db, MT):
    if db is None: L = 2*math.pi*(a1 - a2)/(b[0] - b[1]); return 1/(a2 - b[1]*L/(2*math.pi) + b[2]*L/(2*math.pi))
    L1 = math.log(MT/MZ); bp = [b[i] + db[i] for i in range(3)]
    i1, i2 = a1 - b[0]*L1/(2*math.pi), a2 - b[1]*L1/(2*math.pi)
    L2 = 2*math.pi*(i1 - i2)/(bp[0] - bp[1]); aXi = i2 - bp[1]*L2/(2*math.pi)
    a3MT = aXi + bp[2]*L2/(2*math.pi); a3 = a3MT + b[2]*L1/(2*math.pi)
    return (1/a3 if a3 > 0 else 'nonperturbative (alpha3^-1=%.2f)' % a3), MT*math.exp(L2), aXi
# S2 decomposition (Y=(B-L)/2+T3R, GUT-normalised 3/5): bd+bd'+be' = 5 x (2_L,2_x): db2 += 5*2*1/2; cd+cd'+ce' = 5 x (2_R,2_x):
# 2x2 states Y=+-1/2 each -> sum Y^2 = 1 per multiplet; ad = 2 x [(4,2_d)+hc]: per (4,2): 2x[3 x (1/6)^2 + (1/2)^2] = 2/3, x2 (hc) x2 copies
dbY = 5*1 + 4*(2/3); db = (0.6*dbY, 5.0, 2*2*2*0.5)
s1 = alphas(None, None); s2r = alphas(db, 1000.0)
R['K8'] = {'S1_MSSM': s1, 'S1_pass': abs(s1 - 0.118) < 0.01, 'S2_db(1,2,3)': db, 'S2_alpha_s,MX,aXinv': s2r,
           'S2_pass': isinstance(s2r[0], float) and abs(s2r[0] - 0.118) < 0.01}
# K9 Yukawa instanton suppression (ESTIMATE)
R['K9'] = {'S_charm=ln(mt/mc)': math.log(171/0.62), 'S_up=ln(mt/mu)': math.log(171/0.00127)}
# K10 PS breaking Higgs search: reps listed in Tables 28/29 charged under (a,c) together with no other non-abelian charge
reps = ['ab', "ab'", 'ac', "ac'", 'bc', 'bd', "bd'", "be'", 'cd', "cd'", "ce'", 'dd', "dd'", "ee'", 'ad', "de'"]
R['K10'] = {'(4,1,2)-type sectors present (a and c only)': [r for r in reps if set(r.replace("'", '')) == {'a', 'c'}],
            'note': 'ac/ac\' are the right-handed families (3 chiral, no vector-like pair) -> no PS-breaking Higgs in spectrum'}
R['K11'] = {'U1_massless': 5 - R['K4']['rank_ours'], 'hidden_b': {x: R['K5'][x] for x in 'de'},
            'confining': [x for x in 'de' if Fr(R['K5'][x]) < 0]}
print(json.dumps(R, indent=1, default=str))
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'z2z6p_checklist_results.json'), 'w'), indent=1, default=str)
