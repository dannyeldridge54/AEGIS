"""Neutron stars with realistic equations of state: Read-Lackey-Owen-Friedman (2009, arXiv:0812.2163) piecewise polytropes
(SLy crust = their Table 2; core = log p1, Gamma1..3 at rho1 = 10^14.7, rho2 = 10^15 g/cm^3), TOV + tidal y-equation
(Hinderer 2008 form), mass-radius curve, M_max, R_1.4, Love number k2 and Lambda. Internally cgs -> geometric (cm)."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar
G, C = 6.67430e-8, 2.99792458e10; MSUN_G = 1.98840987e33
GC2, GC4 = G/C**2, G/C**4
CRUST = [(6.80110e-09, 1.58425, 0.0), (1.06186e-06, 1.28733, 2.44034e+07), (5.32697e+01, 0.62223, 3.78358e+11),
         (3.99874e-08, 1.35692, 2.62780e+12)]           # (K_i cgs, Gamma_i, lower density rho_{i-1}); Read+ Table 2
TABLE3 = {'SLy': (34.384, 3.005, 2.988, 2.851), 'AP4': (34.269, 2.830, 3.445, 3.348)}
class PPEOS:
    def __init__(self, logp1, g1, g2, g3, rho1=10**14.7, rho2=10**15.0):
        K1 = 10**logp1/rho1**g1; K2 = K1*rho1**(g1-g2); K3 = K2*rho2**(g2-g3)
        Kc, gc = CRUST[3][0], CRUST[3][1]
        rho0 = (Kc/K1)**(1/(g1-gc))                    # crust-core joining density
        pieces = [list(p) for p in CRUST] + [[K1, g1, rho0], [K2, g2, rho1], [K3, g3, rho2]]
        # a_i from continuity of energy density (a_1 = 0)
        a = [0.0]
        for i in range(1, len(pieces)):
            Kp, gp, _ = pieces[i-1]; K, g, r = pieces[i]
            a.append(a[-1] + Kp*r**(gp-1)/(gp-1) - K*r**(g-1)/(g-1))
        self.p = pieces; self.a = a
        self.pb = [K*r**g for K, g, r in pieces]           # pressure at each lower boundary
    def _piece(self, P):
        i = 0
        for j in range(len(self.p)):
            if P >= self.pb[j]: i = j
        return i
    def rho_eps(self, P):
        """cgs: rest-mass density rho (g/cm^3) and energy density eps/c^2 (g/cm^3) at pressure P (dyn/cm^2)."""
        i = self._piece(P); K, g, _ = self.p[i]
        rho = (P/K)**(1/g); eps = (1 + self.a[i])*rho + P/(C*C)/(g - 1)
        return rho, eps, g
def tov_tidal(eos, rho_c, rtol=1e-10):
    """Returns (M [Msun], R [km], k2, Lambda, C) for central rest-mass density rho_c (g/cm^3)."""
    i = 0
    for j in range(len(eos.p)):
        if rho_c >= eos.p[j][2]: i = j
    K, g, _ = eos.p[i]; Pc = K*rho_c**g
    Pg = lambda P: P*GC4                               # cm^-2
    def rhs(r, y):
        P, m, yy = y
        if P <= 0: return [0, 0, 0]
        _, eps, gam = eos.rho_eps(P/GC4)
        e = eps*GC2; p = P
        f = 1 - 2*m/r
        dP = -(e + p)*(m + 4*math.pi*r**3*p)/(r*r*f)
        dm = 4*math.pi*r*r*e
        dpde = gam*p/(e + p)
        F = (1 - 4*math.pi*r*r*(e - p))/f
        Q = 4*math.pi*(5*e + 9*p + (e + p)/dpde)/f - 6/(r*r*f) - 4*((m + 4*math.pi*r**3*p)/(r*r*f))**2
        dy = -(yy*yy + yy*F + r*r*Q)/r
        return [dP, dm, dy]
    r0 = 1.0; e0 = eos.rho_eps(Pc)[1]*GC2
    ev = lambda r, y: y[0] - Pg(eos.pb[0])*1e-6; ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, [r0, 5e6], [Pg(Pc), 4/3*math.pi*r0**3*e0, 2.0], method='DOP853', rtol=rtol, atol=[Pg(Pc)*1e-30, 1e-20, 1e-12], events=ev)
    R = float(s.t_events[0][0]) if s.t_events[0].size else float(s.t[-1])
    P_, m, y = (s.y_events[0][0] if s.t_events[0].size else s.y[:, -1])
    Cc = m/R
    k2 = (8*Cc**5/5)*(1-2*Cc)**2*(2 + 2*Cc*(y-1) - y) / (
        2*Cc*(6 - 3*y + 3*Cc*(5*y - 8)) + 4*Cc**3*(13 - 11*y + Cc*(3*y - 2) + 2*Cc*Cc*(1 + y))
        + 3*(1-2*Cc)**2*(2 - y + 2*Cc*(y - 1))*math.log(1 - 2*Cc))
    return m/GC2/MSUN_G, R/1e5, k2, 2/3*k2/Cc**5, Cc, y
def mr_curve(eos, lo=14.3, hi=15.8, n=60):
    return [(lr,) + tov_tidal(eos, 10**lr) for lr in np.linspace(lo, hi, n)]
def max_mass(eos):
    res = minimize_scalar(lambda lr: -tov_tidal(eos, 10**lr)[0], bounds=(14.8, 15.8), method='bounded', options={'xatol': 1e-6})
    return -res.fun, 10**res.x, tov_tidal(eos, 10**res.x)
def at_mass(eos, M, lo=14.4):
    Mmax, rhomax, _ = max_mass(eos)
    lr = brentq(lambda lr: tov_tidal(eos, 10**lr)[0] - M, lo, math.log10(rhomax), xtol=1e-10)
    return tov_tidal(eos, 10**lr)
