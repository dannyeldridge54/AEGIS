"""D1688 / Janus genesis G16b (PREREG_D1688_G16B_LZ_DIGITISED). Reads the digitised curve as data."""
import json, math, sys
import numpy as np
a = np.array([[float(x) for x in l.split()] for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')])
m, s = a[:, 0], a[:, 1]
sig = lambda M: float(10 ** np.interp(math.log10(M), np.log10(m), np.log10(s)))
S = {str(M): sig(M) for M in (10.0, 12.8, 15.0)}
s128 = S['12.8']; f = math.sqrt(s128 / 1e-47)
d1677 = {'0.3': 3e-9, '1': 3.4e-8, '5': 8.4e-7}
d57 = {r['m_MeV']: r['eps_min_tau_1s'] for r in json.load(open('field_tests/results/D1657_G6c_massive_dp.json'))['rows']}
floor = {'0.3': 10 ** np.interp(math.log10(300), np.log10(list(d57)), np.log10(list(d57.values()))), '1': d57[1000.0],
         '5': 10 ** (math.log10(d57[1000.0]) + (math.log10(d57[1000.0]) - math.log10(d57[100.0])) * math.log10(5))}
eps = {k: v * f for k, v in d1677.items()}
judge = 'optimistic' if s128 < 0.5e-47 else ('fair' if s128 <= 2e-47 else 'conservative')
out = dict(D='D1688', curve_points=len(m), mass_range=[float(m.min()), float(m.max())], sigma_SI=S, scale=f, eps_max=eps, BBN_floor=floor,
           strip_open={k: eps[k] > 10 * floor[k] for k in eps}, D1677_bracket_1em47_was=judge)
json.dump(out, open('field_tests/results/D1688_G16b_lz.json', 'w'), indent=1); print(json.dumps(out, indent=1))
