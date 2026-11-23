"""N9+N10 (PREREG_N9N10_ENERGY_DAMAGE): workshop sphere; energy multiplication and FW damage."""
import json, math, os, sys, time, numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mc, test_n6n8 as T6
SC = ((1, 901), (2, 901), (1, 301), (2, 301), (1, 444), (1, 207))
def job(seed):
    c = {}; regs = [None, mc.Material(T6.steel(), c), mc.Material(T6.pbli(), c)]
    return mc.run(regs, [500.0, 510.0, 610.0], n_hist=2500, seed=seed + 1000, tally_regions=(2,), scores=SC)
if __name__ == '__main__':
    t0 = time.time()
    with Pool(2) as p: rs = p.map(job, range(8))
    avg = lambda f: (float(np.mean([f(r) for r in rs])), float(np.std([f(r) for r in rs], ddof=1) / math.sqrt(len(rs))))
    En = 14.06e6
    Mloc = avg(lambda r: (r['scores']['1_901'] + r['scores']['2_901']) / En)
    Mn = avg(lambda r: (r['scores']['1_301'] + r['scores']['2_301']) / En)
    st = T6.steel(); n_atoms_bcm = sum(st.values()); V = 4 / 3 * math.pi * (510.0 ** 3 - 500.0 ** 3); N_atoms = n_atoms_bcm * 1e24 * V
    S1 = 1e6 * 4 * math.pi * 5.0 ** 2 / (14.06e6 * 1.602176634e-19)            # source neutrons/s for 1 MW/m2 at r = 5 m
    dpa_per_src = avg(lambda r: 0.8 * r['scores']['1_444'] / (2 * 40.0) / N_atoms)
    dpa_fpy = dpa_per_src[0] * S1 * 3.15576e7
    he_per_src = avg(lambda r: r['scores']['1_207'] / N_atoms)
    he_appm_per_dpa = he_per_src[0] / dpa_per_src[0] * 1e6
    G = dict(E1=1.05 <= Mloc[0] <= 1.35, E2=(1 - Mn[0] / Mloc[0]) > .03, D1=5 <= dpa_fpy <= 15, D2=7 <= he_appm_per_dpa <= 16)
    res = dict(goals=G, M_local=Mloc, M_neutron_only=Mn, dpa_per_fpy_per_MWm2=dpa_fpy, he_appm_per_dpa=he_appm_per_dpa, he_appm_per_fpy_per_MWm2=he_per_src[0] * S1 * 3.15576e7 * 1e6,
               TBR=avg(lambda r: r['TBR']), leakage=avg(lambda r: r['leakage']), n_hist=sum(r['n_hist'] for r in rs), seconds=time.time() - t0,
               heating_MeV_per_src=dict(steel=avg(lambda r: r['scores']['1_901'] / 1e6), pbli=avg(lambda r: r['scores']['2_901'] / 1e6)))
    json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'n9n10.json'), 'w'), indent=1)
    print(json.dumps(res, indent=1))
