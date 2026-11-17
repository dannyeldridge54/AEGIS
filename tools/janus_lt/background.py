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
class Cosmo:
    def __init__(self, H0, ombh2, omch2, w0=-1.0, wa=0.0, Neff=3.044, Tcmb=2.7255, Fde=None):
        self.H0, self.h = H0, H0/100; h2 = self.h**2
        self.og = omega_gamma_h2(Tcmb)/h2; self.onu = self.og*Neff*(7/8)*(4/11)**(4/3)
        self.om = (ombh2 + omch2)/h2; self.ode = 1 - self.om - self.og - self.onu
        self.w0, self.wa, self.Fde = w0, wa, Fde
    def de(self, a):
        f = a**(-3*(1 + self.w0 + self.wa))*math.exp(-3*self.wa*(1 - a))
        return f*(self.Fde(a) if self.Fde else 1.0)
    def E(self, z):
        a = 1/(1 + z)
        return math.sqrt((self.og + self.onu)*a**-4 + self.om*a**-3 + self.ode*self.de(a))
    def H(self, z): return self.H0*self.E(z)
    def DM(self, z): return C_KMS/self.H0*quad(lambda x: 1/self.E(x), 0, z, limit=500, epsrel=1e-11)[0]
    def DH(self, z): return C_KMS/self.H(z)
