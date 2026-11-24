"""D2238 A: blanket upgrade scan with the locked N6-N8 Monte Carlo."""
import json, math, os, sys, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, mc
import test_n6n8_rerun as T
def pbli(e6):
    N = 3.2720171e-2; nPb, nLi = N * .842, N * .158
    return {'Pb204': nPb * .014, 'Pb206': nPb * .241, 'Pb207': nPb * .221, 'Pb208': nPb * .524, 'Li6': nLi * e6, 'Li7': nLi * (1 - e6)}
def job(a):
    seed, e6, fw = a; c = {}
    regs = [None, mc.Material(T.steel(), c), mc.Material(pbli(e6), c)]
    return mc.run(regs, [500.0, 500.0 + fw, 600.0 + fw], n_hist=2500, seed=seed, tally_regions=(2,))
if __name__ == '__main__':
    out = {}; t0 = time.time()
    with Pool(2) as p:
        for e6 in (0.5, 0.7, 0.9):
            for fw in (10.0, 5.0):
                r = T.combine(p.map(job, [(s, e6, fw) for s in range(401, 409)]))
                out[f'Li6_{int(e6*100)}_fw{int(fw)}'] = r; print(e6, fw, round(r['TBR'], 4), round(r['TBR_sem'], 4), flush=True)
    out['seconds'] = time.time() - t0
    json.dump(out, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'd2238_blanket.json'), 'w'), indent=1)
