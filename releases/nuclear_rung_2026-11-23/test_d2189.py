import numpy as np, math, json
from chronos import *
R = {}
# T1
worst = 0.0
for name, (nucs, br) in CHAINS.items():
    tmax = 10 * max(T12[k] for k in nucs)
    for s in range(len(nucs)):
        N0 = [0.0] * len(nucs); N0[s] = 1.0
        for t in np.logspace(math.log10(1e-3 * min(T12[k] for k in nucs)), math.log10(tmax), 20):
            a, b = solve_expm(nucs, br, N0, t), solve_bateman(nucs, br, N0, t)
            for x, y in zip(a, b):
                if abs(x) > 1e-12: worst = max(worst, abs(x - y) / abs(x))
R['T1_worst_rel'] = worst; R['T1_pass'] = bool(worst < 1e-9)
# T2
tp = generator_peak('Mo-99 -> Tc-99m (generator)') / H; tr = transient_ratio('Mo-99 -> Tc-99m (generator)')
R['T2'] = dict(t_peak_h=tp, ratio=tr, pass_=bool(22.5 <= tp <= 23.5 and 0.95 <= tr <= 0.97))
# T3
ta = math.log(LAM['Am-241'] / LAM['Pu-241']) / (LAM['Am-241'] - LAM['Pu-241']) / Y
R['T3'] = dict(t_peak_y=ta, pass_=bool(65 <= ta <= 75))
# T4
err = max(abs(release_age(ratio_at(t)) - t) for t in (0.5, 3, 10)); R['T4'] = dict(max_err_y=err, pass_=bool(err < 1e-9))
# T5
eN, eC = sn_eps_coeffs(); R['T5'] = dict(e_Ni=eN, e_Co=eC, pass_=bool(abs(eN / 3.9e10 - 1) < .03 and abs(eC / 6.8e9 - 1) < .03))
# T6
L = sn_luminosity(18 * D); R['T6'] = dict(L18=L, pass_=bool(1.1e43 <= L <= 1.5e43))
json.dump(R, open('d2189_tests.json', 'w'), indent=1); print(json.dumps(R, indent=1))
