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
def lens(J):
    if J is None: return None   # window
    u, s, vt = np.linalg.svd(J); r = int((s > 1e-3 * s.max()).sum()) if s.max() > 0 else 0
    return vt[:r].T            # n x r orthonormal basis; r = 0 -> OPAQUE (DEVIATIONS: blocks every direction)
def angles(A, B):
    if A.shape[1] == 0 or B.shape[1] == 0: return np.array([90.0])     # OPAQUE (DEVIATIONS)
    s = np.clip(np.linalg.svd(A.T @ B, compute_uv=False), 0, 1); return np.degrees(np.arccos(s))   # ascending angles
def klass(a): return 'PASS' if a < 15 else 'BENT' if a <= 75 else 'BLOCKED'
def reading(Jf):
    Ls = {L: lens(Jf(L)) for L in range(1, 10)}
    real = [L for L in range(1, 10) if Ls[L] is not None]
    pairs = [(real[i], real[i + 1]) for i in range(len(real) - 1)]
    tr = {}
    for a, b in pairs:
        ang = angles(Ls[a], Ls[b]); tr[f'{a}-{b}'] = dict(min_angle=round(float(ang.min()), 2), angles=[round(float(v), 2) for v in ang], cls=klass(ang.min()),
                                                        shared=[K[i] for i in range(n) if Ls[a].size and Ls[b].size and abs(Ls[a][i]).max() > 0.1 and abs(Ls[b][i]).max() > 0.1])
    P = np.eye(n)
    for L in range(1, 10):
        if Ls[L] is not None: P = (Ls[L] @ Ls[L].T) @ P
    C = np.zeros((9, 9))
    for j in range(1, 10):
        for k in range(1, 10):
            if Ls[j] is None or Ls[k] is None: C[j - 1, k - 1] = np.nan; continue
            C[j - 1, k - 1] = float(np.cos(np.radians(angles(Ls[j], Ls[k]).min())) ** 2)
    rows = {L: (None if Ls[L] is None else dict(r=Ls[L].shape[1], opaque=Ls[L].shape[1] == 0, dirs=[{K[i]: round(float(v[i]), 3) for i in range(n) if abs(v[i]) > 0.05} for v in Ls[L].T])) for L in range(1, 10)}
    off = np.where(np.eye(9) == 1, np.nan, C); rs = np.nansum(off, axis=1); hub = int(np.argmax(rs)) + 1
    return dict(lenses=rows, transfers=tr, chain_dim=int(np.linalg.matrix_rank(P, tol=1e-6)), chain_frac=round(float(np.linalg.norm(P) ** 2 / n), 4),
                C=[[None if np.isnan(v) else round(v, 3) for v in r] for r in C], hub=hub, hub_rowsum=round(float(rs[hub - 1]), 3))
R = {'R1_fd': reading(J_fd), 'R2_probe': reading(J_probe), 'R3_declared': reading(J_decl)}
# triangulate: agreement on r_k and on transfer classes
agree = {}
for L in range(1, 10):
    rs_ = [None if R[r]['lenses'][L] is None else R[r]['lenses'][L]['r'] for r in R]; agree[f'L{L}_r'] = dict(values=rs_, agree=len(set(rs_)) == 1)
for p in R['R1_fd']['transfers']:
    cs = [R[r]['transfers'].get(p, {}).get('cls') for r in R]; agree[f'T{p}'] = dict(values=cs, agree=len(set(cs)) == 1, verdict=cs[0] if len(set(cs)) == 1 else 'INDETERMINATE')
cls = [agree[f'T{p}']['verdict'] for p in R['R1_fd']['transfers']]
nb, nbl = cls.count('BENT'), cls.count('BLOCKED')
verdict = 'SUPPORTED' if (nb >= 2 and R['R1_fd']['chain_dim'] >= 1) else 'DECOUPLED' if nbl >= 5 else 'MIXED'
out = dict(prereg='PREREG_D1981_layer_lensing.md', knob_space=K, readings=R, triangulation=agree, transfer_classes=dict(zip(R['R1_fd']['transfers'], cls)), verdict=verdict)
json.dump(out, open('field_tests/results/d1981_lensing.json', 'w'), indent=1)
r1 = R['R1_fd']
for L in range(1, 10): print('L%d %-28s' % (L, NAMES[L]), 'WINDOW' if r1['lenses'][L] is None else ('OPAQUE (rank 0)' if r1['lenses'][L]['opaque'] else '') + 'lenses=%d %s' % (r1['lenses'][L]['r'], r1['lenses'][L]['dirs']), ' r(R1,R2,R3)=', agree[f'L{L}_r']['values'])
for p, t in r1['transfers'].items(): print('T%s %-8s min angle %6.2f  shared %s  triang %s' % (p, agree[f'T{p}']['verdict'], t['min_angle'], t['shared'], agree[f'T{p}']['values']))
print('chain: dim %d, fraction %.3f (R2 %d, R3 %d) | hub L%d rowsum %.2f (R2 L%d, R3 L%d) | VERDICT %s' % (r1['chain_dim'], r1['chain_frac'], R['R2_probe']['chain_dim'], R['R3_declared']['chain_dim'], r1['hub'], r1['hub_rowsum'], R['R2_probe']['hub'], R['R3_declared']['hub'], verdict))
print('C (R1):'); [print('  ', r) for r in r1['C']]
