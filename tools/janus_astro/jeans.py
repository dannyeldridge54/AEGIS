"""Spherical Jeans equation, constant anisotropy beta (Binney & Tremaine 2008 §4.8):
sigma_r^2(r) = [nu(r) r^{2 beta}]^{-1} * int_r^inf nu(r') r'^{2 beta} G M(r')/r'^2 dr'."""
import math
from scipy.integrate import quad
def sigma_r(r, M_of_r, nu, beta=0.0, G=1.0):
    f = lambda x: nu(x)*x**(2*beta)*G*M_of_r(x)/(x*x)
    I = quad(f, r, 10*r, epsabs=0, epsrel=1e-12, limit=400)[0] + quad(f, 10*r, math.inf, epsabs=0, epsrel=1e-12, limit=400)[0]
    return math.sqrt(I/(nu(r)*r**(2*beta)))
# analytic enclosed masses (galpy amp conventions, G = 1)
def M_nfw(amp=1.0, a=1.0): return lambda r: amp*(math.log1p(r/a) - (r/a)/(1 + r/a))
def M_hernquist(amp=1.0, a=1.0): return lambda r: 0.5*amp*(r/a)**2/(1 + r/a)**2
def nu_nfw(a=1.0): return lambda r: 1/((r/a)*(1 + r/a)**2)
def nu_hernquist(a=1.0): return lambda r: 1/((r/a)*(1 + r/a)**3)
