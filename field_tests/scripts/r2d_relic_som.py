"""R2d (PREREG_R2d_relic_som): LO Sommerfeld wino thermal mass."""
import sys, math, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, 'tools/janus_astro'); sys.path.insert(0, 'field_tests/scripts')
import relic, sommerfeld_nlo as N
from r2c_b_alls import run
XS = list(np.geomspace(3, 3e4, 25)); A2 = N.ALPHA2
def omega(m, Rfun, xend=3e4, gstar=106.75, geff=6.0):     # copy of relic.omega_h2 with lam -> lam*R(x)
    sv = relic.sigma_eff_born(m, A2)[0]
    lam = math.sqrt(math.pi/45)*relic.MPL*math.sqrt(gstar)*m*sv
    yeq = lambda x: 45/(4*math.pi**4)*geff/gstar*x**1.5*math.exp(-x)*math.sqrt(math.pi/2)
    rhs = lambda x, y: [-lam*Rfun(x)/x**2*(y[0]**2 - yeq(x)**2)]
    s = solve_ivp(rhs, [3.0, xend], [yeq(3.0)], method='Radau', rtol=1e-8, atol=1e-20)
    Y = float(s.y[0, -1]); return m*Y*relic.S0/relic.RHOC_H2, Y
if __name__ == '__main__':
    one = lambda x: 1.0
    mB = brentq(lambda m: omega(m, one)[0] - 0.1205, 1500, 4000)
    print(f"S3 Born (R=1, xend 3e4): M_th={mB/1e3:.4f} TeV vs R1b 2.531 (rel {mB/2531-1:+.4f}) -> {'PASS' if abs(mB/2531-1) <= 0.005 else 'FAIL'}", flush=True)
    Ms = [2500.0, 2700.0, 2800.0, 2900.0, 3100.0, 3300.0]
    r = run(Ms, XS, [40])
    chk = run([2800.0], [25, 3e3, 3e4], [80])
    lx = np.log(XS); om = {}; om1e4 = {}
    for M in Ms:
        R = np.array([r[(M, x, 40)][0] for x in XS])
        Rf = lambda x, R=R: float(np.interp(math.log(max(x, 3.0)), lx, R))
        om[M] = omega(M, Rf); om1e4[M] = omega(M, Rf, xend=1e4)
        print(f"M={M/1e3:.1f} TeV: R_eff(x=3,25,300,3e3,3e4)={[round(float(np.interp(math.log(q), lx, R)), 3) for q in (3, 25, 300, 3e3, 3e4)]} Oh2={om[M][0]:.4f} (xend 1e4: {om1e4[M][0]:.4f})", flush=True)
    for x in (25, 3e3, 3e4):
        a = np.interp(math.log(x), lx, [r[(2800.0, q, 40)][0] for q in XS]); b = chk[(2800.0, x, 80)][0]
        print(f"conv M=2800 x={x:g}: n40(interp) {a:.4f} vs n80 {b:.4f} rel {abs(a/b-1):.1e}", flush=True)
    lm = np.log(Ms); lo = np.log([om[M][0] for M in Ms])
    Mth = math.exp(brentq(lambda q: np.interp(q, lm, lo) - math.log(0.1205), lm[0], lm[-1])) if lo[0] < math.log(0.1205) < lo[-1] else float('nan')
    print(f"S1 M_th(LO Sommerfeld) = {Mth/1e3:.3f} TeV, band [2.6, 3.1] -> {'PASS' if 2600 <= Mth <= 3100 else 'FAIL'}")
    yr = om[2800.0][1]/omega(2800.0, one)[1]
    print(f"S2 Y_som/Y_Born at 2.8 TeV = {yr:.3f}, band [0.40, 0.60] -> {'PASS' if 0.4 <= yr <= 0.6 else 'FAIL'}")
