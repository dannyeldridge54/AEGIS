"""Binaries and orbits: Kepler's third law, escape speed, Hill radius, Roche lobe radius by Eggleton (1983)'s
fit and by direct numerical volume of the critical Roche equipotential (second route)."""
import math, numpy as np
from scipy.optimize import brentq
from .const import G

def kepler_period(a, M): return 2*math.pi*math.sqrt(a**3/(G*M))
def escape_speed(M, r): return math.sqrt(2*G*M/r)
def hill_radius(a, m, M): return a*(m/(3*M))**(1/3)

def roche_eggleton(q):
    """R_L / a for the star of mass m1 with q = m1/m2 (Eggleton 1983, ApJ 268, 368)."""
    return 0.49*q**(2/3)/(0.6*q**(2/3) + math.log(1 + q**(1/3)))

def _phi(x, y, z, q):
    """Dimensionless Roche potential, separation 1, star 1 (mass fraction mu1) at origin, star 2 at x = 1,
    corotating frame, units G(m1+m2) = 1."""
    mu2 = 1/(1+q); mu1 = 1 - mu2
    r1 = math.sqrt(x*x+y*y+z*z); r2 = math.sqrt((x-1)**2+y*y+z*z)
    return -mu1/r1 - mu2/r2 - 0.5*((x-mu2)**2 + y*y)

def roche_volume_radius(q, n_th=96, n_ph=192):
    """Volume-equivalent radius of star 1's Roche lobe (q = m1/m2), by ray-casting to the L1 equipotential."""
    mu2 = 1/(1+q)
    dphix = lambda x: (_phi(x+1e-7, 0, 0, q) - _phi(x-1e-7, 0, 0, q))/2e-7
    xL1 = brentq(dphix, 1e-6, 1-1e-6, xtol=1e-14)
    phiL1 = _phi(xL1, 0, 0, q)
    th, wt = np.polynomial.legendre.leggauss(n_th)        # in cos(theta)
    vol = 0.0
    for ct, w in zip(th, wt):
        st = math.sqrt(1-ct*ct)
        for k in range(n_ph):
            ph = 2*math.pi*(k+0.5)/n_ph; dx, dy, dz = st*math.cos(ph), st*math.sin(ph), ct
            f = lambda s: _phi(s*dx, s*dy, s*dz, q) - phiL1
            # lobe boundary: first crossing outward; along the L1 ray it is xL1
            s_hi = xL1 if (dx > 0.999999) else None
            if s_hi is None:
                s = 1e-6; step = 0.002
                while f(s) < 0 and s < 2: s += step
                s_hi = brentq(f, s-step, s, xtol=1e-13) if s < 2 else 2
            vol += w*(2*math.pi/n_ph)*s_hi**3/3
    return (3*vol/(4*math.pi))**(1/3)
