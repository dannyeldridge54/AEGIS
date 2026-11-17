"""L8b (locked PREREG_L8b_priors_bao)."""
import sys, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.optimize import minimize
from tools.janus_lt.background import Cosmo
from tools.janus_lt.recomb import Recomb
from tools.janus_lt.desi import chi2 as chi2_bao, load
src = open('theory/janus_lt/l8_priors.py').read().split('L = []; res = {}')[0]; ns = {}; exec(compile(src, 'l8', 'exec'), ns)
obs, Ci, mu, r_d = ns['obs'], ns['Ci'], ns['mu'], ns['r_d']; rows = load()
def chi2(p):
    if not (0.5 < p[0] < 0.9 and 0.015 < p[1] < 0.03 and 0.08 < p[2] < 0.16): return 1e9
    h, ob, oc = p; d = obs(p, 'HS-code')[0] - mu; c = Cosmo(100*h, ob, oc, mnu=0.06)
    zd = Recomb(c, ob, YHe=0.24).z_drag(); return float(d @ Ci @ d) + chi2_bao(c, r_d(c, ob, zd), rows)
b = min((minimize(chi2, s, method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-6, 'maxiter': 3000}) for s in ([0.684, 0.02236, 0.118], [0.676, 0.02236, 0.121])), key=lambda r: r.fun)
h, ob, oc = b.x; om = (ob + oc + 0.06/93.14)/h**2; dof = 16 - 3
C1 = b.fun/dof <= 2; C2 = abs(h - 0.6842) <= 0.005
L = [f"CHW priors + DESI DR2 BAO, flat LCDM: chi2_min = {b.fun:.2f} (dof {dof}, {b.fun/dof:.2f}/dof) at h = {h:.4f}, wb = {ob:.5f}, wc = {oc:.5f}, Om = {om:.4f}",
     f"C1 fit acceptable: {'PASS' if C1 else 'FAIL'}; C2 |h - 0.6842 (L4)| = {abs(h-0.6842):.4f} <= 0.005: {'PASS' if C2 else 'FAIL'} -> " + ('ROBUST' if C1 and C2 else 'NOT ROBUST')]
open('field_tests/results/janus_lt_l8b.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
