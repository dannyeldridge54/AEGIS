import sys, math, numpy as np
sys.path.insert(0, 'tools/janus_astro')
import sommerfeld_nlo as N, sommerfeld as Sm
N.ALPHA = 0.0
M = 2000.0; G = np.array([[2, math.sqrt(2)], [math.sqrt(2), 3]])
def Vfun(r):
    off = -math.sqrt(2)*N.ALPHA2*math.exp(-N.MW*r)/r
    return np.array([[0.0, off], [off, -N.ALPHA2*N.CW2*math.exp(-N.MZ*r)/r]])
o = {}
for x in [0.95, 0.99, 0.999, 1.001, 1.01, 1.05]:
    v = 2*math.sqrt(x*2*N.DM/M)
    s = np.asarray(N.wino_s_nlo(M, v, nlo=False), complex) if x < 1 else Sm.two_channel_open(M, v, Vfun, N.DM, tails=(0.0, 0.0))[0]
    S = float(np.real(s @ G @ s.conj())); o[x] = S
    print(f"x={x:6.3f} S={S:.5g} |s0|2={abs(s[0])**2:.5g} |s1|2={abs(s[1])**2:.5g}")
j = abs(o[1.01]/o[0.99] - 1); print(f"jump={j:.4f} -> {'PASS' if j <= 0.2 else 'FAIL'}")
