"""Milky Way potential and orbits: our own implementation of the three MWPotential2014 components (Bovy 2015, ApJS 216, 29)
with parameters read from galpy (the referee) in natural units (r0 = 8 kpc, v0 = 220 km/s, G = 1):
  bulge   rho = amp r^-alpha exp(-(r/rc)^2)           M(r) = 2 pi amp rc^(3-alpha) gamma_lower((3-alpha)/2, (r/rc)^2)
  disk    Phi = -amp / sqrt(R^2 + (a + sqrt(z^2 + b^2))^2)   (Miyamoto-Nagai 1975)
  halo    Phi = -amp ln(1 + r/a) / r                    (NFW, galpy amplitude convention)
Forces analytic; orbits by DOP853; circular speed, escape speed, local dark-matter density."""
import math, numpy as np
from scipy.special import gamma, gammainc
from scipy.integrate import solve_ivp, quad
def params():
    from galpy.potential import MWPotential2014 as P
    b, d, h = P
    return dict(bamp=float(b._amp), alpha=b.alpha, rc=b.rc, damp=float(d._amp), a=d._a, b=d._b, hamp=float(h._amp), ha=h.a)
class MW:
    def __init__(self, p=None): self.p = p or params()
    def _bulge_M(self, r):
        p = self.p; s = (3 - p['alpha'])/2
        return 2*math.pi*p['bamp']*p['rc']**(3 - p['alpha'])*gamma(s)*gammainc(s, (r/p['rc'])**2)
    def force(self, R, z):
        p = self.p; r = math.hypot(R, z)
        fb = -self._bulge_M(r)/r**2
        fh = -p['hamp']*(math.log(1 + r/p['ha'])/r**2 - 1/(r*(p['ha'] + r)))
        FR = (fb + fh)*R/r; Fz = (fb + fh)*z/r
        sq = math.sqrt(z*z + p['b']**2); D = (R*R + (p['a'] + sq)**2)**1.5
        FR += -p['damp']*R/D; Fz += -p['damp']*z*(p['a'] + sq)/(sq*D)
        return FR, Fz
    def vcirc(self, R): return math.sqrt(-R*self.force(R, 0.0)[0])
    def phi(self, R, z, rmax=1e4):
        """Potential with Phi(inf) = 0, by radial integration of the spherical parts + analytic disk."""
        p = self.p; r = math.hypot(R, z)
        pb = -quad(lambda s: self._bulge_M(s)/s**2, r, rmax, limit=200)[0] - self._bulge_M(rmax)/rmax
        ph = -p['hamp']*math.log(1 + r/p['ha'])/r
        pd = -p['damp']/math.sqrt(R*R + (p['a'] + math.sqrt(z*z + p['b']**2))**2)
        return pb + ph + pd
    def rho_halo(self, r):
        p = self.p; x = r/p['ha']; return p['hamp']/(4*math.pi*p['ha']**3)/(x*(1 + x)**2)
    def orbit(self, w0, t, rtol=1e-12):
        """w0 = (R, vR, vT, z, vz, phi) natural units; returns solution in cylindrical coords via Cartesian integration."""
        R, vR, vT, z, vz, ph = w0
        x, y = R*math.cos(ph), R*math.sin(ph); vx = vR*math.cos(ph) - vT*math.sin(ph); vy = vR*math.sin(ph) + vT*math.cos(ph)
        def rhs(_, s):
            X, Y, Z, VX, VY, VZ = s; RR = math.hypot(X, Y); FR, Fz = self.force(RR, Z)
            return [VX, VY, VZ, FR*X/RR, FR*Y/RR, Fz]
        return solve_ivp(rhs, [t[0], t[-1]], [x, y, z, vx, vy, vz], t_eval=t, method='DOP853', rtol=rtol, atol=1e-13)
NAT = dict(r0_kpc=8.0, v0_kms=220.0)
def natural_to_rho_GeVcm3(rho_nat):
    G = 6.67430e-11; kpc = 3.0856775814913673e19
    rho_SI = rho_nat*(220e3)**2/(G*(8*kpc)**2)
    return rho_SI/1.78266192e-21          # GeV/c^2 per cm^3 in kg/m^3

# ---- A6b: vectorised circular speed (same formulas as MW.force at z = 0) ----
def vcirc_array(mw, R):
    p = mw.p; R = np.asarray(R, float); s = (3 - p['alpha'])/2
    Mb = 2*math.pi*p['bamp']*p['rc']**(3 - p['alpha'])*gamma(s)*gammainc(s, (R/p['rc'])**2)
    fb = -Mb/R**2
    fh = -p['hamp']*(np.log(1 + R/p['ha'])/R**2 - 1/(R*(p['ha'] + R)))
    fd = -p['damp']*R/(R*R + (p['a'] + p['b'])**2)**1.5
    return np.sqrt(-R*(fb + fh + fd))

def force_array(mw, R, z):
    """Vectorised (F_R, F_z) — same formulas as MW.force."""
    p = mw.p; r = np.sqrt(R*R + z*z); s = (3 - p['alpha'])/2
    Mb = 2*math.pi*p['bamp']*p['rc']**(3 - p['alpha'])*gamma(s)*gammainc(s, (r/p['rc'])**2)
    fs = -Mb/r**2 - p['hamp']*(np.log(1 + r/p['ha'])/r**2 - 1/(r*(p['ha'] + r)))
    sq = np.sqrt(z*z + p['b']**2); D = (R*R + (p['a'] + sq)**2)**1.5
    return fs*R/r - p['damp']*R/D, fs*z/r - p['damp']*z*(p['a'] + sq)/(sq*D)
