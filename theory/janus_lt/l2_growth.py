"""L2 (locked PREREG_L2_growth)."""
import sys, numpy as np, camb, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_lt.background import Cosmo
from tools.janus_lt.growth import growth
zs = [0.0, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]; rng = np.random.default_rng(2026); L = []; e1 = []; e2 = []; n = 0
while n < 20:
    H0, ob, oc, w0, wa = rng.uniform(60, 80), rng.uniform(0.020, 0.024), rng.uniform(0.10, 0.14), rng.uniform(-1.3, -0.6), rng.uniform(-1.5, 0.5)
    if w0 + wa >= -0.1: continue
    n += 1
    if n <= 10: w0, wa = -1.0, 0.0
    p = camb.CAMBparams(); p.set_cosmology(H0=H0, ombh2=ob, omch2=oc, mnu=0, num_massive_neutrinos=0, nnu=3.044, TCMB=2.7255)
    p.set_dark_energy(w=w0, wa=wa, dark_energy_model='ppf'); p.InitPower.set_params(As=2.1e-9, ns=0.965)
    p.set_matter_power(redshifts=sorted(zs, reverse=True), kmax=2.0); R = camb.get_results(p)
    s8 = np.array(R.get_sigma8())[::-1]; fs8 = np.array(R.get_fsigma8())[::-1]          # ordered as zs ascending
    g = growth(Cosmo(H0, ob, oc, w0, wa), zs)
    dD = max(abs(g[z][0] - s8[i]/s8[0]) for i, z in enumerate(zs)); df = max(abs(g[z][1]/(fs8[i]/s8[i]) - 1) for i, z in enumerate(zs))
    (e1 if n <= 10 else e2).append((dD, df))
    L.append(f"#{n} {'LCDM' if n <= 10 else 'w0wa'} H0={H0:.1f} w0={w0:.2f} wa={wa:.2f}: max |dD ratio| {dD:.1e}, max |df/f| {df:.1e}")
    print(L[-1], flush=True)
T1 = max(x[0] for x in e1) <= 2e-3 and max(x[1] for x in e1) <= 3e-3
L.append(f"T1 LCDM: max dD {max(x[0] for x in e1):.2e}, max df/f {max(x[1] for x in e1):.2e} -> {'PASS' if T1 else 'FAIL'}")
L.append(f"T2 w0wa (report): max dD {max(x[0] for x in e2):.2e}, max df/f {max(x[1] for x in e2):.2e}")
L.append(f"L2 {'VALIDATED' if T1 else 'NOT VALIDATED'}")
open('field_tests/results/janus_lt_l2_growth.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L[-3:]))
