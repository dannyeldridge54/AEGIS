"""JMF9 (locked PREREG_JMF9_curved)."""
import sys, os, time, importlib, math, numpy as np, sympy as sp; sys.path.insert(0, '.')
PT = '/home/claude/ext/PyTransport/PyTransport'; sys.path += [PT, PT + '/PyTrans']
import PyTransScripts as S
from tools.janus_calc.mfms_nc import build, spectra_nc
from tools.janus_calc.mfms import spectra_mf
from tools.lockbench.provenance import stamp
t0 = time.time(); L = []; f = sp.symarray('f', 2)
# self-check: flat metric reproduces spectra_mf on DQuad (Q3)
m1, m2 = 1e-11, 9e-11; Vf = lambda x: 0.5*m1*x[0]**2 + 0.5*m2*x[1]**2
gf = lambda x: np.array([m1*x[0], m2*x[1]]); hf = lambda x: np.diag([m1, m2])
ref = spectra_mf(Vf, gf, hf, [12.0, 12.0])['ns']
mf = build(sp.Rational(1, 2)*(m1*f[0]**2 + m2*f[1]**2), [[1, 0], [0, 1]], f)
x0 = np.array([12.0, 12.0]); v0 = -gf(x0)/Vf(x0); eps0 = 0.5*v0 @ v0; H0 = math.sqrt(Vf(x0)/(3 - eps0))
nc = spectra_nc(mf, x0, H0*v0)['ns']; d0 = abs(nc - ref); okS = d0 <= 1e-6
L.append(f"self-check flat DQuad Q3: spectra_mf {ref:.8f} | NC code {nc:.8f} | |d| {d0:.1e} {'PASS' if okS else 'FAIL'}"); print(L[-1], flush=True)
# DoubleQuadNC (PyTransport example values)
M = 0.5e-6; p = np.array([0.002*M**2, 0.004*M**2, 1.0]); fi = np.array([0.4, 20.0])
PyT = importlib.import_module('PyTransJNC_DQuad')
def ns_pyt(tol):
    V = PyT.V(fi, p); dV = PyT.dV(fi, p); ic = np.concatenate([fi, -dV/np.sqrt(3*V)])
    back = PyT.backEvolve(np.linspace(0, 300, 6000), ic, p, np.array([tol, tol]), True); Ne = back[-1, 0]
    ks = S.kexitN(Ne - 55.0, back, p, PyT); lk = np.log(ks) + np.linspace(-0.4, 0.4, 9)
    zz, _ = S.pSpectra(np.exp(lk), back, p, 6.0, np.array([tol, tol]), PyT)
    c = np.polyfit(lk - np.log(ks), np.log(zz), 2); return c[1] + 4.0, Ne, -dV/np.sqrt(3*V)
sys.stdout = open(os.devnull, 'w'); a, NeP, fd = ns_pyt(1e-8); b, _, _ = ns_pyt(1e-10); sys.stdout = sys.__stdout__
mn = build(sp.Rational(1, 2)*p[0]**2*f[0]**2 + sp.Rational(1, 2)*p[1]**2*f[1]**2, [[p[2]**2, 0], [0, p[2]**2*sp.sin(f[0])**2]], f)
J = spectra_nc(mn, fi, fd); d = abs(J['ns'] - a); ok = d <= 2e-4
L.append(f"DoubleQuadNC: N_tot PyT {NeP:.3f} / Janus {J['Ne']:.3f} | PyT n_s {a:.6f} (tol 1e-10: {b:.6f}) | Janus-MF-NC {J['ns']:.6f} | |d| {d:.1e} {'PASS' if ok else 'FAIL'}")
L.append("JMF9: " + ("SELF-CHECK FAILED (fix via DEVIATIONS)" if not okS else ("JANUS-MF VALIDATED ON CURVED FIELD SPACE" if ok else "NOT VALIDATED")))
R = 'field_tests/results/janus_jmf9.txt'; open(R, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
stamp(R, lock='field_tests/rules/PREREG_JMF9_curved.md', code=['theory/janus/jmf9_curved.py', 'tools/janus_calc/mfms_nc.py'], t0=t0)
