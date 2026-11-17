import sys, math, numpy as np
from multiprocessing import Pool
from scipy.special import erf
sys.path.insert(0, 'tools/janus_astro')
import sommerfeld_nlo as N, sommerfeld as Sm
G = np.array([[2, math.sqrt(2)], [math.sqrt(2), 3]]); A0 = N.ALPHA
def Vfun(r):
    off = -math.sqrt(2)*N.ALPHA2*math.exp(-N.MW*r)/r
    return np.array([[0.0, off], [off, -A0/r - N.ALPHA2*N.CW2*math.exp(-N.MZ*r)/r]])
def S(args):
    M, v = args; s = Sm.two_channel_open(M, v, Vfun, N.DM, tails=(0.0, A0))[0]; return float(np.real(s @ G @ s.conj()))
def cdf(v, x):   # Maxwell CDF for w ∝ v² e^{-x v²/4}: a = sqrt(x)/2
    a = math.sqrt(x)/2; z = a*v; return erf(z) - 2*z*math.exp(-z*z)/math.sqrt(math.pi)
if __name__ == '__main__':
    out = []
    for M in [2000.0, 2842.0]:
        vth = 2*math.sqrt(2*N.DM/M); vb = [2*math.sqrt(xe*2*N.DM/M) for xe in (0.9, 1.1)]
        grids = {n: np.geomspace(1.001*vth, 2.0, n) for n in (40, 80)}
        allv = sorted(set(np.round(np.concatenate(list(grids.values())), 14)))
        with Pool(2) as p: Sv = dict(zip(allv, p.map(S, [(M, v) for v in allv])))
        for x in [20, 25, 30]:
            w = lambda v: v**2*np.exp(-x*v**2/4)
            Z = math.sqrt(math.pi)*(4/x)**1.5/4   # ∫0^∞ v² e^{-x v²/4} dv
            res = {}
            for n, g in grids.items():
                sv = np.array([Sv[round(v, 14)] for v in g])
                res[n] = (np.trapezoid(sv*w(g), g) + 2.0*0)/ (np.trapezoid(w(g), g))/2.0
            conv = abs(res[40]/res[80] - 1)
            line = (f"M={M:.0f} x={x}: R00(n40)={res[40]:.5f} R00(n80)={res[80]:.5f} conv={conv:.2e} {'OK' if conv <= 0.01 else 'NOT CONVERGED'} | "
                    f"w(v<vth)={cdf(vth, x):.2e} w(band)={cdf(vb[1], x)-cdf(vb[0], x):.2e} w(v>2)={1-cdf(2.0, x):.2e}")
            print(line, flush=True)
