"""N9+N10 (PREREG_N9N10_ENERGY_DAMAGE): workshop sphere; energy multiplication and FW damage."""
import json, math, os, sys, time, numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mc, test_n6n8 as T6
SC = ((1, 901), (2, 901), (3, 901), (1, 301), (2, 301), (3, 301), (1, 444), (2, 444), (1, 444, 'Fe'), (2, 444, 'Fe'), (1, 207, 'Fe'), (2, 207, 'Fe'), (1, 207), (2, 207))   # DEV-1/2
def job(seed):
    c = {}; st = mc.Material(T6.steel(), c); regs = [None, st, st, mc.Material(T6.pbli(), c)]   # DEV-2: front 1 cm + rest
    return mc.run(regs, [500.0, 501.0, 510.0, 610.0], n_hist=2500, seed=seed + 2000, tally_regions=(3,), scores=SC)
if __name__ == '__main__':
    t0 = time.time()
    with Pool(2) as p: rs = p.map(job, range(8))
    avg = lambda f: (float(np.mean([f(r) for r in rs])), float(np.std([f(r) for r in rs], ddof=1) / math.sqrt(len(rs))))
    En = 14.06e6
    Mloc = avg(lambda r: sum(r['scores'][f'{g}_901'] for g in (1, 2, 3)) / En)
    Mn = avg(lambda r: sum(r['scores'][f'{g}_301'] for g in (1, 2, 3)) / En)
    st = T6.steel(); nb = sum(st.values()); nFe = sum(v for k, v in st.items() if k.startswith('Fe'))
    vol = lambda a, b: 4 / 3 * math.pi * (b ** 3 - a ** 3); V1, V2 = vol(500., 501.), vol(501., 510.)
    S1 = 1e6 * 4 * math.pi * 5.0 ** 2 / (14.06e6 * 1.602176634e-19); Y = 3.15576e7
    dpa = lambda key, n_bcm, V: 0.8 * key / 80.0 / (n_bcm * 1e24 * V)
    dpa10 = avg(lambda r: dpa(r['scores']['1_444'] + r['scores']['2_444'], nb, V1 + V2))[0] * S1 * Y
    dpa_front = avg(lambda r: dpa(r['scores']['1_444'], nb, V1))[0] * S1 * Y
    dpaFe10 = avg(lambda r: dpa(r['scores']['1_444_Fe'] + r['scores']['2_444_Fe'], nFe, V1 + V2))[0]
    heFe10 = avg(lambda r: (r['scores']['1_207_Fe'] + r['scores']['2_207_Fe']) / (nFe * 1e24 * (V1 + V2)))[0]
    dpaFeF = avg(lambda r: dpa(r['scores']['1_444_Fe'], nFe, V1))[0]; heFeF = avg(lambda r: r['scores']['1_207_Fe'] / (nFe * 1e24 * V1))[0]
    he_all = avg(lambda r: (r['scores']['1_207'] + r['scores']['2_207']) / (nb * 1e24 * (V1 + V2)))[0]
    dpa_all = avg(lambda r: dpa(r['scores']['1_444'] + r['scores']['2_444'], nb, V1 + V2))[0]
    he_appm_per_dpa = heFe10 / dpaFe10 * 1e6; dpa_fpy = dpa10
    G = dict(E1=1.05 <= Mloc[0] <= 1.35, E2=(1 - Mn[0] / Mloc[0]) > .03, D1=5 <= dpa_fpy <= 15, D2=7 <= he_appm_per_dpa <= 16)
    res = dict(goals=G, M_local=Mloc, M_neutron_only=Mn, dpa_per_fpy_per_MWm2=dpa_fpy, dpa_front_cm=dpa_front, he_appm_per_dpa_Fe_only=he_appm_per_dpa,
               he_appm_per_dpa_Fe_front=heFeF / dpaFeF * 1e6, he_appm_per_dpa_all_atoms=he_all / dpa_all * 1e6,
               he_Fe_appm_per_fpy_per_MWm2_front=heFeF * S1 * Y * 1e6,
               TBR=avg(lambda r: r['TBR']), leakage=avg(lambda r: r['leakage']), n_hist=sum(r['n_hist'] for r in rs), seconds=time.time() - t0,
               heating_MeV_per_src=dict(steel=avg(lambda r: (r['scores']['1_901'] + r['scores']['2_901']) / 1e6), pbli=avg(lambda r: r['scores']['3_901'] / 1e6)))
    json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'n9n10_rerun.json'), 'w'), indent=1)
    print(json.dumps(res, indent=1))
