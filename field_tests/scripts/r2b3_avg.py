import sys, math, numpy as np
from multiprocessing import Pool
sys.path.insert(0, 'tools/janus_astro')
import sommerfeld_nlo as N, sommerfeld as Sm
M = 2000.0; G = np.array([[2, math.sqrt(2)], [math.sqrt(2), 3]]); C = 0.0917
def Sclosed(n):
    x = 1 - C/n**2; v = 2*math.sqrt(x*2*N.DM/M); s = np.asarray(N.wino_s_nlo(M, v, nlo=False)); return float(s @ G @ s)
def Vfun(r):
    off = -math.sqrt(2)*N.ALPHA2*math.exp(-N.MW*r)/r
    return np.array([[0.0, off], [off, -N.ALPHA/r - N.ALPHA2*N.CW2*math.exp(-N.MZ*r)/r]])
def Sopen(x):
    v = 2*math.sqrt(x*2*N.DM/M); s = Sm.two_channel_open(M, v, Vfun, N.DM, tails=(0.0, N.ALPHA))[0]; return float(np.real(s @ G @ s.conj()))
if __name__ == '__main__':
    a, b = 6.036, 7.036; n = np.linspace(a, b, 2001)
    with Pool(2) as p: S = np.array(p.map(Sclosed, n))
    dx = lambda k: np.trapezoid(S[::k]*2*C/n[::k]**3, n[::k]) / ((1 - C/b**2) - (1 - C/a**2))
    np.save("field_tests/results/r2b3_S_grid.npy", np.vstack([n, S]))
    A1, A2 = dx(2), dx(1); conv = abs(A1/A2 - 1)
    xs = [1.01, 1.02, 1.05, 1.1, 1.2]
    with Pool(2) as p: So = p.map(Sopen, xs)
    c = np.polyfit(np.array(xs) - 1, So, 2); Sp = c[-1]
    print("open S:", [round(s, 3) for s in So], " S+ (x->1) =", round(Sp, 3))
    print(f"<S> N=1001: {A1:.4f}  N=2001: {A2:.4f}  conv={conv:.4f} ({'OK' if conv <= 0.05 else 'NOT CONVERGED'})")
    print(f"max S on grid {S.max():.4g}, min {S.min():.4g}")
    r = A2/Sp - 1; print(f"ratio-1 = {r:.4f} -> " + ("INCONCLUSIVE" if conv > 0.05 else ("PASS" if abs(r) <= 0.2 else "FAIL")))
