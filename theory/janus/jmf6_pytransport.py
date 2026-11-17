"""JMF6 (locked PREREG_JMF6_pytransport)."""
import sys, os, time, importlib, numpy as np, sympy as sym; sys.path.insert(0, '.')
PT = '/home/claude/ext/PyTransport/PyTransport'; sys.path += [PT, PT + '/PyTrans']
import PyTransSetup, PyTransScripts as S
from tools.lockbench.provenance import stamp
t0 = time.time(); f = sym.symarray('f', 2); p = sym.symarray('p', 4); h = sym.Rational(1, 2)
MODELS = {  # name: (V, params, phi_init, Janus-MF n_s, MMC n_s or None)
 'Q1': (h*p[0]*f[0]**2 + h*p[1]*f[1]**2, [1e-11, 1e-11, 0, 0], [12.0, 12.0], 0.963378, 0.963372),
 'Q3': (h*p[0]*f[0]**2 + h*p[1]*f[1]**2, [1e-11, 9e-11, 0, 0], [12.0, 12.0], 0.945477, 0.945477),
 'Q9': (h*p[0]*f[0]**2 + h*p[1]*f[1]**2, [1e-11, 81e-11, 0, 0], [12.0, 12.0], 0.927750, 0.927745),
 'N2p': (h*p[0]*f[0]**2 + h*p[1]*f[1]**2 + p[2]*f[0]*f[1], [1e-11, 9e-11, 1e-12, 0], [12.0, 12.0], 0.946212, None),
 'N1': (h*p[0]*f[0]**2 + h*p[1]*f[1]**2 + sym.Rational(1, 24)*f[0]**2*(p[2]*f[0]**2 + p[3]*f[1]**2), [1e-11, 9e-11, 1e-12, 1e-12], [12.5, 12.5], 0.954583, None)}
def ns(M, pv, f0, tol):
    V = M.V(f0, pv); dV = M.dV(f0, pv); ic = np.concatenate([f0, -dV/np.sqrt(3*V)])
    back = M.backEvolve(np.linspace(0, 300, 6000), ic, pv, np.array([tol, tol]), True); Ne = back[-1, 0]
    ks = S.kexitN(Ne - 55.0, back, pv, M); lk = np.log(ks) + np.linspace(-0.4, 0.4, 9)
    zz, _ = S.pSpectra(np.exp(lk), back, pv, 6.0, np.array([tol, tol]), M)
    c = np.polyfit(lk - np.log(ks), np.log(zz), 2); return c[1] + 4.0, Ne
L = []; c0 = True; c1 = True
for name, (V, pv, f0, nj, nm) in MODELS.items():
    mod = 'J6' + name; PyTransSetup.potential(V, 2, 4, False); PyTransSetup.compileName3(mod, False)
    M = importlib.import_module('PyTrans' + mod); pv = np.array(pv, float); f0 = np.array(f0, float)
    sys.stdout = open(os.devnull, 'w'); a, Ne = ns(M, pv, f0, 1e-8); b, _ = ns(M, pv, f0, 1e-10); sys.stdout = sys.__stdout__
    d1 = abs(a - nj); ok1 = d1 <= 2e-4; c1 &= ok1; s = f"{name}: N_tot {Ne:.2f} | PyT n_s {a:.6f} (tol 1e-10: {b:.6f}) | Janus-MF {nj} |d| {d1:.1e} {'PASS' if ok1 else 'FAIL'}"
    if nm is not None: d0 = abs(a - nm); ok0 = d0 <= 2e-4; c0 &= ok0; s += f" | MMC {nm} |d| {d0:.1e} C0 {'PASS' if ok0 else 'FAIL'}"
    L.append(s); print(s, flush=True)
v = 'INCONCLUSIVE (reference does not reproduce MMC)' if not c0 else ('JANUS-MF VALIDATED ON NON-SEPARABLE (independent reference)' if c1 else 'NOT VALIDATED')
L.append(f'C0 {c0} C1 {c1} -> JMF6: {v}'); R = 'field_tests/results/janus_jmf6.txt'; open(R, 'w').write('\n'.join(L) + '\n'); print(L[-1])
stamp(R, lock='field_tests/rules/PREREG_JMF6_pytransport.md', code=['theory/janus/jmf6_pytransport.py', 'tools/janus_calc/pytransport_build.patch'], t0=t0)
