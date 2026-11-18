"""JMF11 (locked PREREG_JMF11_jit)."""
import sys, time, numpy as np, sympy as sp; sys.path.insert(0, '.')
from tools.janus_calc.mfms import spectra_mf
from tools.janus_calc.mf_jit import build, spectra_jit
src = open('theory/janus/jmf10_fast.py').read(); exec(src[src.index('def quad'):src.index('L = []; F1')])
f = sp.symarray('f', 2); F = sp.Float
def sym(m1, m2, c=0.0, l1=0.0, l2=0.0): return F(m1)/2*f[0]**2 + F(m2)/2*f[1]**2 + F(c)*f[0]*f[1] + f[0]**2*(F(l1)*f[0]**2 + F(l2)*f[1]**2)/24
SYM = {'Q1': sym(1e-11, 1e-11), 'Q3': sym(1e-11, 9e-11), 'Q9': sym(1e-11, 81e-11), 'N2p': sym(1e-11, 9e-11, 1e-12), 'N1': sym(1e-11, 9e-11, 0, 1e-12, 1e-12)}
L = []; ok = True; sp_ = []
for nm, ((V, g, h), f0) in MODELS.items():
    t = time.time(); a = spectra_mf(V, g, h, f0); ta = time.time() - t
    t = time.time(); m = build(SYM[nm], f); spectra_jit(m, f0, rtol=1e-11); tc = time.time() - t     # includes compile
    t = time.time(); b = spectra_jit(m, f0, rtol=1e-11); tb = time.time() - t
    t = time.time(); q = spectra_jit(m, f0, rtol=1e-11, bd=300.0); tq = time.time() - t
    d = (abs(b['ns'] - a['ns']), abs(b['r']/a['r'] - 1)); o = d[0] <= 1e-6 and d[1] <= 1e-5; ok &= o; sp_.append(ta/tb)
    L.append(f"{nm}: ref n_s {a['ns']:.8f} ({ta:.2f} s) | jit |dn_s| {d[0]:.1e} |dr/r| {d[1]:.1e} {tb:.3f} s x{ta/tb:.0f} {o} (first call incl. compile {tc:.1f} s) | jit quick |dn_s| {abs(q['ns']-a['ns']):.1e} {tq:.3f} s x{ta/tq:.0f}")
    print(L[-1], flush=True)
J1 = ok and bool(np.median(sp_) >= 20)
L.append(f"median speed-up x{np.median(sp_):.0f} | J1 {J1} -> {'ADOPTED (PC default, labelled jit)' if J1 else 'NOT ADOPTED'}")
open('field_tests/results/janus_jmf11.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
