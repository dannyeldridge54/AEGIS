"""D393 (locked PREREG_D393_AXION_THAW): Twist-2 sector II test. Thawing axion V = L4 (1 + cos(phi/f)) with matter + radiation.
Units M_P = 1, H0 = 1. For each f and initial angle theta_i, L4 is shot so that H(a=1) = 1 (flat). Outputs w0, wa (CPL least-squares
fit of w(a) on a in [1/3, 1]), Omega_DE today, delta theta from recombination to today, and beta = 0.42 deg (c/2pi) dtheta. AI-assisted."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
Om, Or = 0.31, 9.1e-5
def run(f, th, L4, out=False):
    def rhs(N, z):
        p, dp = z; a = math.exp(N); rm, rr = 3*Om*a**-3, 3*Or*a**-4; V = L4*(1+math.cos(p/f)); Vp = -L4/f*math.sin(p/f)
        H2 = (rm + rr + V)/(3 - 0.5*dp*dp)
        # exact: dlnH/dN = -(rho+P)/(2H^2) ; rho+P = H2 dp^2 + rm + 4/3 rr
        dlnH = -(H2*dp*dp + rm + 4*rr/3)/(2*H2)
        return [dp, -(3 + dlnH)*dp - Vp/H2]
    s = solve_ivp(rhs, [math.log(1e-4), 0.0], [th*f, 0.0], rtol=1e-9, atol=1e-12, dense_output=True, method="LSODA")
    p, dp = s.y[:, -1]; V = L4*(1+math.cos(p/f)); H2 = (3*Om + 3*Or + V)/(3 - 0.5*dp*dp)
    if not out: return H2 - 1.0
    a_s = np.linspace(1/3, 1, 200); w = []
    for a in a_s:
        pp, dd = s.sol(math.log(a)); rm, rr = 3*Om*a**-3, 3*Or*a**-4; VV = L4*(1+math.cos(pp/f)); h2 = (rm+rr+VV)/(3-0.5*dd*dd)
        K = 0.5*h2*dd*dd; w.append((K - VV)/(K + VV))
    A = np.vstack([np.ones_like(a_s), 1 - a_s]).T; w0, wa = np.linalg.lstsq(A, np.array(w), rcond=None)[0]
    K = 0.5*H2*dp*dp; ODE = (K + V)/(3*H2); p_rec = s.sol(math.log(1/1090))[0]
    return w0, wa, ODE, (p - p_rec)/f, w[-1]
if __name__ == "__main__":
    print("f/MP theta_i  w0(fit)  wa(fit)  w(a=1)  Omega_DE  dtheta  beta[c=1,10,20] deg")
    for f in (0.1, 0.3, 1.0):
        for th in (0.1, 0.3, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
            lo, hi = 1e-3, 50.0
            try:
                L4 = brentq(lambda L: run(f, th, L), lo, hi, xtol=1e-12)
            except ValueError:
                print(f"{f:4.1f} {th:5.2f}  no flat solution"); continue
            w0, wa, ODE, dth, w1 = run(f, th, L4, True)
            b = [0.42*c/(2*math.pi)*abs(dth) for c in (1, 10, 20)]
            print(f"{f:4.1f} {th:5.2f}  {w0:+.3f}  {wa:+.3f}  {w1:+.3f}  {ODE:.3f}  {dth:+.3f}  {b[0]:.3f} {b[1]:.3f} {b[2]:.3f}", flush=True)
