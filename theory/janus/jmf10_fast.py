"""JMF10 (locked PREREG_JMF10_fast)."""
import sys, time, numpy as np; sys.path.insert(0, '.')
from tools.janus_calc.mfms import spectra_mf, spectra_mf_fast
def quad(m1, m2, c=0.0, l1=0.0, l2=0.0):   # V = ½m1φ1² + ½m2φ2² + c φ1φ2 + (1/24)φ1²(l1 φ1² + l2 φ2²)
    V = lambda x: 0.5*m1*x[0]**2 + 0.5*m2*x[1]**2 + c*x[0]*x[1] + x[0]**2*(l1*x[0]**2 + l2*x[1]**2)/24
    g = lambda x: np.array([m1*x[0] + c*x[1] + (4*l1*x[0]**3 + 2*l2*x[0]*x[1]**2)/24, m2*x[1] + c*x[0] + 2*l2*x[0]**2*x[1]/24])
    h = lambda x: np.array([[m1 + (12*l1*x[0]**2 + 2*l2*x[1]**2)/24, c + 4*l2*x[0]*x[1]/24], [c + 4*l2*x[0]*x[1]/24, m2 + 2*l2*x[0]**2/24]])
    return V, g, h
MODELS = {'Q1': (quad(1e-11, 1e-11), [12.0, 12.0]), 'Q3': (quad(1e-11, 9e-11), [12.0, 12.0]), 'Q9': (quad(1e-11, 81e-11), [12.0, 12.0]),
          'N2p': (quad(1e-11, 9e-11, 1e-12), [12.0, 12.0]), 'N1': (quad(1e-11, 9e-11, 0, 1e-12, 1e-12), [12.5, 12.5])}
L = []; F1 = True; F2 = True; s1 = []; s2 = []
for nm, ((V, g, h), f0) in MODELS.items():
    t = time.time(); a = spectra_mf(V, g, h, f0); ta = time.time() - t
    t = time.time(); b = spectra_mf_fast(V, g, h, f0); tb = time.time() - t
    t = time.time(); c = spectra_mf_fast(V, g, h, f0, bd=300.0); tc = time.time() - t
    d1 = (abs(b['ns'] - a['ns']), abs(b['r']/a['r'] - 1)); d2 = (abs(c['ns'] - a['ns']), abs(c['r']/a['r'] - 1))
    o1 = d1[0] <= 1e-6 and d1[1] <= 1e-5; o2 = d2[0] <= 1e-6 and d2[1] <= 1e-5; F1 &= o1; F2 &= o2; s1.append(ta/tb); s2.append(ta/tc)
    L.append(f"{nm}: n_s {a['ns']:.8f} r {a['r']:.6f} ({ta:.2f} s) | fast |dn_s| {d1[0]:.1e} |dr/r| {d1[1]:.1e} ({tb:.2f} s, x{ta/tb:.1f}) {o1} | quick |dn_s| {d2[0]:.1e} |dr/r| {d2[1]:.1e} ({tc:.2f} s, x{ta/tc:.1f}) {o2}")
    print(L[-1], flush=True)
F1 &= bool(np.median(s1) >= 3); F2 &= bool(np.median(s2) >= 8)
L.append(f"median speed-up fast x{np.median(s1):.1f}, quick x{np.median(s2):.1f} | F1 {F1} F2 {F2}")
open('field_tests/results/janus_jmf10.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
