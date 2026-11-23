"""N6-N8 (PREREG_N6N8_TRANSPORT)."""
import json, math, os, sys, time, numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mc
# K1: elastic kernel vs analytic xi (isotropic CM, target at rest)
def xi_an(A):
    if A == 1: return 1.0
    a = ((A - 1) / (A + 1)) ** 2; return 1 + a * math.log(a) / (1 - a)
rng = np.random.default_rng(3); K1 = {}
for A in (1.0, 12.0, 56.0, 208.0):
    E = 1e6; g = [math.log(E / mc.to_lab(E, E * (A / (A + 1)) ** 2, 2 * rng.random() - 1, A)[0]) for _ in range(400000)]
    K1[A] = dict(mc=float(np.mean(g)), analytic=xi_an(A))
K1ok = all(abs(v['mc'] / v['analytic'] - 1) <= .01 for v in K1.values())
# workshop task 5 geometry / materials (H8)
NA = 0.602214076
def steel():
    nFe = 0.95 * 7.75 / 55.845 * NA; nC = 0.05 * 7.75 / 12.011 * NA
    return {'Fe54': nFe * .05845, 'Fe56': nFe * .91754, 'Fe57': nFe * .02119, 'Fe58': nFe * .00282, 'C12': nC * .9893, 'C13': nC * .0107}
def pbli():
    N = 3.2720171e-2; nPb, nLi = N * .842, N * .158
    return {'Pb204': nPb * .014, 'Pb206': nPb * .241, 'Pb207': nPb * .221, 'Pb208': nPb * .524, 'Li6': nLi * .5, 'Li7': nLi * .5}
def job(args):
    seed, n, yo = args; c = {}
    regs = [None, mc.Material(steel(), c), mc.Material(pbli(), c)]
    return mc.run(regs, [500.0, 510.0, 610.0], n_hist=n, seed=seed, tally_regions=(2,), yield_override=yo)
def combine(rs):
    n = sum(r['n_hist'] for r in rs); out = {}
    for k in ('leakage', 'T_Li6', 'T_Li7'):
        vals = np.array([r.get(k, 0.0) for r in rs]); out[k] = float(np.mean(vals)); out[k + '_sem'] = float(np.std(vals, ddof=1) / math.sqrt(len(vals)))
    out['TBR'] = out['T_Li6'] + out['T_Li7']; out['TBR_sem'] = math.hypot(out['T_Li6_sem'], out['T_Li7_sem']); out['n_hist'] = n
    out['collisions_per_hist'] = float(np.mean([r['collisions_per_hist'] for r in rs])); return out
if __name__ == '__main__':
    t0 = time.time()
    with Pool(2) as p:
        base = combine(p.map(job, [(s, 2500, None) for s in range(201, 217)]))   # DEV-3: 16 batches
        nomul = combine(p.map(job, [(s, 2500, {16: 1.0}) for s in range(301, 305)]))   # DEV-2: (n,2n) yield 1
    G = dict(K1=K1ok, T1=abs(base['TBR'] / 1.0266 - 1) <= .05, T2=abs(base['leakage'] / 0.0437 - 1) <= .30,
             T3=0.001 <= base['T_Li7'] / base['TBR'] <= 0.015, T4=(1 - nomul['TBR'] / base['TBR']) > .10)
    res = dict(goals=G, K1={str(k): v for k, v in K1.items()}, base=base, no_n2n=nomul, seconds=time.time() - t0)
    json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'n6n8_rerun.json'), 'w'), indent=1)
    print(json.dumps(res, indent=1))
