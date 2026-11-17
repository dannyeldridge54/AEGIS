"""L9c (locked PREREG_L9c_sigma8_md): growth for the amplitude without radiation."""
import sys, math, numpy as np, camb; sys.path.insert(0, '.')
from scipy.integrate import solve_ivp, quad
from tools.janus_lt.background import Cosmo
from tools.janus_lt.transfer import T_nowiggle
def D0(c, a0=1e-3):
    Om0 = c.om; E = lambda a: math.sqrt(Om0*a**-3 + 1 - Om0)
    def dlnE(x, h=1e-5): return (math.log(E(math.exp(x+h))) - math.log(E(math.exp(x-h))))/(2*h)
    rhs = lambda x, u: [u[1], -(2 + dlnE(x))*u[1] + 1.5*Om0/(math.exp(3*x)*E(math.exp(x))**2)*u[0]]
    return solve_ivp(rhs, [math.log(a0), 0.0], [a0, a0], rtol=1e-10, atol=1e-14).y[0, -1]
def sigma8(h, ob, oc, As=2.1e-9, ns=0.9649):
    c = Cosmo(100*h, ob, oc); Om = c.om; H0 = 100*h/299792.458  # 1/Mpc
    d0 = D0(c); R = 8/h
    def integrand(lnk):
        k = math.exp(lnk); T = float(T_nowiggle(k/h, h, ob, oc))
        PR = 2*math.pi**2*As/k**3*(k/0.05)**(ns - 1); P = 4/25*k**4/(Om**2*H0**4)*T*T*d0*d0*PR
        x = k*R; W = 3*(math.sin(x) - x*math.cos(x))/x**3
        return k**3*P/(2*math.pi**2)*W*W
    return math.sqrt(quad(integrand, math.log(1e-5), math.log(50), limit=400, epsrel=1e-8)[0]), d0, Om
def s8camb(h, ob, oc):
    p = camb.CAMBparams(); p.set_cosmology(H0=100*h, ombh2=ob, omch2=oc, mnu=0.0, num_massive_neutrinos=0, nnu=3.044, TCMB=2.7255, omk=0)
    p.InitPower.set_params(As=2.1e-9, ns=0.9649); p.set_matter_power(redshifts=[0.0], kmax=10.0); return float(camb.get_results(p).get_sigma8_0())
L = []; rs = []
for h, ob, oc in ((0.6736, 0.02237, 0.1200), (0.70, 0.0224, 0.110), (0.64, 0.0220, 0.130)):
    s, d0, Om = sigma8(h, ob, oc); sc = s8camb(h, ob, oc); rs.append(s/sc)
    L.append(f"h={h} wb={ob} wc={oc}: Om={Om:.4f} D0={d0:.4f} sigma8 Janus-LT {s:.4f} vs CAMB {sc:.4f} -> ratio {s/sc:.4f}"); print(L[-1], flush=True)
ok = all(abs(r - 1) <= 0.03 for r in rs)
L.append(f"ratio spread {max(rs)-min(rs):.4f}; " + ('own sigma8 VALIDATED' if ok else 'NOT VALIDATED'))
open('field_tests/results/janus_lt_l9c_s8.txt', 'w').write('\n'.join(L)+'\n'); print(L[-1])
