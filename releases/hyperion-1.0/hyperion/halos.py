"""Dark-matter halo profiles: NFW, Einasto, Burkert. Enclosed mass in closed form and by direct quadrature
(two routes), circular velocity, M200/R200 definitions (Delta x rho_crit)."""
import math, numpy as np
from scipy.integrate import quad
from scipy.special import gammainc, gamma
from .const import G

def nfw_menc(r, rho_s, r_s):
    x = r/r_s; return 4*math.pi*rho_s*r_s**3*(math.log(1+x) - x/(1+x))
def nfw_rho(r, rho_s, r_s):
    x = r/r_s; return rho_s/(x*(1+x)**2)
def nfw_from_Mdelta(M, c, rho_ref, Delta=200.0):
    """rho_ref: reference density (e.g. rho_crit). Returns (rho_s, r_s, R_Delta)."""
    R = (3*M/(4*math.pi*Delta*rho_ref))**(1/3); r_s = R/c
    rho_s = M/(4*math.pi*r_s**3*(math.log(1+c) - c/(1+c)))
    return rho_s, r_s, R

def einasto_rho(r, rho_s, r_s, alpha):
    return rho_s*math.exp(-2/alpha*((r/r_s)**alpha - 1))
def einasto_menc(r, rho_s, r_s, alpha):
    """Closed form via the lower incomplete gamma function (rho_s at r_s = r_{-2})."""
    s = 2/alpha*(r/r_s)**alpha
    return 4*math.pi*rho_s*r_s**3*math.exp(2/alpha)/alpha*(alpha/2)**(3/alpha)*gamma(3/alpha)*gammainc(3/alpha, s)

def burkert_rho(r, rho0, r0):
    x = r/r0; return rho0/((1+x)*(1+x*x))
def burkert_menc(r, rho0, r0):
    x = r/r0; return math.pi*rho0*r0**3*(2*math.log(1+x) + math.log(1+x*x) - 2*math.atan(x))

def menc_numeric(rho, r, *p):
    return quad(lambda s: 4*math.pi*s*s*rho(s, *p), 0, r, epsrel=1e-12, limit=200)[0]

def v_circ(menc, r): return math.sqrt(G*menc/r)
