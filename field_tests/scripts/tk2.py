"""TK2 (locked PREREG_TK2): L4/L5 method with U4 recombination."""
import sys, math, time, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.optimize import minimize
from scipy.interpolate import RectBivariateSpline
from scipy.stats import chi2 as CHI, norm
from tools.janus_lt.background import Cosmo
from tools.janus_lt.recomb import Recomb
from tools.janus_lt.desi import chi2 as chi2_bao, load
src = open('theory/janus_lt/l0b_check.py').read().split('rng = ')[0]; ns = {}; exec(compile(src, 'l0b', 'exec'), ns); r_d = ns['r_d']
mu = np.array([0.01041, 0.02223, 0.14208]); C = 1e-9*np.array([[0.006621, 0.12444, -1.1929], [0.12444, 21.344, -94.001], [-1.1929, -94.001, 1488.4]]); Ci = np.linalg.inv(C)
rows = load(); L = []; t0 = time.time(); MNU = 0.05878
wbs = np.linspace(mu[1] - 4*1.46e-4, mu[1] + 4*1.46e-4, 5); wbcs = np.linspace(mu[2] - 4*1.22e-3, mu[2] + 4*1.22e-3, 5); ZS = np.zeros((5, 5)); ZD = np.zeros((5, 5))
for i, wb in enumerate(wbs):
    for j, wbc in enumerate(wbcs):
        r = Recomb(Cosmo(67.5, wb, wbc - wb, mnu=0.06), wb, YHe=0.24); ZS[i, j] = r.z_star(); ZD[i, j] = r.z_drag()
zs_f = RectBivariateSpline(wbs, wbcs, ZS, kx=3, ky=3); zd_f = RectBivariateSpline(wbs, wbcs, ZD, kx=3, ky=3); L.append(f"grid {time.time()-t0:.1f} s")
def chi2(p, lcdm):
    if lcdm: h, wb, wbc = p; w0, wa = -1.0, 0.0
    else: w0, wa, h, wb, wbc = p
    if not (0.4 < h < 1.0 and w0 + wa < 0 and -3 < wa < 2 and -2.5 < w0 < 0.5): return 1e9
    c = Cosmo(100*h, wb, wbc - wb, w0, wa, mnu=MNU); zs = float(zs_f(wb, wbc)[0, 0]); zd = float(zd_f(wb, wbc)[0, 0])
    th = r_d(c, wb, zs)/c.DM(zs); rd = r_d(c, wb, zd); d = np.array([th, wb, wbc]) - mu
    return chi2_bao(c, rd, rows) + float(d @ Ci @ d)
o = dict(method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-6, 'maxiter': 6000})
bl = min((minimize(lambda q: chi2(q, True), s, **o) for s in ([0.68, mu[1], mu[2]], [0.66, mu[1], mu[2] + 0.002])), key=lambda r: r.fun)
L.append(f"SERAPIS late (ΛCDM, Σm_ν {MNU}): χ² {bl.fun:.3f} at h {bl.x[0]:.4f}, ω_b {bl.x[1]:.5f}, ω_bc {bl.x[2]:.5f} | L5 at 0.0587: 15.32 → T1 {'PASS' if abs(bl.fun - 15.32) <= 0.05 else 'FAIL'}"); print(L[-1], flush=True)
bw = min((minimize(lambda q: chi2(q, False), s, **o) for s in ([-0.45, -1.6, 0.64, mu[1], mu[2]], [-0.8, -0.6, 0.66, mu[1], mu[2]], [-1.0, 0.0, 0.68, mu[1], mu[2]])), key=lambda r: r.fun)
dchi = bw.fun - bl.fun; p = CHI.sf(-dchi, 2); sig = norm.isf(p/2)
L.append(f"w0waCDM (Σm_ν {MNU}): χ² {bw.fun:.3f} at w0 {bw.x[0]:.3f}, wa {bw.x[1]:.3f}, h {bw.x[2]:.4f} | Δχ² = {dchi:.2f} → p = {p:.3g} (2 dof) ≈ {sig:.2f}σ preference for dynamical dark energy over SERAPIS's ΛCDM"); print(L[-1], flush=True)
L.append(f"total {time.time()-t0:.0f} s → T3 {'PASS' if time.time()-t0 <= 120 else 'FAIL'}"); print(L[-1])
open('field_tests/results/tk2_serapis_late.txt', 'w').write('\n'.join(L) + '\n')
