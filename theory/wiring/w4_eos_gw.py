import sys, math, numpy as np; sys.path.insert(0, '.')
from tools.janus_astro import ns, gw, const as K
MS = 1.98840987e30; M1 = M2 = 1.4*MS
fmax = 0.8*K.c**3/(6**1.5*math.pi*K.G*(M1+M2)); f = np.linspace(20, fmax, 20000)
def detr(y): A = np.vstack([np.ones_like(f), f]).T; co, *_ = np.linalg.lstsq(A, y, rcond=None); return y - A @ co
out = []; ph = {}; T1 = True
for name, ref in (('SLy', 296), ('AP4', 248)):
    L = ns.at_mass(ns.PPEOS(*ns.TABLE3[name]), 1.4)[3]
    chain = gw.taylorf2_tidal_dphase(f, M1, M2, L, L, 6); direct = gw.taylorf2_tidal_dphase(f, M1, M2, float(L), float(L), 6)
    T1 &= bool(np.array_equal(chain, direct)); ph[name] = detr(chain)
    out.append(f"{name}: Lambda_1.4 = {L:.1f} (ref {ref}) -> {'OK' if abs(L-ref) <= 1 else 'OFF'}; tidal phase span {np.ptp(ph[name]):.3f} rad")
d = ph['SLy'] - ph['AP4']
out.append(f"SLy - AP4 tidal phase difference (detrended, max abs): {np.max(np.abs(d)):.3f} rad (estimate in D1098: ~0.13)")
out.append(f"T1 lossless: {T1}")
open('field_tests/results/w4_eos_gw.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
