"""Halo mass function with massive neutrinos. Linear P(k) from CAMB (referee code); sigma(R) by direct integration;
Tinker et al. (2008) multiplicity f(sigma) taken from colossus (modelTinker08, Delta = 200 x mean) so no coefficient is retyped.
Massive neutrinos: cold-dark-matter + baryon prescription (P_cb and rho_cb in the mass function; Costanzi et al. 2013 convention),
total-matter Omega_m held fixed (omega_cdm lowered by omega_nu = sum m_nu / 93.14 eV)."""
import math, numpy as np
from scipy.integrate import simpson
H0, OMBH2, OMCH2_0, NS, AS = 67.66, 0.02242, 0.11933, 0.9665, 2.105e-9      # Planck 2018 (TT,TE,EE+lowE+lensing) best fit
RHO_CRIT_H2 = 2.77536627e11                                                 # Msun h^2 / Mpc^3
def camb_linear(mnu=0.0, z=0.0, kmax=50.0):
    import camb
    onu = mnu/93.14
    p = camb.CAMBparams()
    p.set_cosmology(H0=H0, ombh2=OMBH2, omch2=OMCH2_0 - onu, mnu=mnu, num_massive_neutrinos=1 if mnu > 0 else 0, nnu=3.046, omk=0, tau=0.0561)
    p.InitPower.set_params(As=AS, ns=NS); p.set_matter_power(redshifts=[z], kmax=kmax); p.NonLinear = camb.model.NonLinear_none
    r = camb.get_results(p)
    k, _, Pm = r.get_matter_power_spectrum(minkh=1e-4, maxkh=kmax, npoints=2000, var1='delta_tot', var2='delta_tot')
    _, _, Pcb = r.get_matter_power_spectrum(minkh=1e-4, maxkh=kmax, npoints=2000, var1='delta_nonu', var2='delta_nonu')
    h = H0/100; Om = (OMBH2 + OMCH2_0 + 0*onu)/h**2 + (0 if mnu == 0 else 0)
    Om_tot = (OMBH2 + OMCH2_0)/h**2                 # held fixed (cdm lowered by onu, nu added)
    Ocb = (OMBH2 + OMCH2_0 - onu)/h**2
    return dict(k=k, Pm=Pm[0], Pcb=Pcb[0], sigma8=float(r.get_sigma8()[0]), Om=Om_tot, Ocb=Ocb, h=h)
def sigma_R(k, P, R):
    x = k*R; W = 3*(np.sin(x) - x*np.cos(x))/x**3
    return math.sqrt(simpson(P*W*W*k**3/(2*math.pi**2), x=np.log(k)))
def dndlnM(M, k, P, rho):
    """M in Msun/h, rho in Msun h^2/Mpc^3 (comoving), Tinker08 Delta = 200m at z = 0."""
    from colossus.lss import mass_function as mf
    R = (3*M/(4*math.pi*rho))**(1/3); s = sigma_R(k, P, R)
    e = 1e-3; s1 = sigma_R(k, P, R*(1+e)**(1/3)); s0 = sigma_R(k, P, R*(1-e)**(1/3))
    dlns_dlnM = (math.log(s1) - math.log(s0))/(math.log(1+e) - math.log(1-e))
    f = float(mf.modelTinker08(s, 0.0, '200m'))   # A7d D1
    return f*rho/M*abs(dlns_dlnM), s
def n_above(M, k, P, rho, Mmax=1e17, n=200):
    lM = np.linspace(math.log(M), math.log(Mmax), n)
    v = np.array([dndlnM(math.exp(x), k, P, rho)[0] for x in lM])
    return simpson(v, x=lM)

# ---- A6b: cached sigma(M) spline, vectorised dn/dlnM ----
class SigmaTable:
    def __init__(self, k, P, rho, lMmin=6.0, lMmax=17.0, n=400):
        from scipy.interpolate import CubicSpline
        self.rho = rho; lM = np.linspace(lMmin, lMmax, n)
        R = (3*10**lM/(4*math.pi*rho))**(1/3)
        x = np.outer(R, k); W = 3*(np.sin(x) - x*np.cos(x))/x**3
        s2 = simpson((P*k**3/(2*math.pi**2))[None, :]*W*W, x=np.log(k), axis=1)
        self.spl = CubicSpline(lM, 0.5*np.log(s2))
    def sigma(self, M): return np.exp(self.spl(np.log10(M)))
    def dlnsigma_dlnM(self, M): return self.spl(np.log10(M), 1)/math.log(10)
def dndlnM_array(M, table, z=0.0, model='tinker08', D=1.0):
    from colossus.lss import mass_function as mf
    M = np.asarray(M, float); s = table.sigma(M)*D
    f = {'tinker08': lambda: mf.modelTinker08(s, z, '200m')}[model]()
    return f*table.rho/M*np.abs(table.dlnsigma_dlnM(M))
