"""A1b — PREREG_A1b_resonance.md"""
import sys, math; sys.path.insert(0, '.')
import numpy as np
from scipy.optimize import minimize_scalar
import tools.janus_astro.sommerfeld as S
def peak(aw, dm):
    f = lambda M: -float(np.dot(S.wino_s(M*1e3, v=1e-6, alpha_w=aw, dm=dm)**2, [2, 3]) + 2*math.sqrt(2)*np.prod(S.wino_s(M*1e3, v=1e-6, alpha_w=aw, dm=dm)))/M**2
    Ms = np.arange(2.10, 2.501, 0.01); v = [f(M) for M in Ms]; i = int(np.argmin(v))
    r = minimize_scalar(f, bracket=(Ms[max(i-1,0)], Ms[i], Ms[min(i+1,len(Ms)-1)]), tol=1e-8); return r.x
out = []
d = (S.S_W2, S.M_W, S.M_Z, S.ALPHA_W, S.DM); p0 = peak(S.ALPHA_W, S.DM)
mw, mz = 80.385, 91.1876; sw2 = 1 - (mw/mz)**2; a2 = (1/128.943)/sw2
S.S_W2, S.M_W, S.M_Z = sw2, mw, mz
p1 = peak(a2, 0.1641); S.S_W2, S.M_W, S.M_Z = d[0], d[1], d[2]
T1 = abs(p1/2.282 - 1) <= 0.01
out.append(f"their inputs: s_W2={sw2:.5f} alpha2={a2:.5f} -> peak {p1:.4f} TeV vs 2.282 (rel {p1/2.282-1:+.4f}) -> {'PASS' if T1 else 'FAIL'}")
out.append(f"our defaults (alpha_W {d[3]}, s_W2 {d[0]}, dm {d[4]}): peak {p0:.4f} TeV")
out.append(f"NLO shift quoted +0.137 TeV -> D1081 CMB band ~2.0-2.7 TeV moves to ~{2.0+p1 and 2.137:.2f}-{2.837:.2f} TeV [estimate, rigid shift]")
out.append("A1b VALIDATED" if T1 else "A1b NOT VALIDATED")
open('field_tests/results/a1b_resonance.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
