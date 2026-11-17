"""L0b2 (locked PREREG_L0b2_recombination)."""
import sys, time, numpy as np, camb, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_lt.background import Cosmo
from tools.janus_lt.recomb import Recomb
import importlib.util
sp = importlib.util.spec_from_file_location('l0b', 'theory/janus_lt/l0b_check.py')
src = open('theory/janus_lt/l0b_check.py').read().split('rng = ')[0]; ns = {}; exec(compile(src, 'l0b', 'exec'), ns); r_d = ns['r_d']
rng = np.random.default_rng(2026); L = []; ez = []; er = []; n = 0; t0 = time.time()
while n < 50:
    H0, ob, oc, w0, wa = rng.uniform(60, 80), rng.uniform(0.020, 0.024), rng.uniform(0.10, 0.14), rng.uniform(-1.3, -0.6), rng.uniform(-1.5, 0.5)
    if w0 + wa >= -0.1: continue
    n += 1
    p = camb.CAMBparams(); p.set_cosmology(H0=H0, ombh2=ob, omch2=oc, mnu=0.0, num_massive_neutrinos=0, nnu=3.044, TCMB=2.7255, omk=0, YHe=0.24)
    p.set_dark_energy(w=w0, wa=wa, dark_energy_model='ppf'); R = camb.get_background(p, no_thermo=False); d = R.get_derived_params()
    c = Cosmo(H0, ob, oc, w0, wa); rec = Recomb(c, ob, YHe=0.24); zd = rec.z_drag(); rd = r_d(c, ob, zd)
    a, b = abs(zd/d['zdrag'] - 1), abs(rd/d['rdrag'] - 1); ez.append(a); er.append(b)
    L.append(f"#{n} H0={H0:.2f} ob={ob:.4f} oc={oc:.4f}: z_d {zd:.3f} vs CAMB {d['zdrag']:.3f} ({a:.1e}) | r_d {rd:.4f} vs {d['rdrag']:.4f} ({b:.1e})")
    print(L[-1], flush=True)
T1 = max(ez) <= 2e-3; T2 = max(er) <= 2e-3
L.append(f"T1 z_d: max {max(ez):.2e} median {np.median(ez):.2e} (1e-3 level: {sum(x <= 1e-3 for x in ez)}/50) -> {'PASS' if T1 else 'FAIL'}")
L.append(f"T2 r_d: max {max(er):.2e} median {np.median(er):.2e} (1e-3 level: {sum(x <= 1e-3 for x in er)}/50) -> {'PASS' if T2 else 'FAIL'}")
L.append(f"L0b2 {'VALIDATED' if (T1 and T2) else 'NOT VALIDATED'}  ({(time.time()-t0)/50:.1f} s per cosmology)")
open('field_tests/results/janus_lt_l0b2.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L[-3:]))
