"""L0b2: minimal RECFAST (Seager-Sasselov-Scott; equations as transcribed in astro-ph/0602577 Eqs. 1-4, 6-10) for
x_e(z), plus the drag epoch z_d (tau_d = 1). SI units, constants from scipy.constants. Saha for early phases."""
import math, numpy as np
from scipy import constants as K
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.interpolate import interp1d
from scipy.optimize import brentq
eV = K.e; me = K.m_e; kB = K.k; h = K.h; c = K.c
mH = K.m_p + K.m_e                            # hydrogen atom mass (binding neglected), stated
sigT = 8*math.pi/3*(K.e**2/(4*math.pi*K.epsilon_0*me*c**2))**2
aR = 8*math.pi**5*kB**4/(15*c**3*h**3)
lamA = 121.5682e-9; nuH = c/lamA; LamH = 8.22458
lamHe = 60.1404e-9; nuHe = c/lamHe; LamHe = 51.3; dEHe = h*(c/58.4334e-9 - nuHe)
def SahaC(T): return (2*math.pi*me*kB*T/h**2)**1.5
class Recomb:
    def __init__(self, cosmo, ombh2, YHe=0.24, Tcmb=2.7255):
        self.c, self.Y, self.T0 = cosmo, YHe, Tcmb
        rho_c100 = 3*(100e3/(K.parsec*1e6))**2/(8*math.pi*K.G)
        self.nH0 = (1 - YHe)*ombh2*rho_c100/mH; self.fHe = YHe/(4*(1 - YHe))
        self.Rfac = 3*ombh2/(4*__import__('tools.janus_lt.background', fromlist=['x']).omega_gamma_h2(Tcmb))
        self._solve()
    def Hs(self, z): return self.c.H(z)*1e3/(K.parsec*1e6)        # 1/s
    def nH(self, z): return self.nH0*(1 + z)**3
    def _saha_all(self, z):
        T = self.T0*(1 + z); nH = self.nH(z); f = self.fHe
        sH = SahaC(T)*math.exp(-13.605693*eV/(kB*T))/nH
        sHe1 = 4*SahaC(T)*math.exp(-24.587387*eV/(kB*T))/nH
        sHe2 = SahaC(T)*math.exp(-54.417760*eV/(kB*T))/nH
        def resid(xe):  # charge balance with each species in Saha
            xp = sH/(xe + sH); r1 = sHe1/xe; r2 = sHe2/xe
            heII = f*r1/(1 + r1 + r1*r2); heIII = f*r1*r2/(1 + r1 + r1*r2)
            return xp + heII + 2*heIII - xe
        xe = brentq(resid, 1e-12, 1 + 2*f + 1e-9)
        xp = sH/(xe + sH); r1 = sHe1/xe; r2 = sHe2/xe
        return xp, f*r1/(1 + r1 + r1*r2), f*r1*r2/(1 + r1 + r1*r2), xe
    def _rhs(self, z, u, hydrogen_ode):
        xp, xHeII, TM = u; f = self.fHe; nH = self.nH(z); H = self.Hs(z); TR = self.T0*(1 + z)
        if not hydrogen_ode: xp = self._saha_all(z)[0]
        xe = xp + xHeII
        t = TM/1e4; RH = 1e-19*1.14*4.309*t**-0.6166/(1 + 0.6703*t**0.53)
        bH = RH*SahaC(TM)*math.exp(-3.4*eV/(kB*TM))
        KH = lamA**3/(8*math.pi*H)
        CH = (1 + KH*LamH*nH*(1 - xp))/(1 + KH*(LamH + bH)*nH*(1 - xp))
        dxp = CH/(H*(1 + z))*(xe*xp*nH*RH - bH*(1 - xp)*math.exp(-h*nuH/(kB*TM))) if hydrogen_ode else 0.0
        if xHeII < 1e-13 or z < 800:    # He I recombined (x_HeII ~ 0): its term is irrelevant and exp(dE/kT) overflows
            dHe = -xHeII*0.0
        else:
          RHe = 10**-16.744/(math.sqrt(TM/3)*(1 + TM/3)**(1 - 0.711)*(1 + TM/10**5.114)**(1 + 0.711))
          bHe = RHe*SahaC(TM)*math.exp(-3.97*eV/(kB*TM))
          KHe = c**3/(8*math.pi*nuHe**3*H); g = math.exp(dEHe/(kB*TM))
          CHe = (1 + KHe*LamHe*nH*(f - xHeII)*g)/(1 + KHe*(LamHe + bHe)*nH*(f - xHeII)*g)
          dHe = CHe/(H*(1 + z))*(xHeII*xe*nH*RHe - bHe*(f - xHeII)*math.exp(-h*nuHe/(kB*TM)))
        dT = 8*sigT*aR*TR**4/(3*H*(1 + z)*me*c)*xe/(1 + f + xe)*(TM - TR) + 2*TM/(1 + z)
        return [dxp, dHe, dT]
    def _solve(self):
        zs1 = np.linspace(8000, 3500, 200); xe1 = [self._saha_all(z)[3] for z in zs1]
        xp0, he0, _, _ = self._saha_all(3500.0)
        # stage A: He ODE + T_M, hydrogen in Saha until its Saha x_p drops to 0.99
        zsw = brentq(lambda z: self._saha_all(z)[0] - 0.99, 1200, 3500)
        sA = solve_ivp(lambda z, u: self._rhs(z, u, False), [3500, zsw], [xp0, he0, self.T0*3501], method='LSODA',
                       rtol=1e-8, atol=[1e-12, 1e-12, 1e-6], dense_output=True)
        uA = sA.y[:, -1].copy(); uA[0] = self._saha_all(zsw)[0]
        sB = solve_ivp(lambda z, u: self._rhs(z, u, True), [zsw, 0.0], uA, method='LSODA',
                       rtol=1e-8, atol=[1e-12, 1e-12, 1e-6], dense_output=True)
        zA = np.linspace(3500, zsw, 300); xeA = [self._saha_all(z)[0] + sA.sol(z)[1] for z in zA]
        zB = np.linspace(zsw, 0, 6000); xeB = [sB.sol(z)[0] + sB.sol(z)[1] for z in zB]
        Z = np.concatenate([zs1, zA[1:], zB[1:]]); X = np.concatenate([xe1, xeA[1:], xeB[1:]])
        o = np.argsort(Z); self.z, self.xe = Z[o], X[o]; self.xe_of = interp1d(self.z, self.xe, kind='cubic')
    def tau_d(self, zmax):
        zz = np.linspace(0, zmax, 20001)
        g = [self.xe_of(z)*self.nH(z)*sigT*c/(self.Hs(z)*(1 + z)*(self.Rfac/(1 + z))) for z in zz]
        return float(np.trapezoid(g, zz))
    def z_drag(self):
        return brentq(lambda z: self.tau_d(z) - 1.0, 800, 1300, xtol=1e-4)
