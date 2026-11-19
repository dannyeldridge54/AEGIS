"""JANUS tick 13: rho offset model (A y^2 + B + D/y plateau, kappa=1 tilt), slow roll inverted at A1 (see PREREG)."""
import json, math, sys
import numpy as np
from scipy.optimize import fsolve
from scipy.special import zeta
A, B0, D0 = 2*zeta(4), 1-5.783341757348703, math.pi*zeta(3)
def epstein(y, M=300):
    t = complex(-0.5, y); m = np.arange(-M, M+1)[:, None]; n = np.arange(-M, M+1)[None, :]
    z = np.abs(m+n*t)**2; z[M, M] = np.inf; return float(np.sum(y**2/z**2))
chk = {y: epstein(y) - (A*y*y + D0/y) for y in (2.0, 3.0, 4.0)}
def V(phi, C, B, D):
    y = math.exp(math.sqrt(2)*phi); E1 = A*y*y + B + D/y; return (1 - 1/E1)*(1 + C*(E1-1))
def sr(phi, C, B, D, h=1e-3):
    v = [V(phi+k*h, C, B, D) for k in (-2, -1, 0, 1, 2)]
    d1 = (v[0]-8*v[1]+8*v[3]-v[4])/(12*h); d2 = (-v[0]+16*v[1]-30*v[2]+16*v[3]-v[4])/(12*h*h)
    d3 = (-v[0]+2*v[1]-2*v[3]+v[4])/(2*h**3); V0 = v[2]
    e = 0.5*(d1/V0)**2; eta = d2/V0; xi2 = d1*d3/V0**2
    return 1-6*e+2*eta, 16*e, 16*e*eta-24*e*e-2*xi2
NS, R, AEX = 0.974393, 4.82095e-4, -9.9814e-4
def solve(B, D):
    f = lambda p: [sr(p[1], p[0]*1e-6, B, D)[0]-NS, (sr(p[1], p[0]*1e-6, B, D)[1]-R)*1e3]
    C6, phi = fsolve(f, (1.2, math.log(14.4)/math.sqrt(2)), xtol=1e-13)
    ns, r, a = sr(phi, C6*1e-6, B, D); return dict(C=C6*1e-6, y_star=math.exp(math.sqrt(2)*phi), ns=ns, r=r, alpha=a, err=a/AEX-1)
full = solve(B0, D0); pure = solve(0.0, 0.0); b_only = solve(B0, 0.0)
out = dict(A=A, B=B0, D=D0, epstein_residual_check=chk, D_check_pass=abs(chk[3.0]) < 1e-3,
           full=full, B_only=b_only, pure_plateau=pure, LO_relation=-9.6419e-4, LO_err=-9.6419e-4/AEX-1)
out['verdict'] = 'PASS' if abs(full['err']) < 0.01 else 'FAIL'
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
