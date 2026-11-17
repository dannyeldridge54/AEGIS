import sys, math; sys.path.insert(0, '.')
import numpy as np
from scipy.optimize import minimize_scalar
from tools.janus_astro import sommerfeld_nlo as N
def peak(lo, hi, **kw):
    def f(M):
        s = N.wino_s_nlo(M*1e3, **kw); return -(2*s[0]**2 + 2*math.sqrt(2)*s[0]*s[1] + 3*s[1]**2)/M**2
    Ms = np.arange(lo, hi+1e-9, 0.01); v = [f(M) for M in Ms]; i = int(np.argmin(v))
    return minimize_scalar(f, bracket=(Ms[max(i-1,0)], Ms[i], Ms[min(i+1,len(Ms)-1)]), tol=1e-8).x
out = []
p0 = peak(2.20, 2.40, nlo=False); T0 = abs(p0 - 2.2855) <= 1e-4*2.2855
out.append(f"T0 NLO off: {p0:.5f} TeV vs A1b 2.2855 -> {'PASS' if T0 else 'FAIL'}")
p1 = peak(2.25, 2.65, nlo=True); T1 = abs(p1/2.419 - 1) <= 0.01
out.append(f"T1 NLO primary: {p1:.4f} TeV vs 2.419 (rel {p1/2.419-1:+.4f}) -> {'PASS' if T1 else 'FAIL'}")
try:
    p2 = peak(2.25, 2.65, nlo=True, off_factor=math.sqrt(2)); out.append(f"alt (x sqrt2): {p2:.4f} TeV (rel {p2/2.419-1:+.4f}) [reported]")
except Exception as e: out.append(f"alt failed: {e}")
out.append("A1c VALIDATED" if T0 and T1 else "A1c NOT VALIDATED")
open('field_tests/results/a1c_nlo.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
