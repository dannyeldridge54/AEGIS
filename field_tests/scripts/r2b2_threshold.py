import sys, math, numpy as np
sys.path.insert(0, 'tools/janus_astro')
import sommerfeld_nlo as N, sommerfeld as S
M = 2000.0; G = np.array([[2, math.sqrt(2)], [math.sqrt(2), 3]])
def Vfun(r):
    off = -math.sqrt(2)*N.ALPHA2*math.exp(-N.MW*r)/r
    return np.array([[0.0, off], [off, -N.ALPHA/r - N.ALPHA2*N.CW2*math.exp(-N.MZ*r)/r]])
out = {}
for x in [0.95, 0.99, 1.01, 1.05, 1.2, 1.5]:
    E = x*2*N.DM; v = 2*math.sqrt(E/M)
    if x < 1: s = np.asarray(N.wino_s_nlo(M, v, nlo=False), complex)
    else: s = S.two_channel_open(M, v, Vfun, N.DM, tails=(0.0, N.ALPHA))[0]
    Sv = float(np.real(s @ G @ s.conj()))
    out[x] = Sv; print(f"E/2dm={x:5.2f} v={v:.4e} S={Sv:.5g} |s00|2={abs(s[0])**2:.5g} |s0+|2={abs(s[1])**2:.5g}")
j = abs(out[1.01]/out[0.99] - 1); print(f"jump={j:.4f} -> {'PASS' if j <= 0.2 else 'FAIL'}")
