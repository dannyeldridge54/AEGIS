import sys, math, cmath, numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, 'tools/janus_astro')
import sommerfeld_nlo as N
M = 2000.0; G = np.array([[2, math.sqrt(2)], [math.sqrt(2), 3]]); A0 = N.ALPHA
def Vfun(r):
    off = -math.sqrt(2)*N.ALPHA2*math.exp(-N.MW*r)/r
    return np.array([[0.0, off], [off, -A0/r - N.ALPHA2*N.CW2*math.exp(-N.MZ*r)/r]])
def solve(x, dm=N.DM, tails=(0.0, A0)):
    # copy of sommerfeld.two_channel_open integration (incoming channel 0), plus outgoing amplitudes
    E = x*2*dm; v = 2*math.sqrt(E/M); thr = np.array([0.0, 2*dm]); k = np.sqrt(M*(E - thr)); R = 300/min(k)
    V = lambda r: Vfun(r) + np.diag(thr); cols = []
    for j in range(2):
        y0 = np.zeros(4); y0[j] = 1e-9; y0[2+j] = 1.0
        s = solve_ivp(lambda r, y: np.concatenate([y[2:], M*(V(r) - E*np.eye(2)) @ y[:2]]), [1e-9, R], y0, method='DOP853', rtol=1e-10, atol=1e-16)
        cols.append(s.y[:, -1])
    U = np.array([c[:2] for c in cols]).T; Up = np.array([c[2:] for c in cols]).T
    B = np.zeros((2, 2), complex); A = np.zeros((2, 2), complex); kl = np.zeros(2)
    for ch in range(2):
        kl[ch] = math.sqrt(M*(E - thr[ch] + tails[ch]/R))
        for sol in range(2):
            u, up = U[ch, sol], Up[ch, sol]
            B[ch, sol] = 0.5*(u - up/(1j*kl[ch]))*math.sqrt(kl[ch]/k[ch])   # incoming (e^{-i phi}) coefficient
            A[ch, sol] = 0.5*(u + up/(1j*kl[ch]))*math.sqrt(kl[ch]/k[ch])   # outgoing (e^{+i phi}) coefficient
    tgt = -1/(2j*k[0])*cmath.exp(-1j*kl[0]*R)
    c = np.linalg.solve(B, np.array([tgt, 0]))
    a = A @ c
    P = k[1]*abs(a[1])**2/(k[0]*abs(1/(2*k[0]))**2); S00 = abs(a[0])/abs(1/(2*k[0]))
    return c, P, S00, k
c, P, S00, k = solve(1.01)
Sann = float(np.real(c @ G @ c.conj()))
print(f"self-check S_ann = {Sann:.4f} (locked ref 36.20) -> {'OK' if abs(Sann-36.20) <= 1e-3*36.20 else 'STOP'}")
Sconv = 2*P*M/(k[0]*N.ALPHA2**2)
print(f"k0={k[0]:.4f} k1={k[1]:.4f}  P_conv={P:.5g}  |S00|={S00:.6f}  |S00|^2+P={S00**2+P:.6f}")
print(f"S_conv(A)={Sconv:.4g}  S_conv(B)={2*Sconv:.4g}")
avg = 107.61
for lab, sc in [('A', Sconv), ('B', 2*Sconv)]:
    r = avg/(Sann + sc) - 1; print(f"conv {lab}: S_ann+S_conv={Sann+sc:.4g}  <S>/(..)-1 = {r:+.4f} -> {'PASS' if abs(r) <= 0.2 else 'FAIL'}")
