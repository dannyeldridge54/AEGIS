"""I25 (locked PREREG_I25_pyt_radius)."""
import sys, os, importlib, numpy as np; sys.path.insert(0, '.')
PT = '/home/claude/ext/PyTransport/PyTransport'; sys.path += [PT, PT + '/PyTrans']
import PyTransScripts as S
PyT = importlib.import_module('PyTransJNC_DQuad'); M = 0.5e-6; fi = np.array([0.4, 26.0]); L = []
def ns_pyt(p, tol):
    V = PyT.V(fi, p); dV = PyT.dV(fi, p); ic = np.concatenate([fi, -dV/np.sqrt(3*V)])
    back = PyT.backEvolve(np.linspace(0, 400, 8000), ic, p, np.array([tol, tol]), True); Ne = back[-1, 0]
    ks = S.kexitN(Ne - 55.0, back, p, PyT); lk = np.log(ks) + np.linspace(-0.4, 0.4, 9)
    zz, _ = S.pSpectra(np.exp(lk), back, p, 6.0, np.array([tol, tol]), PyT)
    c = np.polyfit(lk - np.log(ks), np.log(zz), 2); return c[1] + 4.0, Ne
for R in (1.0, 1.5, 2.0):
    p = np.array([0.002*M**2, 0.004*M**2, R])
    try:
        sys.stdout = open(os.devnull, 'w'); a, Ne = ns_pyt(p, 1e-8); b, _ = ns_pyt(p, 1e-10); sys.stdout = sys.__stdout__
        L.append(f"R={R}: PyTransport N_tot {Ne:.2f} n_s {a:.6f} (tol 1e-10: {b:.6f})")
    except Exception as e:
        sys.stdout = sys.__stdout__; L.append(f"R={R}: PyTransport failed: {e}")
    print(L[-1], flush=True)
open('field_tests/results/i25_pyt_radius.txt', 'w').write('\n'.join(L) + '\n')
