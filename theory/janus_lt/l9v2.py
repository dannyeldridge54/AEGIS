"""L9v2 (locked PREREG_L9v2_fs8_own)."""
import sys, importlib.util, numpy as np; sys.path.insert(0, '.')
def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    src = open(p).read().split('\nL = []')[0]; exec(compile(src, p, 'exec'), m.__dict__); return m
A = load('l9', 'theory/janus_lt/l9_fs8.py'); B = load('l9c', 'theory/janus_lt/l9c_sigma8.py')
sf = B.sigma8(0.6736, 0.02237, 0.1200)[0]; sb = B.sigma8(0.6864, 0.02252, 0.11903)[0]
F0 = A.fs8(0.6736, 0.02237, 0.1200, 0.811355); Fb = A.fs8(0.6864, 0.02252, 0.11903, sb*0.811355/sf)
r = Fb/F0; chi = float(np.sum(((A.rat - r)/A.sig)**2))
L = [f"own sigma8: fid {sf:.4f}, L8b {sb:.4f} (rescaled {sb*0.811355/sf:.4f})", "ratios " + ", ".join(f"{x:.4f}" for x in r),
     f"chi2 = {chi:.2f} (6 dof); vs L9 CAMB-referee 3.81: |dchi2| = {abs(chi-3.81):.2f} -> {'CONSISTENT' if chi <= 12.59 else 'TENSION'}"]
open('field_tests/results/janus_lt_l9v2.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
