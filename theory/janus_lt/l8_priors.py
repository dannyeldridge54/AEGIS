"""L8 (locked PREREG_L8_distance_priors)."""
import sys, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.optimize import minimize
from tools.janus_lt.background import Cosmo
from tools.janus_lt.recomb import Recomb
src = open('theory/janus_lt/l0b_check.py').read().split('rng = ')[0]; ns = {}; exec(compile(src, 'l0b', 'exec'), ns); r_d = ns['r_d']
mu = np.array([1.7502, 301.471, 0.02236]); sg = np.array([0.0046, 0.0895, 0.00015])
Cr = np.array([[1, 0.46, -0.66], [0.46, 1, -0.33], [-0.66, -0.33, 1]]); Ci = np.linalg.inv(Cr*np.outer(sg, sg))
def zhs(ob, om, g1c):
    g1 = g1c*ob**-0.238/(1 + 39.5*ob**0.763); g2 = 0.560/(1 + 21.1*ob**1.81)
    return 1048*(1 + 0.00124*ob**-0.738)*(1 + g1*om**g2)
def obs(p, opt):
    h, ob, oc = p; c = Cosmo(100*h, ob, oc, mnu=0.06)
    om = ob + oc + 0.06/93.14
    zs = zhs(ob, om, 0.0738) if opt == 'HS-text' else zhs(ob, om, 0.0783) if opt == 'HS-code' else Recomb(c, ob, YHe=0.24).z_star()
    DM = c.DM(zs); rs = r_d(c, ob, zs)
    return np.array([DM*math.sqrt(om)*100/299792.458, math.pi*DM/rs, ob]), zs
def chi2(p, opt):
    if not (0.5 < p[0] < 0.9 and 0.015 < p[1] < 0.03 and 0.08 < p[2] < 0.16): return 1e9
    d = obs(p, opt)[0] - mu; return float(d @ Ci @ d)
L = []; res = {}
for opt in ('HS-code', 'HS-text', 'own'):
    b = min((minimize(chi2, s, args=(opt,), method='Nelder-Mead', options={'xatol': 1e-8, 'fatol': 1e-8, 'maxiter': 3000}) for s in ([0.674, 0.02236, 0.120], [0.66, 0.0224, 0.122])), key=lambda r: r.fun)
    o, zs = obs(b.x, opt); res[opt] = b.fun
    L.append(f"{opt:8s}: chi2_min = {b.fun:.3f} at h = {b.x[0]:.4f}, wb = {b.x[1]:.5f}, wc = {b.x[2]:.5f} (Om = {(b.x[1]+b.x[2]+0.06/93.14)/b.x[0]**2:.4f}); z* = {zs:.2f}; R = {o[0]:.4f}, lA = {o[1]:.3f}"); print(L[-1], flush=True)
L.append(f"HS-code chi2_min {res['HS-code']:.3f} -> {'CONSISTENT' if res['HS-code'] <= 1 else 'INCONSISTENT'}")
open('field_tests/results/janus_lt_l8_priors.txt', 'w').write('\n'.join(L)+'\n'); print(L[-1])
