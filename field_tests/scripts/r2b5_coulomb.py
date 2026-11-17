import sys, math, numpy as np
sys.path.insert(0, 'tools/janus_astro')
import sommerfeld_nlo as N, sommerfeld as Sm
M = 2000.0; G = np.array([[2, math.sqrt(2)], [math.sqrt(2), 3]]); A0 = N.ALPHA
def Vf(lam):
    def V(r):
        off = -math.sqrt(2)*N.ALPHA2*math.exp(-N.MW*r)/r
        return np.array([[0.0, off], [off, -lam*A0/r - N.ALPHA2*N.CW2*math.exp(-N.MZ*r)/r]])
    return V
def S(s): return float(np.real(s @ G @ s.conj()))
def opn(x, lam, R=None):
    v = 2*math.sqrt(x*2*N.DM/M); return Sm.two_channel_open(M, v, Vf(lam), N.DM, tails=(0.0, lam*A0), R=R)[0]
x = 1.01; E = x*2*N.DM; k1 = math.sqrt(M*(E - 2*N.DM)); R0 = 300/k1
base = None
for f in [1, 2, 4]:
    s = opn(x, 1.0, f*R0); v = S(s); base = base or v
    print(f"check1 R={f}R0 ({f*R0:.1f}/GeV): S={v:.5g} |s0|2={abs(s[0])**2:.5g} |s1|2={abs(s[1])**2:.5g} dev={v/base-1:+.4f}", flush=True)
for lam in [0, 0.1, 0.3, 1.0]:
    N.ALPHA = lam*A0; v = 2*math.sqrt(0.99*2*N.DM/M); sc = np.asarray(N.wino_s_nlo(M, v, nlo=False), complex)
    so = opn(1.01, lam)
    print(f"check2 lam={lam}: closed(0.99) S={S(sc):.5g} |s0|2={abs(sc[0])**2:.5g} |s1|2={abs(sc[1])**2:.5g} | open(1.01) S={S(so):.5g} |s0|2={abs(so[0])**2:.5g} |s1|2={abs(so[1])**2:.5g}", flush=True)
