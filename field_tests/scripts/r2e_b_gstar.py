"""R2e-b (PREREG_R2e_b_gstar): wino relic with Saikawa-Shirai g_*(T), h_*(T); otherwise as R2e-a."""
import sys, math, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, 'tools/janus_astro'); sys.path.insert(0, 'field_tests/scripts')
import relic, sommerfeld_nlo as N
from r2c_b_alls import run
from r2e_a_alpha import a2hat, XS, AOS
D = np.loadtxt('field_tests/data/saikawa_shirai_2020_gstar.dat'); LT = np.log(D[:, 0])
def gs(T): return float(np.interp(math.log(T), LT, D[:, 2]))
def gr(T): return float(np.interp(math.log(T), LT, D[:, 3]))
def gstar_half(T, h=1e-3):
    dlnh = (math.log(gs(T*math.exp(h))) - math.log(gs(T*math.exp(-h))))/(2*h)
    return gs(T)/math.sqrt(gr(T))*(1 + dlnh/3)
def omega(m, Rfun, x0=3.0, xend=1e8, geff=6.0):
    sv = relic.sigma_eff_born(m, AOS)[0]*(a2hat(2*m)/AOS)**2
    lam0 = math.sqrt(math.pi/45)*relic.MPL*m*sv
    yeq = lambda x: 45/(4*math.pi**4)*geff/gs(m/x)*x**1.5*math.exp(-x)*math.sqrt(math.pi/2) if x < 700 else 0.0
    rhs = lambda x, y: [-lam0*gstar_half(m/x)*Rfun(x)/x**2*(y[0]**2 - yeq(x)**2)]
    s = solve_ivp(rhs, [x0, xend], [yeq(x0)], method='Radau', rtol=1e-8, atol=1e-20)
    Y = float(s.y[0, -1]); return m*Y*relic.S0/relic.RHOC_H2, Y
if __name__ == '__main__':
    one = lambda x: 1.0
    mB = brentq(lambda m: omega(m, one)[0] - 0.1205, 1500, 4000)
    mB1 = brentq(lambda m: omega(m, one, x0=1.0)[0] - 0.1205, 1500, 4000)
    print(f"g*^1/2 at T=100 GeV: {gstar_half(100):.3f} (sqrt(106.75)={math.sqrt(106.75):.3f}); at 1 GeV: {gstar_half(1.0):.3f}; at 0.1 GeV: {gstar_half(0.1):.3f}", flush=True)
    print(f"B1 Born M_th = {mB/1e3:.4f} TeV vs Beneke 2.207 (rel {mB/2207-1:+.4f}) -> {'PASS' if abs(mB/2207-1) <= 0.03 else 'FAIL'}; R2e-a was 2.325; start x=1: {mB1/1e3:.4f}", flush=True)
    Ms = [2200.0, 2400.0, 2600.0, 2800.0, 3000.0, 3200.0]
    r = run(Ms, XS, [40]); lx = np.log(XS); om = {}
    for M in Ms:
        R = np.array([r[(M, x, 40)][0] for x in XS])
        Rf = lambda x, R=R: float(np.interp(math.log(min(max(x, 3.0), 3e4)), lx, R))
        om[M] = omega(M, Rf)[0]; print(f"M={M/1e3:.1f}: Oh2={om[M]:.4f}", flush=True)
    lm = np.log(Ms); lo = np.log([om[M] for M in Ms])
    Mth = math.exp(brentq(lambda q: np.interp(q, lm, lo) - math.log(0.1205), lm[0], lm[-1])) if lo.min() < math.log(0.1205) < lo.max() and np.all(np.diff(lo) > 0) else float('nan')
    print(f"L1 LO-Sommerfeld M_th = {Mth/1e3:.3f} TeV vs Beneke 2.886 (rel {Mth/2886-1:+.3f}) -> {'PASS' if abs(Mth/2886-1) <= 0.03 else 'FAIL'}; R2e-a was 3.135")
