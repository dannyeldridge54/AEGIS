import sys, math; sys.path.insert(0, '.')
import numpy as np
from tools.janus_astro import sommerfeld as S, sommerfeld_nlo as N
M = 2000.0; out = []; w1 = w2 = 0.0
for v in (0.1, 0.3):
    s = S.two_channel_open(M, v, lambda r: np.zeros((2, 2)), 0.0); e = np.max(np.abs(np.abs(s) - np.eye(2))); w1 = max(w1, e)
    out.append(f"T1 v={v}: max||s|-I| = {e:.1e}")
a, a2, cw2, mW, mZ = N.ALPHA, N.ALPHA2, N.CW2, N.MW, N.MZ
d11 = lambda r: -a/r - a2*cw2*math.exp(-mZ*r)/r
for v in (0.1, 0.3):
    s = S.two_channel_open(M, v, lambda r: np.array([[0.0, 0.0], [0.0, d11(r)]]), 0.0, tails=(0.0, a))
    s0 = abs(s[0, 0])**2; s1 = abs(s[1, 1])**2; r1 = S.single_channel(M, v, d11, a)
    e = max(abs(s0 - 1), abs(s1/r1 - 1)); w2 = max(w2, e)
    out.append(f"T2 v={v}: |s00|^2={s0:.6f} (free 1); |s11|^2={s1:.6f} vs single {r1:.6f} -> {e:.1e}")
dm = N.DM
off = lambda r: -math.sqrt(2)*a2*math.exp(-mW*r)/r
Vw = lambda r: np.array([[0.0, off(r)], [off(r), d11(r)]])
vthr = math.sqrt(4*1.01*2*dm/M); s = S.two_channel_open(M, vthr, Vw, dm, tails=(0.0, a))
vb = math.sqrt(4*0.99*2*dm/M); sb = N.wino_s_nlo(M, v=vb, nlo=False)
out.append(f"T3 threshold: open |s00,00|^2={abs(s[0,0])**2:.4f} vs closed (wino_s) {sb[0]**2:.4f}")
for v in (0.1, 0.3):
    s = S.two_channel_open(M, v, Vw, dm, tails=(0.0, a)); out.append(f"wino LO v={v}: |s|^2 = {np.round(np.abs(s)**2, 4).tolist()}")
ok = w1 <= 1e-6 and w2 <= 1e-4
out.append(f"T1 worst {w1:.1e}, T2 worst {w2:.1e} -> R2b {'VALIDATED' if ok else 'NOT VALIDATED'}")
open('field_tests/results/r2b_twochannel.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
