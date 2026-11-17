"""L0: background expansion and distances from first principles (scipy.constants; no CAMB inside).
Flat FLRW: photons (from T_CMB), massless neutrinos (N_eff, (7/8)(4/11)^{4/3}), baryons + CDM, dark energy
(Λ, w0–wa CPL, or any F(a) multiplying ρ_DE, or a callable w(a)). Distances in Mpc."""
import math, numpy as np
from scipy import constants as K
from scipy.integrate import quad
C_KMS = K.c/1e3
def omega_gamma_h2(Tcmb=2.7255):
    rho = (math.pi**2/15)*(K.k*Tcmb)**4/((K.hbar*K.c)**3)/K.c**2        # kg/m^3
    rho_c100 = 3*(100e3/(K.parsec*1e6))**2/(8*math.pi*K.G)               # critical density for h = 1
    return rho/rho_c100
_FNU = None
def f_nu(y):
    """L0c: Komatsu et al. 2011 (1001.4538) Eq. 25, f(y) = 120/(7 pi^4) int x^2 sqrt(x^2+y^2)/(e^x+1) dx, tabulated once by
    quadrature on a log grid and splined in log-log (spline error << 1e-8)."""
    global _FNU
    if _FNU is None:
        from scipy.interpolate import CubicSpline
        ys = np.logspace(-6, 6, 2401)
        fs = [120/(7*math.pi**4)*quad(lambda x, yy=yy: x*x*math.sqrt(x*x + yy*yy)/(math.exp(x) + 1), 0, 200 + 0*yy,
              limit=400, epsabs=0, epsrel=1e-12)[0] for yy in ys]
        _FNU = CubicSpline(np.log(ys), np.log(fs))
    if y < 1e-6: return 1.0
    return float(math.exp(_FNU(math.log(y)))) if y < 1e6 else 180*1.2020569031595942*y/(7*math.pi**4)
class Cosmo:
    def __init__(self, H0, ombh2, omch2, w0=-1.0, wa=0.0, Neff=3.044, Tcmb=2.7255, Fde=None, mnu=0.0):
        """mnu (eV): one massive eigenstate carrying Neff/3 of the neutrino density (CAMB num_massive_neutrinos=1 reading, L0c)."""
        self.H0, self.h = H0, H0/100; h2 = self.h**2
        self.og = omega_gamma_h2(Tcmb)/h2; self.onu = self.og*Neff*(7/8)*(4/11)**(4/3)
        self.mnu = mnu; self.ynu = mnu/(K.k*(4/11)**(1/3)*Tcmb/K.e) if mnu > 0 else 0.0
        self.om = (ombh2 + omch2)/h2; self.ode = 1 - self.om - self.og - self.nu(1.0)
        self.w0, self.wa, self.Fde = w0, wa, Fde
    def nu(self, a):
        """neutrino density in units of rho_crit today, times a^4 (radiation-like scaling removed)."""
        if self.mnu <= 0: return self.onu
        return self.onu*(2/3 + f_nu(self.ynu*a)/3)
    def de(self, a):
        f = a**(-3*(1 + self.w0 + self.wa))*math.exp(-3*self.wa*(1 - a))
        return f*(self.Fde(a) if self.Fde else 1.0)
    def E(self, z):
        a = 1/(1 + z)
        return math.sqrt(self.og*a**-4 + self.nu(a)*a**-4 + self.om*a**-3 + self.ode*self.de(a))
    def H(self, z): return self.H0*self.E(z)
    def DM(self, z): return C_KMS/self.H0*quad(lambda x: 1/self.E(x), 0, z, limit=500, epsrel=1e-11)[0]
    def DH(self, z): return C_KMS/self.H(z)
