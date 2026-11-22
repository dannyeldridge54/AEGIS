#!/usr/bin/env python3
"""D1981 layer lensing / polarization map (PREREG_D1981_layer_lensing.md). 9 layers; lenses = right-singular directions of each layer's
margin Jacobian in the 5-knob space; transfers = principal angles to the next non-window layer; chain = product of projectors;
9x9 coupling matrix. Three readings: R1 finite differences, R2 random-probe regression, R3 the declared KNOBS_OF map."""
import json, math, sys
import numpy as np
src = open('tools/loom/resonance.py').read(); ns = {}; exec(src.split("out = {'sweeps'")[0], ns)
margins, KNOBS_OF, NAMES, D, LOG = ns['margins'], ns['KNOBS_OF'], ns['NAMES'], ns['D'], ns['LOG']
K = ['u', 'MN', 'm32', 'TR', 'split']; n = len(K)
def at(x):  # x: knob coordinates (ln for LOG knobs, raw for split) -> state
    return {k: (D[k] * math.exp(x[i]) if k in LOG else D[k] + x[i]) for i, k in enumerate(K)}
def mvec(x, L): m = margins(at(x))[L]; return np.array([m[a] for a in sorted(m)])
x0 = np.zeros(n)
def J_fd(L, h=1e-4):
    if not margins(at(x0))[L]: return None
    return np.column_stack([(mvec(x0 + h * e, L) - mvec(x0 - h * e, L)) / (2 * h) for e in np.eye(n)])
def J_probe(L, N=400, w=0.03, seed=1981):
    if not margins(at(x0))[L]: return None
    rng = np.random.default_rng(seed + L); X = rng.uniform(-w, w, (N, n)); f0 = mvec(x0, L)
    Y = np.array([mvec(x, L) - f0 for x in X]); return np.linalg.lstsq(X, Y, rcond=None)[0].T
def J_decl(L):
    if not margins(at(x0))[L]: return None
    return np.array([[1.0 if k in KNOBS_OF[L] else 0.0 for k in K]])
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from lens_core import lens, angles, klass, analyze, verdict as _verdict
def reading(Jf): return analyze(Jf, K)
R = {'R1_fd': reading(J_fd), 'R2_probe': reading(J_probe), 'R3_declared': reading(J_decl)}
# triangulate: agreement on r_k and on transfer classes
agree = {}
for L in range(1, 10):
    rs_ = [None if R[r]['lenses'][L] is None else R[r]['lenses'][L]['r'] for r in R]; agree[f'L{L}_r'] = dict(values=rs_, agree=len(set(rs_)) == 1)
for p in R['R1_fd']['transfers']:
    cs = [R[r]['transfers'].get(p, {}).get('cls') for r in R]; agree[f'T{p}'] = dict(values=cs, agree=len(set(cs)) == 1, verdict=cs[0] if len(set(cs)) == 1 else 'INDETERMINATE')
cls = [agree[f'T{p}']['verdict'] for p in R['R1_fd']['transfers']]
verdict = _verdict(cls, R['R1_fd']['chain_dim'])
out = dict(prereg='PREREG_D1981_layer_lensing.md', knob_space=K, readings=R, triangulation=agree, transfer_classes=dict(zip(R['R1_fd']['transfers'], cls)), verdict=verdict)
json.dump(out, open('field_tests/results/d1981_lensing.json', 'w'), indent=1)
r1 = R['R1_fd']
for L in range(1, 10): print('L%d %-28s' % (L, NAMES[L]), 'WINDOW' if r1['lenses'][L] is None else ('OPAQUE (rank 0)' if r1['lenses'][L]['opaque'] else '') + 'lenses=%d %s' % (r1['lenses'][L]['r'], r1['lenses'][L]['dirs']), ' r(R1,R2,R3)=', agree[f'L{L}_r']['values'])
for p, t in r1['transfers'].items(): print('T%s %-8s min angle %6.2f  shared %s  triang %s' % (p, agree[f'T{p}']['verdict'], t['min_angle'], t['shared'], agree[f'T{p}']['values']))
print('chain: dim %d, fraction %.3f (R2 %d, R3 %d) | hub L%d rowsum %.2f (R2 L%d, R3 L%d) | VERDICT %s' % (r1['chain_dim'], r1['chain_frac'], R['R2_probe']['chain_dim'], R['R3_declared']['chain_dim'], r1['hub'], r1['hub_rowsum'], R['R2_probe']['hub'], R['R3_declared']['hub'], verdict))
print('C (R1):'); [print('  ', r) for r in r1['C']]
