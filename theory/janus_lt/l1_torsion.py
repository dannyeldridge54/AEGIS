"""L1 (locked PREREG_L1_torsionlambda_firstprinciples)."""
import sys, math, numpy as np, camb, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.integrate import quad
from tools.janus_lt.background import Cosmo, C_KMS
from tools.janus_lt.recomb import Recomb
src = open('theory/janus_lt/l0b_check.py').read().split('rng = ')[0]; ns = {}; exec(compile(src, 'l0b', 'exec'), ns); r_d = ns['r_d']
wb = 0.02237; L = []
def compressed(H0, Om_eff):
    h = H0/100; wc = Om_eff*h*h - wb; c = Cosmo(H0, wb, wc); rec = Recomb(c, wb, YHe=0.24); zs = rec.z_star()
    DM = c.DM(zs); rs = r_d(c, wb, zs)
    return zs, rs, DM, math.sqrt(Om_eff)*H0*DM/C_KMS, math.pi*DM/rs
# V: LCDM vs CAMB
H0, Om = 67.36, 0.3153; zs, rs, DM, R, lA = compressed(H0, Om)
p = camb.CAMBparams(); p.set_cosmology(H0=H0, ombh2=wb, omch2=Om*(H0/100)**2 - wb, mnu=0, num_massive_neutrinos=0, nnu=3.044, TCMB=2.7255, YHe=0.24)
Rc = camb.get_background(p, no_thermo=False); d = Rc.get_derived_params()
DMc = d['DAstar']*(1 + d['zstar'])   # DEVIATIONS D2: DAstar is in Mpc
lAc = math.pi*DMc/d['rstar']
dz, dl = abs(zs/d['zstar'] - 1), abs(lA/lAc - 1); V = dz <= 2e-3 and dl <= 1e-3
L.append(f"V (LCDM vs CAMB): z* {zs:.3f} vs {d['zstar']:.3f} ({dz:.1e}); r_s {rs:.3f} vs {d['rstar']:.3f}; D_M {DM:.2f} vs {DMc:.2f}; l_A {lA:.3f} vs {lAc:.3f} ({dl:.1e}) -> {'PASS' if V else 'FAIL'}")
for name, H0, Om_eff in (("(a') LCDM Om=0.3153 h=0.6736", 67.36, 0.3153), ("(b) beta=0.192, H0=72.95, lambda renormalised", 72.95, 0.315*1.192)):
    zs, rs, DM, R, lA = compressed(H0, Om_eff)
    L.append(f"{name}: z* {zs:.2f}, r_s {rs:.2f} Mpc, R = {R:.4f} ({(R-1.7502)/0.0046:+.1f} sigma), l_A = {lA:.2f} ({(lA-301.471)/0.090:+.1f} sigma)")
open('field_tests/results/janus_lt_l1_torsion.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
