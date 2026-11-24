"""D2251c (DEV-8): sensitivity re-run, one fresh process per job (no state leak)."""
import json
from multiprocessing import get_context
SRC = open('theory/tests/d2251b_rescore.py').read(); SRC = SRC[:SRC.rindex("if __name__ == '__main__':")]
G = {'__name__': 'd2251c'}; exec(SRC, G)
def job(a):
    pt, refl, mode = a
    if mode == 'base':
        G['H']['refl'] = refl; G['ENG']['evaluate'].cache_clear(); return dict(point=pt, refl=refl, mode=mode, result=G['ev'](tuple(pt[k] for k in G['KEYS'])))
    return G['sens'](a)
if __name__ == '__main__':
    pts = [({'R': 9.0, 'B': 9.0, 'fAr': 0.005, 'leg': 3, 'blk': 2, 'Paux': 10.0, 'dens': 0.9, 'nu': 0.6, 'enr': 10}, 0.8),
           ({'R': 9.0, 'B': 9.0, 'fAr': 0.005, 'leg': 3, 'blk': 2, 'Paux': 10.0, 'dens': 0.9, 'nu': 0.6, 'enr': 10}, 0.6),
           ({'R': 8.0, 'B': 4.0, 'fAr': 0.0014, 'leg': 5, 'blk': 2, 'Paux': 20.0, 'dens': 0.9, 'nu': 0.6, 'enr': 10}, 0.6),
           ({'R': 7.0, 'B': 4.5, 'fAr': 0.005, 'leg': 4, 'blk': 2, 'Paux': 50.0, 'dens': 0.9, 'nu': 0.6, 'enr': 10}, 0.6),
           ({'R': 5.0, 'B': 4.0, 'fAr': 0.0005, 'leg': 4, 'blk': 2, 'Paux': 10.0, 'dens': 0.9, 'nu': 0.5, 'enr': 10}, 0.6)]
    jobs = [(p, r, m) for p, r in pts for m in ('base', 'kappa1.6', 'synch1.3')]
    with get_context('fork').Pool(2, maxtasksperchild=1) as pool: res = pool.map(job, jobs, chunksize=1)
    for s in res:
        r = s['result']; v = G['viol'](r, 0.85) if r.get('burn') else None
        print(s['mode'].ljust(9), 'refl', s['refl'], {k: s['point'][k] for k in ('R', 'B', 'fAr', 'Paux')}, 'P_fus', r.get('P_fus') and round(r['P_fus']),
              'P_net', r.get('P_net') and round(r['P_net']), 'f_rad', r.get('f_rad') and round(r['f_rad'], 3), 'synch/alpha', r.get('synch_frac') and round(r['synch_frac'], 3),
              'burn', r.get('burn'), 'viol@0.85', v and {k: round(float(x), 3) for k, x in v.items()}, flush=True)
    json.dump(res, open('field_tests/results/d2251c_sens.json', 'w'), default=float)
