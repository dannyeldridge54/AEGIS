"""JMF7 (locked PREREG_JMF7_adiabatic)."""
import sys, time, numpy as np; sys.path.insert(0, '.')
from tools.janus_calc.mfms import spectra_mf
from tools.lockbench.provenance import stamp
t0 = time.time(); m9 = np.array([1e-11, 81e-11]); m = np.array([1e-11, 9e-11]); lam = np.array([1e-12, 1e-12]); e = 1e-12
M = {'Q9': (lambda f: float(0.5*m9 @ f**2), lambda f: m9*f, lambda f: np.diag(m9), [12.0, 12.0]),
     "N2'": (lambda f: float(0.5*m @ f**2 + e*f[0]*f[1]), lambda f: np.array([m[0]*f[0] + e*f[1], m[1]*f[1] + e*f[0]]), lambda f: np.array([[m[0], e], [e, m[1]]]), [12.0, 12.0]),
     'N1': (lambda f: float(0.5*m @ f**2 + f[0]**2*(lam @ f**2)/24),
            lambda f: np.array([m[0]*f[0] + (4*lam[0]*f[0]**3 + 2*lam[1]*f[0]*f[1]**2)/24, m[1]*f[1] + 2*lam[1]*f[0]**2*f[1]/24]),
            lambda f: np.array([[m[0] + (12*lam[0]*f[0]**2 + 2*lam[1]*f[1]**2)/24, 4*lam[1]*f[0]*f[1]/24], [4*lam[1]*f[0]*f[1]/24, m[1] + 2*lam[1]*f[0]**2/24]]), [12.5, 12.5])}
L = []
for name, (V, g, h, f0) in M.items():
    S = {eb: spectra_mf(V, g, h, f0, end_back=eb) for eb in (5.0, 3.0, 1.0, 0.0)}
    dP = S[1.0]['PR']/S[0.0]['PR'] - 1; dn = S[1.0]['ns'] - S[0.0]['ns']; ok = abs(dP) <= 1e-3 and abs(dn) <= 1e-5
    seq = ', '.join(f"{eb:g}: P_R/P_R(0)-1 {S[eb]['PR']/S[0.0]['PR']-1:+.2e}, n_s {S[eb]['ns']:.6f}" for eb in (5.0, 3.0, 1.0, 0.0))
    L.append(f"{name}: {seq} -> {'ADIABATIC LIMIT REACHED' if ok else 'STILL EVOLVING'}"); print(L[-1], flush=True)
R = 'field_tests/results/janus_jmf7.txt'; open(R, 'w').write('\n'.join(L) + '\n')
stamp(R, lock='field_tests/rules/PREREG_JMF7_adiabatic.md', code=['theory/janus/jmf7_adiabatic.py', 'tools/janus_calc/mfms.py'], t0=t0)
