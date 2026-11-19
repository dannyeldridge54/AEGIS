"""D1380 (locked PREREG_D1380_shifted_epstein.md): minima of parity-shifted Epstein sums."""
import json, math, numpy as np
from scipy.optimize import minimize
def make(N):
    m = np.arange(-N, N + 1); M, Nn = np.meshgrid(m, m, indexing='ij'); M = M.ravel().astype(float); Nn = Nn.ravel().astype(float)
    nz = ~((M == 0) & (Nn == 0))
    sg = {'S0': np.ones_like(M), 'Sa': (-1.0)**np.abs(M), 'Sb': (-1.0)**np.abs(Nn), 'Sc': (-1.0)**np.abs(M + Nn)}
    def f(name, x, y):
        if name == 'Sh':
            Mh = np.arange(-N, N + 1) + 0.5; A, B = np.meshgrid(Mh, m, indexing='ij')
            return float(np.sum(y**2/((A + B*x)**2 + (B*y)**2)**2))
        return float(np.sum(sg[name][nz]*y**2/((M[nz] + Nn[nz]*x)**2 + (Nn[nz]*y)**2)**2))
    return f
f60, f300 = make(60), make(300)
xs = np.arange(-0.5, 0.5 + 1e-9, 0.0125); ys = np.arange(0.15, 3 + 1e-9, 0.0125)
rho = (0.5, math.sqrt(3)/2); out = {}
for name in ('S0', 'Sa', 'Sb', 'Sc', 'Sh'):
    best = min(((f60(name, x, y), x, y) for x in xs for y in ys))
    edge = abs(best[2] - 0.15) < 1e-9
    res = minimize(lambda p: f300(name, p[0], p[1]) if p[1] > 0.05 else 1e9, [best[1], best[2]], method='Nelder-Mead',
                   options=dict(xatol=1e-6, fatol=1e-10, maxiter=400))
    out[name] = dict(grid_min=[best[1], best[2], best[0]], refined=[float(res.x[0]), float(res.x[1]), float(res.fun)],
                     at_rho=f300(name, *rho), on_edge=bool(edge))
    print(name, json.dumps(out[name]), flush=True)
json.dump(out, open('field_tests/results/D1380_shifted_epstein.json', 'w'), indent=1)
