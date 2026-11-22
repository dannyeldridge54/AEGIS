#!/usr/bin/env python3
"""D2124: proton-decay operator enumeration under Z4 (k=(0,1,1,1,1)) + suppression estimates."""
import itertools, math, json
k = (0, 1, 1, 1, 1)
F = {'F1': (1,-1,0,0,0), 'F2': (1,1,0,0,0), 'F3': (1,1,0,0,0)}
Rb = {'R1': (-1,0,1,0,0), 'R2': (-1,0,-1,0,0), 'R3': (-1,0,-1,0,0)}
z4 = lambda Q: sum(a*b for a, b in zip(k, Q)) % 4
add = lambda *Qs: tuple(sum(x) for x in zip(*Qs))
neg = lambda Q: tuple(-x for x in Q)
S22 = [(2,2,0),(2,0,2),(0,2,2),(2,1,1),(1,2,1),(1,1,2)]   # weights of S_(2,2)(C^3)
def content(names, w): return [n for n, m in zip(names, w) for _ in range(m)]
out = {'T1_FL4': [], 'T1_FR4': [], 'T2_kahler': []}
for lab, fam in (('T1_FL4', F), ('T1_FR4', Rb)):
    names = list(fam)
    for w in S22:
        c = content(names, w); Q = add(*[fam[n] for n in c])
        out[lab].append(dict(content=''.join(c), z4=z4(Q), dQ=Q, allowed=z4(Q) == 0, light_only=('1' not in ''.join(c))))
# Kahler F_L F_L Rbar^dag Rbar^dag : pairs (symmetric choice of 2 from F, 2 from R)
for f2 in itertools.combinations_with_replacement(list(F), 2):
    for r2 in itertools.combinations_with_replacement(list(Rb), 2):
        Q = add(F[f2[0]], F[f2[1]], neg(Rb[r2[0]]), neg(Rb[r2[1]]))
        out['T2_kahler'].append(dict(content=''.join(f2) + '|' + ''.join(r2) + '^dag', z4=z4(Q), dQ=Q, allowed=z4(Q) == 0))
# T3: B-L of components: F_L=(Q: 1/3, L: -1), Fbar_R=(u^c,d^c: -1/3, e^c,nu^c: +1). Any cubic F F Fbar_R contraction of SU(4) needs 4 4 4bar -> no singlet (4x4x4bar has no singlet).
out['T3'] = dict(SU4_trilinear_singlet='none: 4x4x4bar, 4x4bar x4bar contain no SU(4) singlet -> LLE, LQD, UDD absent',
                 Z2_matter_parity={n: (2*sum(a*b for a, b in zip(k, Q))) % 4 for n, Q in {**F, **Rb, 'bc(Higgs)': (0,1,-1,0,0)}.items()})
# T4 estimates
hbar = 6.582e-25; yr = 3.156e7; mp = 0.938; Ms = 8e12; aX = 1/24; a3 = 0.04; msusy = 1e3; tau_req = 1e34
G6 = aX**2*mp**5/Ms**4; tau6 = hbar/G6/yr
G5 = (a3/(4*math.pi))**2*mp**5/(Ms**2*msusy**2); tau5 = hbar/G5/yr
out['T4'] = dict(tau_dim6_O1_yr=tau6, eS_required_dim6=math.sqrt(tau6/tau_req), S_min_dim6=-math.log(math.sqrt(tau6/tau_req)),
                 tau_dim5_O1_yr=tau5, eS_required_dim5=math.sqrt(tau5/tau_req), S_min_dim5=-math.log(math.sqrt(tau5/tau_req)))
lightallowed = [d['content'] for d in out['T1_FL4'] + out['T1_FR4'] if d['allowed'] and d['light_only']]
out['light_Z4_allowed_dim5'] = lightallowed
out['ITEM14'] = 'PASS' if not lightallowed else 'CONDITIONAL (S >= %.1f for dim-5, %.1f for dim-6)' % (out['T4']['S_min_dim5'], out['T4']['S_min_dim6'])
print(json.dumps(out, indent=1, default=str))
