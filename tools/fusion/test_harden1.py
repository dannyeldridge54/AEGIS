import json, math, os, sys, numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mc, test_n6n8 as T6
def job(a):
    seed, yo = a; c = {}; regs = [None, mc.Material(T6.steel(), c), mc.Material(T6.pbli(), c)]
    return mc.run(regs, [500.0, 510.0, 610.0], n_hist=500, seed=seed + 5000, tally_regions=(2,), yield_override=yo)
if __name__ == '__main__':
    with Pool(2) as p: base = p.map(job, [(s, None) for s in range(4)]); y1 = p.map(job, [(s, {(16, 'Pb'): 1.0}) for s in range(4)])
    def bal(rs):
        b = {k: sum(r['book'][k] for r in rs) for k in rs[0]['book']}; return b, b['source'] + b['multiplication'] - (b['leaks'] + b['absorptions'] + b['cutoffs'])
    b0, r0 = bal(base); b1, r1 = bal(y1)
    est = np.array([r['T_Li6'] for r in base]); ana = np.array([r['book']['li6_n_t'] / r['n_hist'] for r in base])
    se = math.sqrt(est.var(ddof=1) / len(est) + ana.var(ddof=1) / len(ana))
    G = dict(B1=r0 == 0, B2=r1 == 0, B3=abs(est.mean() - ana.mean()) <= 3 * se)
    res = dict(goals=G, book=b0, residual=r0, book_yield1=b1, residual_yield1=r1, T_Li6_estimator=float(est.mean()), T_Li6_analog=float(ana.mean()), combined_se=se)
    json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'harden1.json'), 'w'), indent=1, default=int)
    print(json.dumps(res, indent=1, default=int))
