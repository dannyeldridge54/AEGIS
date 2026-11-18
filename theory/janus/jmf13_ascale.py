"""JMF13 (locked PREREG_JMF13_ascale)."""
import sys, math, time, numpy as np, sympy as sp; sys.path.insert(0, '.')
from tools.janus_calc.mfms import spectra_mf, spectra_mf_fast
from tools.janus_calc.mf_jit import build as bmf, spectra_jit
from tools.janus_calc.mfms_nc import build as bnc, spectra_nc
from tools.janus_calc.mfms_nc_jit import build as bncj, spectra_ncjit
L = []; A1 = True; A2 = True; F = sp.Float; f = sp.symarray('f', 2)
m1, m2 = 1e-11, 9e-11; Vf = lambda x: 0.5*m1*x[0]**2 + 0.5*m2*x[1]**2; gf = lambda x: np.array([m1*x[0], m2*x[1]]); hf = lambda x: np.diag([m1, m2])
for nm, fn, old in (('spectra_mf', lambda: spectra_mf(Vf, gf, hf, [12.0, 12.0])['ns'], 0.94547697), ('spectra_mf_fast', lambda: spectra_mf_fast(Vf, gf, hf, [12.0, 12.0])['ns'], 0.94547694),
                    ('spectra_jit', lambda: spectra_jit(bmf(F(m1)/2*f[0]**2 + F(m2)/2*f[1]**2, f), [12.0, 12.0], rtol=1e-11)['ns'], 0.94547694)):
    v = fn(); o = abs(v - old) <= 1e-7 + 5e-9; A1 &= o; L.append(f"A1 flat Q3 {nm}: {v:.9f} vs pre-fix {old} -> {o}"); print(L[-1], flush=True)
M = 0.5e-6; p = [0.002*M**2, 0.004*M**2]; Vq = F(p[0])**2/2*f[0]**2 + F(p[1])**2/2*f[1]**2; fi = np.array([0.4, 26.0])
PYT = {1.5: 0.933687, 2.0: 0.936712}
for R in (1.0, 1.5, 2.0):
    Gx = [[F(R*R), 0], [0, F(R*R)*sp.sin(f[0])**2]]; ms = bnc(Vq, Gx, f)
    Vi = float(ms['V'](fi)); dV = np.array(ms['dV'](fi), float).ravel(); fd = -dV/np.sqrt(3*Vi)
    t = time.time(); a = spectra_nc(ms, fi, fd)['ns']; ta = time.time() - t; mj = bncj(Vq, Gx, f); b = spectra_ncjit(mj, fi, fd)['ns']
    if R == 1.0:
        o = abs(a - 0.92502415) <= 1e-7 + 5e-9 and abs(b - 0.92502408) <= 1e-7 + 5e-9; A1 &= o
        L.append(f"A1 NC R=1: python {a:.9f} (pre 0.92502415), nc-jit {b:.9f} (pre 0.92502408) -> {o}")
    else:
        o = abs(a - PYT[R]) <= 2e-4 and abs(b - PYT[R]) <= 2e-4; A2 &= o
        L.append(f"A2 NC R={R}: python {a:.6f}, nc-jit {b:.6f}, PyTransport {PYT[R]} | |d| {abs(a-PYT[R]):.1e}, {abs(b-PYT[R]):.1e} -> {o}")
    print(L[-1], flush=True)
L.append(f"A1 {A1} A2 {A2} -> " + ("FIX ADOPTED in all four codes; JMF9 scope extends to R = 1.5, 2; nc-jit adopted" if A1 and A2 else "NOT ADOPTED"))
open('field_tests/results/janus_jmf13.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
