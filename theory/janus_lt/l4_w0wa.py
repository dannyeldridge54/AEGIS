"""L4 (locked PREREG_L4_w0wa_fit)."""
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
def chi2(p, lcdm=False):
    if lcdm: h, wb, wbc = p; w0, wa = -1.0, 0.0
    else: w0, wa, h, wb, wbc = p
    if not (0.4 < h < 1.0 and w0 + wa < 0 and -3 < wa < 2 and -2.5 < w0 < 0.5): return 1e9
    c = Cosmo(100*h, wb, wbc - wb, w0, wa, mnu=0.06)
    zs = float(zs_f(wb, wbc)[0, 0]); zd = float(zd_f(wb, wbc)[0, 0])
    th = r_d(c, wb, zs)/c.DM(zs); rd = r_d(c, wb, zd)
    d = np.array([th, wb, wbc]) - mu
    return chi2_bao(c, rd, rows) + float(d @ Ci @ d)
best_l = min((minimize(lambda q: chi2(q, True), s, method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-6, 'maxiter': 4000}) for s in ([0.68, mu[1], mu[2]], [0.66, mu[1], mu[2]])), key=lambda r: r.fun)
best = min((minimize(chi2, s, method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-6, 'maxiter': 8000}) for s in ([-0.4, -1.8, 0.64, mu[1], mu[2]], [-0.8, -0.8, 0.66, mu[1], mu[2]], [-1.0, 0.0, 0.68, mu[1], mu[2]])), key=lambda r: r.fun)
w0, wa = best.x[0], best.x[1]; dchi = best.fun - best_l.fun
st = np.array([0.01, 0.03, 0.002, 2e-5, 2e-4]); H = np.zeros((5, 5)); x = best.x
for i in range(5):
    for j in range(5):
        e = np.zeros(5); g = np.zeros(5); e[i] = st[i]; g[j] = st[j]
        H[i, j] = (chi2(x+e+g) - chi2(x+e-g) - chi2(x-e+g) + chi2(x-e-g))/(4*st[i]*st[j])
Cv = np.linalg.inv(H/2); s0, sa = math.sqrt(abs(Cv[0, 0])), math.sqrt(abs(Cv[1, 1]))
L.append(f"LCDM: chi2 = {best_l.fun:.2f} at h = {best_l.x[0]:.4f}, wb = {best_l.x[1]:.5f}, wbc = {best_l.x[2]:.5f}")
L.append(f"w0waCDM MAP: w0 = {w0:.3f} ± {s0:.3f}, wa = {wa:.3f} ± {sa:.3f}, h = {x[2]:.4f}; chi2 = {best.fun:.2f}; Delta chi2 = {dchi:.2f}")
ok = abs(w0 + 0.42) <= 0.21 and abs(wa + 1.75) <= 0.58 and abs(dchi + 12.5) <= 4
L.append(f"vs DESI+CMB (Eq. 25: w0 = -0.42 ± 0.21, wa = -1.75 ± 0.58, Delta chi2 = -12.5): {'CONSISTENT' if ok else 'INCONSISTENT'}  (total {time.time()-t0:.0f} s)")
open('field_tests/results/janus_lt_l4_w0wa.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
