"""L9 (locked PREREG_L9_fsigma8)."""
import sys, numpy as np, camb; sys.path.insert(0, '.')
from tools.janus_lt.background import Cosmo
from tools.janus_lt.growth import growth
z = [0.295, 0.510, 0.706, 0.919, 1.317, 1.491]
rat = np.array([0.80, 1.09, 1.05, 0.96, 0.95, 1.16]); sig = np.array([0.20, 0.13, 0.12, 0.105, 0.095, 0.12])
fid = np.array([0.4723, 0.4733, 0.4608, 0.4398, 0.3944, 0.3750])
def fs8(h, ob, oc, s8):
    g = growth(Cosmo(100*h, ob, oc), z); return np.array([g[zz][1]*s8*g[zz][0] for zz in z])
def s8camb(h, ob, oc):
    p = camb.CAMBparams(); p.set_cosmology(H0=100*h, ombh2=ob, omch2=oc, mnu=0.0, num_massive_neutrinos=0, nnu=3.044, TCMB=2.7255, omk=0)
    p.InitPower.set_params(As=2.1e-9, ns=0.9649); p.set_matter_power(redshifts=[0.0], kmax=2.0); return float(camb.get_results(p).get_sigma8_0())
L = []
F0 = fs8(0.6736, 0.02237, 0.1200, 0.811355); d0 = F0/fid - 1
L.append("C0 fiducial: Janus-LT " + ", ".join(f"{a:.4f}" for a in F0) + " vs Table 11; max |rel| = " + f"{np.max(np.abs(d0)):.3%}")
C0 = np.max(np.abs(d0)) <= 0.01
s_fid = s8camb(0.6736, 0.02237, 0.1200); s_b = s8camb(0.6864, 0.02252, 0.11903)
Fb = fs8(0.6864, 0.02252, 0.11903, s_b*0.811355/s_fid)
L.append(f"CAMB sigma8(As=2.1e-9): fid {s_fid:.4f}, L8b {s_b:.4f}; L8b sigma8 rescaled to fid amplitude convention = {s_b*0.811355/s_fid:.4f}")
r_b = Fb/F0; chi_b = float(np.sum(((rat - r_b)/sig)**2)); chi_1 = float(np.sum(((rat - 1)/sig)**2))
L.append("L8b/fid ratios " + ", ".join(f"{a:.4f}" for a in r_b) + f"; chi2 = {chi_b:.2f} (6 dof); fiducial chi2 = {chi_1:.2f}")
C1 = chi_b <= 12.59
L.append(f"C0 {'PASS' if C0 else 'FAIL'}; C1 {'PASS' if C1 else 'FAIL'} -> " + ('L9 NOT CLAIMED (C0)' if not C0 else ('CONSISTENT' if C1 else 'TENSION')))
open('field_tests/results/janus_lt_l9_fs8.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
