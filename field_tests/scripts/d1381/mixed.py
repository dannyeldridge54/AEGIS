"""D1381 (locked PREREG_D1381_mixed_sectors.md)."""
import sys, json, math, numpy as np
sys.path.insert(0, '.')
from tools.serapis_calc.shapes import E
from scipy.optimize import minimize
def direct(U, sign, N=300):
    m = np.arange(-N, N + 1); M, Nn = np.meshgrid(m, m, indexing='ij'); nz = ~((M == 0) & (Nn == 0))
    w = np.ones_like(M, float) if sign == 0 else (-1.0)**np.abs(M)
    return float(np.sum((w*U.imag**2/np.abs(M + Nn*U)**4)[nz]))
chk = []
for U in (complex(0.5, math.sqrt(3)/2), complex(0.1, 1.3), complex(-0.3, 0.6)):
    lhs = direct(U, 0) - direct(U, 1); rhs = 2*(E(U) - E(U/2)/4)
    chk.append([str(U), lhs, rhs, abs(lhs - rhs)/abs(rhs)])
print('identity check (odd-m sum x2):', json.dumps(chk), flush=True)
F = lambda c, x, y: (1 - c)*E(complex(x, y)) + 0.5*c*E(complex(x, y)/2)
xs = np.arange(-1, 1 + 1e-9, 0.01); ys = np.arange(0.2, 3 + 1e-9, 0.01); out = dict(identity=chk, rows={})
for c in (0.0, -1.0, -0.5, 0.5, 1.0):
    best = min((F(c, x, y), x, y) for x in xs for y in ys)
    res = minimize(lambda p: F(c, p[0], p[1]) if 0.05 < p[1] < 50 else 1e9, [best[1], best[2]], method='Nelder-Mead',
                   options=dict(xatol=1e-7, fatol=1e-12, maxiter=600))
    edge = abs(best[2] - 0.2) < 1e-9 or abs(best[2] - 3) < 1e-9
    out['rows'][str(c)] = dict(grid=[best[1], best[2], best[0]], refined=[float(res.x[0]), float(res.x[1]), float(res.fun)], grid_on_edge=bool(edge))
    print(c, json.dumps(out['rows'][str(c)]), flush=True)
json.dump(out, open('field_tests/results/D1381_mixed_sectors.json', 'w'), indent=1)
