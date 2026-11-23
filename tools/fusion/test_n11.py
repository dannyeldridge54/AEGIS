"""N11 (PREREG_N11_ACTIVATION): first-wall Fe activation from MC reaction rates + single-step Bateman."""
import json, math, os, sys, time, numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mc, test_n6n8 as T6, fusion_cm as FC
RX = {'Fe-55a': (102, 'Fe54'), 'Fe-55b': (16, 'Fe56'), 'Mn-54': (103, 'Fe54'), 'Mn-56': (103, 'Fe56'), 'Fe-59': (102, 'Fe58'), 'Cr-51': (107, 'Fe54')}
SC = tuple((1, mt, pre) for mt, pre in RX.values()) + ((1, 207, 'Fe'),)
def job(seed):
    c = {}; st = mc.Material(T6.steel(), c); regs = [None, st, st, mc.Material(T6.pbli(), c)]
    return mc.run(regs, [500.0, 501.0, 510.0, 610.0], n_hist=2500, seed=seed + 3000, tally_regions=(3,), scores=SC)
def activity(R, kill=()):
    T = 3.15576e7; out = {}
    for t_lab, t in (('0s', 0.0), ('1d', 86400.0), ('30d', 30 * 86400.0), ('1y', 3.15576e7), ('10y', 3.15576e8), ('100y', 3.15576e9)):
        a = {}
        for nuc in ('Fe-55', 'Mn-54', 'Mn-56', 'Fe-59', 'Cr-51'):
            r = sum(v for k, v in R.items() if k.startswith(nuc) and k not in kill); lam = math.log(2) / FC.run('nuclide_lookup', {'name': nuc})['half_life_s']
            a[nuc] = r * (1 - math.exp(-lam * T)) * math.exp(-lam * t)
        out[t_lab] = a
    return out
if __name__ == '__main__':
    t0 = time.time()
    with Pool(2) as p: rs = p.map(job, range(8))
    st = T6.steel(); nFe = sum(v for k, v in st.items() if k.startswith('Fe')); V1 = 4 / 3 * math.pi * (501.0 ** 3 - 500.0 ** 3)
    massFe_kg = nFe * 1e24 * V1 * 55.845 / 6.02214076e23 / 1000
    S1 = 1e6 * 4 * math.pi * 5.0 ** 2 / (14.0e6 * 1.602176634e-19)     # source energy 14.0 MeV (audit R99)
    def key(mt, pre): return f'1_{mt}_{pre}'
    R = {lab: float(np.mean([r['scores'][key(mt, pre)] for r in rs])) * S1 / massFe_kg for lab, (mt, pre) in RX.items()}   # reactions / s / kg Fe
    A = activity(R); A0 = activity(R, kill=('Fe-55a', 'Fe-55b'))
    top = lambda a: sorted(a, key=lambda k: -a[k])
    he = float(np.mean([r['scores']['1_207_Fe'] for r in rs])) / (nFe * 1e24 * V1) * S1 * 3.15576e7 * 1e6
    G = dict(A1=top(A['0s'])[0] == 'Mn-56', A2=set(top(A['1y'])[:2]) == {'Fe-55', 'Mn-54'} and top(A['10y'])[0] == 'Fe-55',
             A3=60 <= he <= 160, A4=top(A0['10y'])[0] != 'Fe-55')
    res = dict(goals=G, rates_per_s_per_kgFe=R, activity_Bq_per_kgFe=A, total_Bq_per_kgFe={k: sum(v.values()) for k, v in A.items()},
               ranking={k: top(v) for k, v in A.items()}, he_appm_per_fpy_per_MWm2=he, can_fail_ranking_10y=top(A0['10y']), seconds=time.time() - t0)
    json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'n11_activation.json'), 'w'), indent=1)
    print(json.dumps({k: res[k] for k in ('goals', 'total_Bq_per_kgFe', 'ranking', 'he_appm_per_fpy_per_MWm2', 'can_fail_ranking_10y')}, indent=1))
