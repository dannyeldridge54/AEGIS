"""J9 (locked PREREG_J9_beta_s): beta_s Janus vs exact MS."""
import sys, importlib.util, numpy as np; sys.path.insert(0, '.')
sp = importlib.util.spec_from_file_location('j7b', 'theory/janus/j7b_wide.py'); B = importlib.util.module_from_spec(sp); sp.loader.exec_module(B)
from tools.serapis_calc.ms import Background, spectra_fast
from tools.janus_calc.core import spectra3
def beta(bg, N, lo, n):
    s = spectra_fast(bg, N, dlnk=tuple(np.linspace(-lo, lo, n)), bd=1000.0, return_lp=True)
    c = np.polyfit(s['dlnk'], s['lnPR'], 5); return 6*c[-4]
L = []; inf = 0; ok = True
for i in (1, 4, 13):
    name, V, dV, y0, m = B.build(i); bg = Background(V, dV, y0, Nmax=3000)
    for N in (50.0, 60.0):
        bA, bB = beta(bg, N, 1.5, 15), beta(bg, N, 1.0, 11); bJ = float(spectra3(m, N)['beta_s'])
        I = abs(bA-bB) <= 0.2*abs(bA); inf += I; e = abs(bJ-bA)/abs(bA)
        if I: ok &= e <= 0.1
        L.append(f"{name:10s} N*={N:.0f}: beta_A {bA:.4e} beta_B {bB:.4e} ({'informative' if I else 'NOT informative'}) | Janus {bJ:.4e} rel err {e:.3f}"); print(L[-1], flush=True)
C1 = inf >= 4; C2 = ok
L.append(f"C1 informative {inf}/6: {'PASS' if C1 else 'FAIL'}; C2: {'PASS' if C2 else 'FAIL'} -> " + ('J9 UNINFORMATIVE' if not C1 else ('Janus beta_s VALIDATED' if C2 else 'Janus beta_s NOT VALIDATED')))
open('field_tests/results/janus_j9_beta_s.txt', 'w').write('\n'.join(L)+'\n'); print(L[-1])
