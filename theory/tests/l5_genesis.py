"""PREREG_L5_GENESIS_MAGD7"""
import math, json
import numpy as np
out = {}
for ainv in (24.3, 40.0):
    x = 9 * math.sqrt(3) / 2 / ainv; TR = x * 1.34e9
    eps = 1.8e-6 * 9e8 / TR; mmin = eps / (3 * 0.0501e-9 / (16 * math.pi * 174 ** 2)); mmax = 2.5e12
    lo = max(mmin, 10 * TR); ok = lo < mmax
    def allowed(M, p0):
        MP = 2.435e18; G = M ** 3 / (4 * math.pi * MP ** 2)
        g = 10.75 if (90 / (math.pi ** 2 * 10.75)) ** .25 * math.sqrt(G * MP) < 1 else 80
        Td = (90 / (math.pi ** 2 * g)) ** .25 * math.sqrt(G * MP); D = max(1.0, TR * p0 ** 2 / 6 / Td)
        return Td >= 5e-3 and D <= 1e3 and abs(2 * (-math.log(D) / 3) / 50.37 ** 2) <= 0.003
    grid = np.logspace(4, math.log10(5.23e12), 4000)
    win = {str(p0): float(min([m for m in grid if allowed(m, p0)], default=float('nan'))) for p0 in (0.1, 1.0)}
    dN = math.log(x) / 3; r = 5.41e-4 * (50.37 / (50.37 + dN)) ** 2
    out[f'alpha_inv={ainv}'] = dict(x=x, T_R=TR, eps_needed=eps, M_N_min_DI=mmin, M_N_window=[lo, mmax], genesis_PASS=ok,
                                    tauq_lowest_allowed_mass_GeV=win, dNstar=dN, r_new=r)
print(json.dumps(out, indent=1))
