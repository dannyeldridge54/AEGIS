"""D2168 weave_core: one engine = scales (margins) + fingerprint (Jacobian) + compass + lenses + per-node optimisation.
Nodes are the D2156 VN resonance margins (unchanged equations). python3 tools/loom/weave_core.py"""
import math, time, json, sys, os
PC = time.perf_counter
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lens_core import lens
src = open(os.path.join(HERE, 'resonance_d2156.py')).read()
src = src[:src.index("out = dict(variant=VAR")]            # definitions only (no breathing loop)
G = {'__name__': 'weave_core_import', '__file__': os.path.join(HERE, 'resonance_d2156.py')}
sys.argv = ['x', 'VN']; exec(compile(src, 'resonance_d2156.py', 'exec'), G)
margins, D = G['margins'], dict(G['D'])
DIALS = ['u', 'MN', 'm32', 'TR', 'split', 'dNeff']; LOG = {'u', 'MN', 'm32', 'TR'}
def to_state(z):
    s = dict(D)
    for j, k in enumerate(DIALS): s[k] = D[k] * math.exp(z[j]) if k in LOG else D[k] + z[j]
    return s
def nodes(z):
    st = to_state(z); m = margins(st); out = {}
    for L, d in m.items():
        if isinstance(d, dict):
            for name, v in d.items(): out[f'L{L}.{name}'] = float(v)
    out['L10.dNeff_nonneg'] = 100 * min(st['dNeff'], 0.0)        # DEV-2.4
    return out
t0 = time.time()
z0 = np.zeros(len(DIALS)); base = nodes(z0); names = list(base); m0 = np.array([base[n] for n in names])
def vec(z):
    try: b = nodes(z); return np.array([b[n] for n in names])
    except (ZeroDivisionError, ValueError, OverflowError): return np.full(len(names), -1e6)   # DEV-1
t1 = PC(); h = 1e-3
J = np.array([(vec(z0 + h*e) - vec(z0 - h*e)) / (2*h) for e in np.eye(len(DIALS))]).T     # nodes x dials
t_fp = PC() - t1
jd = DIALS.index('dNeff')
for i, n in enumerate(names):                                   # DEV-2.1: log-floor kink rows
    if n in ('L10.negspace_dNeff_ACT', 'L8.spine_BBN_dNeff', 'L10.dNeff_nonneg'): J[i, jd] = 0.0
Jn = J / np.where(np.linalg.norm(J, axis=0) > 0, np.linalg.norm(J, axis=0), 1)
lz = lens(J)
compass = {}
for i, n in enumerate(names):
    g = J[i]; nrm = np.linalg.norm(g)
    if nrm < 1e-12: compass[n] = dict(direction=None, note='no dial moves this node (data-fixed or TRUST)'); continue
    d = g / nrm; hurt = [names[k] for k in range(len(names)) if k != i and J[k] @ d < -1e-9 and m0[k] >= 0]
    compass[n] = dict(direction={DIALS[j]: round(float(d[j]), 3) for j in range(len(DIALS)) if abs(d[j]) > 1e-3}, hurts=hurt)
hold = [i for i in range(len(names)) if m0[i] >= 0]
SMOOTH = [j for j, k in enumerate(DIALS) if k != 'split']
def solve_node(i, split_on):
    best = None
    def full(zs):
        z = np.zeros(len(DIALS)); z[SMOOTH] = zs
        if split_on: z[DIALS.index('split')] = 1e-3
        return z
    cons = [{'type': 'ineq', 'fun': (lambda zs, i=i: vec(full(zs))[i])}] + [{'type': 'ineq', 'fun': (lambda zs, k=k: vec(full(zs))[k])} for k in hold]
    rng = np.random.default_rng(i)
    for s_ in range(5):
        x0 = rng.normal(0, 0.3, len(SMOOTH)) if s_ else np.zeros(len(SMOOTH))
        r = minimize(lambda zs: float(zs @ zs), x0, method='SLSQP', constraints=cons, bounds=[(-3, 3)]*len(SMOOTH), options={'maxiter': 300, 'ftol': 1e-10})
        if not r.success: continue
        zs = np.where(np.abs(r.x) < 1e-6, 0.0, r.x); z = full(zs); v = vec(z)          # DEV-2.2
        if v[i] >= -1e-6 and all(v[k] >= -1e-6 for k in hold) and (best is None or r.fun < best[0] - 1e-9): best = (r.fun, z, v)
    return best
opt = {}
for i, n in enumerate(names):
    if m0[i] >= 0: continue
    b0 = solve_node(i, False); b1 = None if b0 else solve_node(i, True)
    best = b0 or b1
    if best is None:
        opt[n] = dict(verdict='NOT CLOSABLE BY DIALS', margin=round(float(m0[i]), 4)); continue
    st = to_state(best[1]); spent = [k for k in DIALS if (abs(st[k]/D[k] - 1) > 0.01 if k in LOG else abs(st[k] - D[k]) > 1e-9)]
    payers = [names[k] for k in hold if best[2][k] < m0[k] - 0.05]
    opt[n] = dict(verdict='CLOSABLE' if b0 else 'CLOSABLE ONLY WITH THE SPLIT STEP (a fit by construction)', margin=round(float(m0[i]), 4),
                  move={k: round(float(best[1][j]), 4) for j, k in enumerate(DIALS) if abs(best[1][j]) > 1e-4}, fits_spent=spent, who_pays=payers)
movable = [i for i in range(len(names)) if np.any(np.abs(J[i]) > 1e-6)]          # DEV-3 joint readout
joint = {}
for split_on in (False, True):
    def fz(w, split_on=split_on):
        z = np.zeros(len(DIALS)); z[SMOOTH] = w[:-1]
        if split_on: z[DIALS.index('split')] = 1e-3
        return z
    cons = [{'type': 'ineq', 'fun': (lambda w, k=k: vec(fz(w))[k] - w[-1])} for k in movable]
    rng = np.random.default_rng(7); best = None
    for s_ in range(5):
        w0 = np.append(rng.normal(0, 0.3, len(SMOOTH)) if s_ else np.zeros(len(SMOOTH)), -5.0)
        r = minimize(lambda w: -w[-1], w0, method='SLSQP', constraints=cons, bounds=[(-3, 3)]*len(SMOOTH) + [(-50, 50)], options={'maxiter': 500, 'ftol': 1e-10})
        if r.success and (best is None or -r.fun > best[0] + 1e-9): best = (-r.fun, r.x)
    if best is None: joint['split_on' if split_on else 'split_off'] = 'no solution'; continue
    z = fz(best[1]); z[np.abs(z) < 1e-6] = 0.0; v = vec(z); st = to_state(z)
    joint['split_on' if split_on else 'split_off'] = dict(
        t_star=round(float(best[0]), 4), move={k: round(float(z[j]), 4) for j, k in enumerate(DIALS) if abs(z[j]) > 1e-4},
        holding=[names[k] for k in range(len(names)) if v[k] >= -1e-6], failing={names[k]: round(float(v[k]), 4) for k in range(len(names)) if v[k] < -1e-6},
        worse_than_start={names[k]: [round(float(m0[k]), 4), round(float(v[k]), 4)] for k in range(len(names)) if v[k] < m0[k] - 0.05},
        fits_spent=[k for k in DIALS if (abs(st[k]/D[k] - 1) > 0.01 if k in LOG else abs(st[k] - D[k]) > 1e-9)])
closable = [names.index(n) for n, v in opt.items() if v['verdict'] != 'NOT CLOSABLE BY DIALS']   # DEV-4
joint2 = {}
for split_on in (False, True):
    targets = [k for k in closable if not (split_on and names[k] == 'L7.alpha_s')]
    def fz(w, split_on=split_on):
        z = np.zeros(len(DIALS)); z[SMOOTH] = w[:-1]
        if split_on: z[DIALS.index('split')] = 1e-3
        return z
    cons = [{'type': 'ineq', 'fun': (lambda w, k=k: vec(fz(w))[k])} for k in hold] + [{'type': 'ineq', 'fun': (lambda w, k=k: vec(fz(w))[k] - w[-1])} for k in targets]
    rng = np.random.default_rng(11); best = None
    for s_ in range(6):
        w0 = np.append(rng.normal(0, 0.3, len(SMOOTH)) if s_ else np.zeros(len(SMOOTH)), -3.0)
        r = minimize(lambda w: -w[-1], w0, method='SLSQP', constraints=cons, bounds=[(-3, 3)]*len(SMOOTH) + [(-50, 50)], options={'maxiter': 500, 'ftol': 1e-10})
        if not r.success: continue
        z = fz(r.x); z[np.abs(z) < 1e-6] = 0.0; v = vec(z)
        if all(v[k] >= -1e-6 for k in hold) and (best is None or -r.fun > best[0] + 1e-9): best = (-r.fun, z, v)
    key = 'split_on' if split_on else 'split_off'
    if best is None: joint2[key] = 'no feasible point'; continue
    t, z, v = best; st = to_state(z)
    joint2[key] = dict(t_star=round(float(t), 4), move={k: round(float(z[j]), 4) for j, k in enumerate(DIALS) if abs(z[j]) > 1e-4},
        targets={names[k]: round(float(v[k]), 4) for k in targets}, closed_together=[names[k] for k in targets if v[k] >= -1e-6] + (['L7.alpha_s (split step)'] if split_on else []),
        fits_spent=[k for k in DIALS if (abs(st[k]/D[k] - 1) > 0.01 if k in LOG else abs(st[k] - D[k]) > 1e-9)])
res = dict(joint_v2=joint2, joint=joint, dials=DIALS, nodes={n: round(float(m0[i]), 4) for i, n in enumerate(names)}, n_nodes=len(names), n_holding=len(hold),
           fingerprint={n: {DIALS[j]: round(float(J[i, j]), 4) for j in range(len(DIALS)) if abs(J[i, j]) > 1e-6} for i, n in enumerate(names)},
           lenses=dict(rank=int(lz.shape[1]) if lz is not None else 0, rank_column_normalised=int(lens(Jn).shape[1])),
           singular_values=[round(float(x), 4) for x in np.linalg.svd(J, compute_uv=False)], singular_values_normalised=[round(float(x), 4) for x in np.linalg.svd(Jn, compute_uv=False)],
           compass=compass, per_node_optimisation=opt, ms_fingerprint=float('%.3g' % (t_fp*1000)), seconds_total=round(time.time() - t0, 2))
json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'd2168_weave_core.json'), 'w'), indent=1, default=str)
print('nodes', res['n_nodes'], 'holding', res['n_holding'], '| singular values', res['singular_values'])
for n, v in opt.items(): print(n, v)
print(json.dumps(joint2, indent=1)); print('fingerprint %.3g ms total %.2fs | lens rank %s' % (t_fp*1000, res['seconds_total'], res['lenses']))
