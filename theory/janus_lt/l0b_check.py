"""L0b (locked PREREG_L0b_sound_horizon): r_d vs CAMB rdrag. Same 50 seeded cosmologies as L0a."""
import sys, time, math, numpy as np, camb, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.integrate import quad
from tools.janus_lt.background import Cosmo, C_KMS, omega_gamma_h2
def r_d(c, ob, zd):
    Rk = 3*ob/(4*omega_gamma_h2())
    f = lambda z: C_KMS/math.sqrt(3*(1 + Rk/(1 + z)))/c.H(z)
    return quad(f, zd, np.inf, limit=1000, epsrel=1e-10)[0]
def zd_eh98(ob, om):   # Eisenstein & Hu 1998 Eq. 4 (fetched via ar5iv)
    b1 = 0.313*om**-0.419*(1 + 0.607*om**0.674); b2 = 0.238*om**0.223
    return 1291*om**0.251/(1 + 0.659*om**0.828)*(1 + b1*ob**b2)
rng = np.random.default_rng(2026); L = []; e2 = []; e1 = []; ez = []; n = 0
while n < 50:
    H0, ob, oc, w0, wa = rng.uniform(60, 80), rng.uniform(0.020, 0.024), rng.uniform(0.10, 0.14), rng.uniform(-1.3, -0.6), rng.uniform(-1.5, 0.5)
    if w0 + wa >= -0.1: continue
    n += 1
    p = camb.CAMBparams(); p.set_cosmology(H0=H0, ombh2=ob, omch2=oc, mnu=0.0, num_massive_neutrinos=0, nnu=3.044, TCMB=2.7255, omk=0)
    p.set_dark_energy(w=w0, wa=wa, dark_energy_model='ppf'); R = camb.get_background(p, no_thermo=False); d = R.get_derived_params()
    c = Cosmo(H0, ob, oc, w0, wa)
    r2 = r_d(c, ob, d['zdrag']); zd = zd_eh98(ob, ob + oc); r1 = r_d(c, ob, zd)
    a2, a1, az = abs(r2/d['rdrag'] - 1), abs(r1/d['rdrag'] - 1), abs(zd/d['zdrag'] - 1); e2.append(a2); e1.append(a1); ez.append(az)
    L.append(f"#{n} H0={H0:.2f} ob={ob:.4f} oc={oc:.4f}: CAMB zdrag {d['zdrag']:.3f} rdrag {d['rdrag']:.4f} | route2 r_d {r2:.4f} ({a2:.1e}) | EH98 z_d {zd:.2f} ({az:.1e}) route1 r_d {r1:.4f} ({a1:.1e})")
T1 = max(e2) <= 1e-3; T2 = np.median(e1) <= 0.01 and max(e1) <= 0.02
L.append(f"T1 route 2 (CAMB z_d): max {max(e2):.2e} median {np.median(e2):.2e} -> {'PASS' if T1 else 'FAIL'}")
L.append(f"T2 route 1 (EH98 z_d): r_d median {np.median(e1):.2e} max {max(e1):.2e}; z_d median {np.median(ez):.2e} max {max(ez):.2e} -> {'PASS' if T2 else 'FAIL'}")
L.append(f"L0b {'VALIDATED' if T1 else 'NOT VALIDATED'}")
open('field_tests/results/janus_lt_l0b.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L[-4:]))
