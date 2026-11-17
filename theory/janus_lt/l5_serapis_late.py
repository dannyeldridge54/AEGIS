"""L5 (locked PREREG_L5_serapis_late): reuses the L4 grid construction."""
import sys, math, time, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.optimize import minimize
from scipy.interpolate import RectBivariateSpline
from tools.janus_lt.background import Cosmo
from tools.janus_lt.recomb import Recomb
from tools.janus_lt.desi import chi2 as chi2_bao, load
src = open('theory/janus_lt/l0b_check.py').read().split('rng = ')[0]; ns = {}; exec(compile(src, 'l0b', 'exec'), ns); r_d = ns['r_d']
mu = np.array([0.01041, 0.02223, 0.14208]); C = 1e-9*np.array([[0.006621, 0.12444, -1.1929], [0.12444, 21.344, -94.001], [-1.1929, -94.001, 1488.4]]); Ci = np.linalg.inv(C)
rows = load(); L = []; t0 = time.time()
wbs = np.linspace(mu[1] - 4*1.46e-4, mu[1] + 4*1.46e-4, 5); wbcs = np.linspace(mu[2] - 4*1.22e-3, mu[2] + 4*1.22e-3, 5)
ZS = np.zeros((5, 5)); ZD = np.zeros((5, 5))
for i, wb in enumerate(wbs):
    for j, wbc in enumerate(wbcs):
        c = Cosmo(67.5, wb, wbc - wb, mnu=0.06); r = Recomb(c, wb, YHe=0.24); ZS[i, j] = r.z_star(); ZD[i, j] = r.z_drag()
zs_f = RectBivariateSpline(wbs, wbcs, ZS, kx=3, ky=3); zd_f = RectBivariateSpline(wbs, wbcs, ZD, kx=3, ky=3)
chk = []
for wb, wbc in ((mu[1] + 1.1e-4, mu[2] - 1.7e-3), (mu[1] - 2.3e-4, mu[2] + 2.9e-3), (mu[1] + 3.1e-4, mu[2] + 0.6e-3)):
    c = Cosmo(67.5, wb, wbc - wb, mnu=0.06); r = Recomb(c, wb, YHe=0.24)
    chk.append(max(abs(r.z_star() - float(zs_f(wb, wbc)[0, 0])), abs(r.z_drag() - float(zd_f(wb, wbc)[0, 0]))))
L.append(f"grid built in {time.time()-t0:.0f} s; interpolation check max |dz| = {max(chk):.2e} ({'OK' if max(chk) <= 1e-4 else 'TOO LARGE'})")

def chi2(p, mnu):
    h, wb, wbc = p
    if not (0.4 < h < 1.0): return 1e9
    c = Cosmo(100*h, wb, wbc - wb, mnu=mnu)
    zs = float(zs_f(wb, wbc)[0, 0]); zd = float(zd_f(wb, wbc)[0, 0])
    th = r_d(c, wb, zs)/c.DM(zs); rd = r_d(c, wb, zd); d = np.array([th, wb, wbc]) - mu
    return chi2_bao(c, rd, rows) + float(d @ Ci @ d)
prof = {}
for mnu in (0.0, 0.0587, 0.10, 0.15, 0.20):
    r = min((minimize(lambda q: chi2(q, mnu), s, method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-6, 'maxiter': 4000}) for s in ([0.68, mu[1], mu[2]], [0.66, mu[1], mu[2] + 0.002])), key=lambda r: r.fun)
    prof[mnu] = r; L.append(f"mnu = {mnu:.4f} eV: chi2 = {r.fun:.3f} at h = {r.x[0]:.4f}, wb = {r.x[1]:.5f}, wbc = {r.x[2]:.5f}"); print(L[-1], flush=True)
for mnu in (0.0, 0.20):
    h, wb, wbc = prof[mnu].x; c = Cosmo(100*h, wb, wbc - wb, mnu=mnu); rr = Recomb(c, wb, YHe=0.24)
    L.append(f"z* check at mnu = {mnu}: direct {rr.z_star():.4f} vs grid {float(zs_f(wb, wbc)[0, 0]):.4f}")
cmin = min(r.fun for r in prof.values()); d = prof[0.0587].fun - cmin
L.append(f"Delta chi2(frozen 0.0587 eV) - min over grid = {d:.3f} -> {'inside' if d <= 4 else 'outside'} Delta chi2 <= 4 (consistency check only; data predate the freeze)")
open('field_tests/results/janus_lt_l5_serapis_late.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L[-3:]))
