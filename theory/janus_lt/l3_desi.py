"""L3 (locked PREREG_L3_desi_bao)."""
import sys, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.optimize import minimize
from tools.janus_lt.background import Cosmo
from tools.janus_lt.desi import chi2, load
from tools.janus_lt.recomb import Recomb
src = open('theory/janus_lt/l0b_check.py').read().split('rng = ')[0]; ns = {}; exec(compile(src, 'l0b', 'exec'), ns); r_d = ns['r_d']
rows = load(); wb = 0.02237; L = []
def f(p):   # BAO-only: distances/r_d depend on (Om, h*rd); use H0 = 100 h with h fixed at 0.7 and rd = hrd/0.7 (exact degeneracy)
    Om, hrd = p; h = 0.7; c = Cosmo(100*h, wb, Om*h*h - wb); return chi2(c, hrd/h, rows)
res = minimize(f, [0.30, 101.0], method='Nelder-Mead', options={'xatol': 1e-6, 'fatol': 1e-8, 'maxiter': 2000})
Om, hrd = res.x; H = np.zeros((2, 2)); st = [1e-3, 0.05]
for i in range(2):
    for j in range(2):
        e = np.zeros(2); g = np.zeros(2); e[i] = st[i]; g[j] = st[j]
        H[i, j] = (f(res.x+e+g) - f(res.x+e-g) - f(res.x-e+g) + f(res.x-e-g))/(4*st[i]*st[j])
Cov = np.linalg.inv(H/2); sOm, shrd = math.sqrt(Cov[0, 0]), math.sqrt(Cov[1, 1]); rho = Cov[0, 1]/(sOm*shrd)
V = abs(Om - 0.2975)/0.0086 <= 0.3 and abs(hrd - 101.54)/0.73 <= 0.3 and abs(sOm/0.0086 - 1) <= 0.15 and abs(shrd/0.73 - 1) <= 0.15
L.append(f"V: Om = {Om:.4f} ± {sOm:.4f} (DESI 0.2975 ± 0.0086), h rd = {hrd:.2f} ± {shrd:.2f} (DESI 101.54 ± 0.73), r = {rho:.2f} (DESI −0.92), chi2_min = {res.fun:.2f} / 13 pts -> {'PASS' if V else 'FAIL'}")
for name, H0, Om_ in (("(i) Planck-like LCDM Om=0.3153 h=0.6736", 67.36, 0.3153), ("(ii) TorsionLambda case b (beta=0.192, H0=72.95)", 72.95, 0.315*1.192)):
    h = H0/100; c = Cosmo(H0, wb, Om_*h*h - wb); rd = r_d(c, wb, Recomb(c, wb, YHe=0.24).z_drag())
    L.append(f"{name}: r_d = {rd:.2f} Mpc, chi2 = {chi2(c, rd, rows):.2f} / 13 points")
open('field_tests/results/janus_lt_l3_desi.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
