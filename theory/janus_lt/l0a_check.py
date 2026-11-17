"""L0a (locked PREREG_L0a): Janus-LT background vs CAMB."""
import sys, time, numpy as np, camb, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_lt.background import Cosmo
rng = np.random.default_rng(2026); zs = [0.1, 0.3, 0.51, 0.71, 0.93, 1.32, 2.33, 1100.0]; L = []; eH = []; eD = []; tj = tc = 0.0
n = 0
while n < 50:
    H0, ob, oc, w0, wa = rng.uniform(60, 80), rng.uniform(0.020, 0.024), rng.uniform(0.10, 0.14), rng.uniform(-1.3, -0.6), rng.uniform(-1.5, 0.5)
    if w0 + wa >= -0.1: continue
    n += 1
    t = time.time(); p = camb.CAMBparams(); p.set_cosmology(H0=H0, ombh2=ob, omch2=oc, mnu=0.0, num_massive_neutrinos=0, nnu=3.044, TCMB=2.7255, omk=0)
    p.set_dark_energy(w=w0, wa=wa, dark_energy_model='ppf'); R = camb.get_background(p)
    Hc = R.hubble_parameter(zs); Dc = R.comoving_radial_distance(zs); tc += time.time() - t
    t = time.time(); c = Cosmo(H0, ob, oc, w0, wa); Hj = np.array([c.H(z) for z in zs]); Dj = np.array([c.DM(z) for z in zs]); tj += time.time() - t
    eh = abs(Hj/Hc - 1); ed = abs(Dj/Dc - 1); eH += list(eh); eD += list(ed)
    L.append(f"#{n} H0={H0:.2f} ob={ob:.4f} oc={oc:.4f} w0={w0:.3f} wa={wa:.3f}: max|dH/H| {eh.max():.1e} (z={zs[int(eh.argmax())]}), max|dDM/DM| {ed.max():.1e} (z={zs[int(ed.argmax())]})")
mx = max(max(eH), max(eD)); v = 'L0a VALIDATED' if mx <= 1e-4 else ('PARTIAL' if mx <= 1e-3 else 'NOT VALIDATED')
L.append(f"H: max {max(eH):.2e} median {np.median(eH):.2e}; D_M: max {max(eD):.2e} median {np.median(eD):.2e}; time Janus-LT {tj/50*1e3:.1f} ms vs CAMB background {tc/50*1e3:.0f} ms per cosmology -> {v}")
open('field_tests/results/janus_lt_l0a.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[-4:]))
