"""L0c (locked PREREG_L0c_massive_nu)."""
import sys, time, numpy as np, camb, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_lt.background import Cosmo
from tools.janus_lt.recomb import Recomb
src = open('theory/janus_lt/l0b_check.py').read().split('rng = ')[0]; ns = {}; exec(compile(src, 'l0b', 'exec'), ns); r_d = ns['r_d']
zs = [0.1, 0.3, 0.51, 0.71, 0.93, 1.32, 2.33, 1100.0]; L = []; E = []; R2 = []; R1 = []
for MNU in (0.06, 0.15, 0.30):
    rng = np.random.default_rng(2026); n = 0
    while n < 50:
        H0, ob, oc, w0, wa = rng.uniform(60, 80), rng.uniform(0.020, 0.024), rng.uniform(0.10, 0.14), rng.uniform(-1.3, -0.6), rng.uniform(-1.5, 0.5)
        if w0 + wa >= -0.1: continue
        n += 1
        p = camb.CAMBparams(); p.set_cosmology(H0=H0, ombh2=ob, omch2=oc, mnu=MNU, num_massive_neutrinos=1, nnu=3.044, TCMB=2.7255, omk=0, YHe=0.24)
        p.set_dark_energy(w=w0, wa=wa, dark_energy_model='ppf'); R = camb.get_background(p, no_thermo=False); d = R.get_derived_params()
        Hc = R.hubble_parameter(zs); Dc = R.comoving_radial_distance(zs)
        c = Cosmo(H0, ob, oc, w0, wa, mnu=MNU); Hj = np.array([c.H(z) for z in zs]); Dj = np.array([c.DM(z) for z in zs])
        e = max(abs(Hj/Hc - 1).max(), abs(Dj/Dc - 1).max()); E.append(e)
        r2 = abs(r_d(c, ob, d['zdrag'])/d['rdrag'] - 1); R2.append(r2)
        if n <= 10:
            zd = Recomb(c, ob, YHe=0.24).z_drag(); R1.append(abs(r_d(c, ob, zd)/d['rdrag'] - 1))
        L.append(f"mnu={MNU} #{n}: max |dH/H|,|dDM/DM| {e:.1e} | r_d route2 {r2:.1e}")
    print(f"mnu={MNU}: max {max(E[-50:]):.2e} median {np.median(E[-50:]):.2e}", flush=True)
mx = max(E); v = 'L0c VALIDATED' if mx <= 1e-4 else ('PARTIAL' if mx <= 1e-3 else 'NOT VALIDATED')
L.append(f"T1 H, D_M over 150 cases: max {mx:.2e} median {np.median(E):.2e} -> {v}")
L.append(f"T2 r_d route 2 (CAMB zdrag): max {max(R2):.2e} median {np.median(R2):.2e}; route 1 (own recombination, first 10 per mass): max {max(R1):.2e} median {np.median(R1):.2e}")
open('field_tests/results/janus_lt_l0c.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L[-2:]))
