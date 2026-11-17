"""JMF8 (locked PREREG_JMF8_threefield)."""
import sys, os, time, importlib, numpy as np, sympy as sym; sys.path.insert(0, '.')
PT = '/home/claude/ext/PyTransport/PyTransport'; sys.path += [PT, PT + '/PyTrans']
import PyTransSetup, PyTransScripts as S
from tools.janus_calc.mfms import spectra_mf
from tools.lockbench.provenance import stamp
t0 = time.time(); f = sym.symarray('f', 3); p = sym.symarray('p', 4); h = sym.Rational(1, 2)
m = np.array([1e-11, 9e-11, 25e-11]); e = 1e-12
MODELS = {'T1': (h*(p[0]*f[0]**2 + p[1]*f[1]**2 + p[2]*f[2]**2), [*m, 0.0],
                 lambda x: float(0.5*m @ x**2), lambda x: m*x, lambda x: np.diag(m)),
          'T2': (h*(p[0]*f[0]**2 + p[1]*f[1]**2 + p[2]*f[2]**2) + p[3]*(f[0]*f[1] + f[1]*f[2]), [*m, e],
                 lambda x: float(0.5*m @ x**2 + e*(x[0]*x[1] + x[1]*x[2])),
                 lambda x: m*x + e*np.array([x[1], x[0] + x[2], x[1]]),
                 lambda x: np.diag(m) + e*np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]))}
def ns_pyt(M, pv, f0, tol):
    V = M.V(f0, pv); dV = M.dV(f0, pv); ic = np.concatenate([f0, -dV/np.sqrt(3*V)])
    back = M.backEvolve(np.linspace(0, 400, 8000), ic, pv, np.array([tol, tol]), True); Ne = back[-1, 0]
    ks = S.kexitN(Ne - 55.0, back, pv, M); lk = np.log(ks) + np.linspace(-0.4, 0.4, 9)
    zz, _ = S.pSpectra(np.exp(lk), back, pv, 6.0, np.array([tol, tol]), M); c = np.polyfit(lk - np.log(ks), np.log(zz), 2); return c[1] + 4.0, Ne
L = []; ok = True; f0 = np.array([12.0, 12.0, 12.0])
for name, (Vs, pv, V, g, hs) in MODELS.items():
    PyTransSetup.potential(Vs, 3, 4, False); PyTransSetup.compileName3('J8' + name, False); M = importlib.import_module('PyTransJ8' + name); pv = np.array(pv)
    sys.stdout = open(os.devnull, 'w'); a, Ne = ns_pyt(M, pv, f0, 1e-8); b, _ = ns_pyt(M, pv, f0, 1e-10); sys.stdout = sys.__stdout__
    J = spectra_mf(V, g, hs, list(f0)); J1 = spectra_mf(V, g, hs, list(f0), end_back=1.0)
    d = abs(J['ns'] - a); c = d <= 2e-4; ok &= c
    L.append(f"{name}: N_tot {Ne:.2f} | PyT n_s {a:.6f} (tol 1e-10: {b:.6f}) | Janus-MF n_s {J['ns']:.6f} r {J['r']:.5f} |d| {d:.1e} {'PASS' if c else 'FAIL'} | adiabatic P_R(1)/P_R(0)-1 {J1['PR']/J['PR']-1:+.1e}")
    print(L[-1], flush=True)
L.append('JMF8: ' + ('JANUS-MF VALIDATED FOR THREE FIELDS' if ok else 'NOT VALIDATED')); R = 'field_tests/results/janus_jmf8.txt'; open(R, 'w').write('\n'.join(L) + '\n'); print(L[-1])
stamp(R, lock='field_tests/rules/PREREG_JMF8_threefield.md', code=['theory/janus/jmf8_threefield.py', 'tools/janus_calc/mfms.py'], t0=t0)
