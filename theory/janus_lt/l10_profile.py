"""L10 (locked PREREG_L10_w0wa_profile): profile-likelihood grid over (w0, wa) reusing L7's chi2."""
import sys, time, math, numpy as np; sys.path.insert(0, '.')
from scipy.optimize import minimize
from tools.lockbench.provenance import stamp
t0 = time.time(); src = open('theory/janus_lt/l7_joint.py').read().split('best_l = ')[0]; ns = {'__name__': 'l7lib'}; exec(compile(src, 'l7', 'exec'), ns)
chi2, mu = ns['chi2'], ns['mu']
W0 = np.round(np.linspace(-1.2, -0.5, 15), 4); WA = np.linspace(-1.4, 0.4, 15); G = np.zeros((15, 15))
for i, w0 in enumerate(W0):
    for j, wa in enumerate(WA):
        G[i, j] = min(minimize(lambda q: chi2([w0, wa, *q]), s, method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-6, 'maxiter': 3000}).fun
                      for s in ([0.67, mu[1], mu[2]], [0.69, mu[1], mu[2]]))
    print(f'row {i+1}/15 done {time.time()-t0:.0f}s', flush=True)
lc = min(minimize(lambda q: chi2(q, True), s, method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-6, 'maxiter': 4000}).fun for s in ([0.68, mu[1], mu[2]], [0.66, mu[1], mu[2]]))
gmin = G.min(); i0, j0 = np.unravel_index(G.argmin(), G.shape); MAPc = 1422.93; dl = lc - min(gmin, MAPc)
c1 = abs(W0[i0] + 0.853) <= 0.05 + 1e-9 and abs(WA[j0] + 0.518) <= 0.1286 + 1e-9; c2 = abs(dl - 7.70) <= 0.30
from scipy.interpolate import RectBivariateSpline
sp = RectBivariateSpline(W0, WA, G - min(gmin, MAPc)); c3 = float(sp(-0.838, -0.62)[0, 0]) <= 2.30
def ext(t):
    m = (G - min(gmin, MAPc)) <= t; ii, jj = np.where(m)
    return (W0[ii].min(), W0[ii].max(), WA[jj].min(), WA[jj].max()) if m.any() else None
L = [f'grid min chi2 {gmin:.2f} at w0 {W0[i0]}, wa {WA[j0]:.3f}; L7 MAP chi2 1422.93 at (-0.853, -0.518) -> C1 {c1}',
     f'LCDM chi2 {lc:.2f}; Delta chi2 vs minimum {dl:.2f} (L7: 7.70) -> C2 {c2}',
     f'DESI best fit (-0.838, -0.62): profile Delta chi2 {float(sp(-0.838, -0.62)[0, 0]):.2f} -> C3 (inside 68%) {c3}',
     f'68% (Delta chi2 2.30) grid extent w0 {ext(2.30)[:2]}, wa {ext(2.30)[2:]}; 95% (6.18) w0 {ext(6.18)[:2]}, wa {ext(6.18)[2:]}; L7 Gaussian: w0 ±0.053, wa ±0.200',
     'L10: ' + ('PROFILE CONSISTENT WITH L7' + ('; CONTAINS DESI' if c3 else '; DESI OUTSIDE 68%') if (c1 and c2) else 'NOT CONSISTENT') + f'  ({time.time()-t0:.0f} s)']
R = 'field_tests/results/janus_lt_l10_profile.txt'; open(R, 'w').write('\n'.join(L) + '\n'); np.savez('field_tests/results/janus_lt_l10_grid.npz', W0=W0, WA=WA, G=G, lcdm=lc)
print('\n'.join(L)); stamp(R, lock='field_tests/rules/PREREG_L10_w0wa_profile.md', code=['theory/janus_lt/l10_profile.py', 'theory/janus_lt/l7_joint.py'], t0=t0)
