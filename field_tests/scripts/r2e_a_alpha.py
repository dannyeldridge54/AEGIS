"""R2e-a (PREREG_R2e_a_alpha): MSbar alpha2(2M) in Gamma, x_end 1e8, constant g*."""
import sys, math, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, 'tools/janus_astro'); sys.path.insert(0, 'field_tests/scripts')
import relic, sommerfeld_nlo as N
from r2c_b_alls import run
XS = list(np.geomspace(3, 3e4, 25)); AOS = N.ALPHA2; MZ = 91.1876
def a2hat(mu): return 1/(1/(0.00780372/0.232486) + (19/6)/(2*math.pi)*math.log(mu/MZ))
def omega(m, Rfun, xend, scale, gstar=106.75, geff=6.0):
    sv = relic.sigma_eff_born(m, AOS)[0]*scale
    lam = math.sqrt(math.pi/45)*relic.MPL*math.sqrt(gstar)*m*sv
    yeq = lambda x: 45/(4*math.pi**4)*geff/gstar*x**1.5*math.exp(-x)*math.sqrt(math.pi/2) if x < 700 else 0.0
    rhs = lambda x, y: [-lam*Rfun(x)/x**2*(y[0]**2 - yeq(x)**2)]
    s = solve_ivp(rhs, [3.0, xend], [yeq(3.0)], method='Radau', rtol=1e-8, atol=1e-20)
    Y = float(s.y[0, -1]); return m*Y*relic.S0/relic.RHOC_H2, Y
if __name__ == '__main__':
    one = lambda x: 1.0
    mreg = brentq(lambda m: omega(m, one, 3e4, 1.0)[0] - 0.1205, 1500, 4000)
    print(f"Regression (old inputs): {mreg/1e3:.4f} TeV vs 2.564 -> {'PASS' if abs(mreg/1e3-2.564) <= 0.002 else 'FAIL'}", flush=True)
    sc = lambda m: (a2hat(2*m)/AOS)**2
    mB = brentq(lambda m: omega(m, one, 1e8, sc(m))[0] - 0.1205, 1500, 4000)
    print(f"alpha2hat(2*2.2TeV)={a2hat(4400):.5f} (os {AOS:.5f}); B1 Born M_th={mB/1e3:.4f} TeV vs Beneke 2.207 (rel {mB/2207-1:+.4f}) -> {'PASS' if abs(mB/2207-1) <= 0.03 else 'FAIL'}", flush=True)
    Ms = [2200.0, 2400.0, 2600.0, 2800.0, 3000.0, 3200.0]
    r = run(Ms, XS, [40]); lx = np.log(XS); om = {}; om3 = {}
    for M in Ms:
        R = np.array([r[(M, x, 40)][0] for x in XS])
        Rf = lambda x, R=R: float(np.interp(math.log(min(max(x, 3.0), 3e4)), lx, R))
        om[M] = omega(M, Rf, 1e8, sc(M))[0]; om3[M] = omega(M, Rf, 3e4, sc(M))[0]
        print(f"M={M/1e3:.1f}: Oh2={om[M]:.4f} (xend 3e4: {om3[M]:.4f})", flush=True)
    lm = np.log(Ms); lo = np.log([om[M] for M in Ms])
    ok = lo.min() < math.log(0.1205) < lo.max()
    Mth = math.exp(brentq(lambda q: np.interp(q, lm, lo) - math.log(0.1205), lm[0], lm[-1])) if ok and np.all(np.diff(lo) > 0) else float('nan')
    print(f"L1 (reported) LO-Sommerfeld M_th = {Mth/1e3:.3f} TeV vs Beneke 2.886 (rel {Mth/2886-1:+.3f})")
