"""D404 (locked PREREG_D404_BRIDGE4): reionization-vs-recombination birefringence ratio for the single thawing axion. AI-assisted.
ρ_β = β_reio/β_rec = |θ(0) − θ(z_re)| / |θ(0) − θ(1089)|, z_re ∈ {7, 8, 10}; same locked D393 integrator (axion_thaw_d393.run)."""
import math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
import axion_thaw_d393 as AX
def theta_hist(f, th, L4):
    Om, Or = AX.Om, AX.Or
    def rhs(N, z):
        p, dp = z; a = math.exp(N); rm, rr = 3*Om*a**-3, 3*Or*a**-4; V = L4*(1+math.cos(p/f)); Vp = -L4/f*math.sin(p/f)
        H2 = (rm + rr + V)/(3 - 0.5*dp*dp); dlnH = -(H2*dp*dp + rm + 4*rr/3)/(2*H2); return [dp, -(3 + dlnH)*dp - Vp/H2]
    s = solve_ivp(rhs, [math.log(1e-4), 0.0], [th*f, 0.0], rtol=1e-9, atol=1e-12, dense_output=True, method="LSODA")
    return lambda z: s.sol(-math.log(1 + z))[0] / f
print("f   θ_i   w0       ρ_β(z_re=7)  ρ_β(8)    ρ_β(10)   1−ρ_β(8)")
for f in (0.5, 1.0, 2.0):
    for th in (0.3, 0.5, 1.0, 1.5):
        try: L4 = brentq(lambda L: AX.run(f, th, L), 1e-3, 50.0, xtol=1e-12)
        except ValueError: print(f"{f:3.1f} {th:4.1f}  no flat solution"); continue
        w0 = AX.run(f, th, L4, True)[0]; t = theta_hist(f, th, L4); d = abs(t(0) - t(1089))
        r = [abs(t(0) - t(z)) / d for z in (7, 8, 10)]
        print(f"{f:3.1f} {th:4.1f}  {w0:+.4f}  {r[0]:.6f}    {r[1]:.6f}  {r[2]:.6f}  {1-r[1]:.2e}", flush=True)
