"""
AEGIS UFE v2 — Torsion-Born Early Dark Energy engine.

Replaces the v1 "UFE" background  H^2 = H0^2[Or(1+z)^4 + Om(1+beta)(1+z)^3 + OL]
with the Barbero–Immirzi torsion field model (Eldridge 2026):

    E^2(a) = [omega_m a^-3 + omega_r a^-4 + omega_L + omega_tau(a)] / h^2

Torsion-field energy, fluid form of the canonical field phi = sqrt(3/2) M_Pl arsinh(1/gamma)
with V = Lambda^4 [1 - cos(phi/F)]^n  (Poulin et al. 2018 fluid approximation):

    omega_tau(a) = 2 omega_tau(a_c) / [ (a/a_c)^{3(1+w_n)} + 1 ],   w_n = (n-1)/(n+1)

normalised so that omega_tau(a_c) / total(a_c) = f.  Exactly flat:  omega_L = h^2 - omega_m - omega_r - omega_tau(1).

The sound horizon r_s(z*) and r_d(z_d) are COMPUTED from the model (v1 used a fixed 147.09 Mpc).
"""
import numpy as np

C_KMS = 299792.458
CH = C_KMS / 100.0                 # c / (100 km/s/Mpc) in Mpc
OMEGA_G = 2.473e-5                 # photons, T0 = 2.7255 K
N_EFF = 3.046
OMEGA_R = OMEGA_G * (1 + 0.2271 * N_EFF)
OMEGA_B_PLANCK = 0.02237

# ---------------------------------------------------------------- recombination fits
def z_star(wb, wm):
    """Hu & Sugiyama (1996) photon-decoupling redshift."""
    g1 = 0.0783 * wb**-0.238 / (1 + 39.5 * wb**0.763)
    g2 = 0.560 / (1 + 21.1 * wb**1.81)
    return 1048 * (1 + 0.00124 * wb**-0.738) * (1 + g1 * wm**g2)

def _z_drag_raw(wb, wm):
    b1 = 0.313 * wm**-0.419 * (1 + 0.607 * wm**0.674)
    b2 = 0.238 * wm**0.223
    return 1291 * wm**0.251 / (1 + 0.659 * wm**0.828) * (1 + b1 * wb**b2)

_ZD_CAL = 1059.94 / _z_drag_raw(0.02237, 0.14237)   # calibrated to Planck 2018 z_d

def z_drag(wb, wm):
    """Eisenstein & Hu (1998) drag redshift, calibrated to Planck z_d = 1059.94."""
    return _ZD_CAL * _z_drag_raw(wb, wm)

# ---------------------------------------------------------------- models
class Model:
    """Base class. Subclasses implement extra(a): additional physical density omega_x(a)."""
    name = "base"
    def __init__(self, h, omega_c, omega_b=OMEGA_B_PLANCK):
        self.h, self.wc, self.wb = h, omega_c, omega_b
        self.wm = omega_c + omega_b
    def extra(self, a):
        return 0.0 * a
    def omega_L(self):
        return self.h**2 - self.wm - OMEGA_R - float(self.extra(np.array([1.0]))[0])
    def E(self, a):
        tot = self.wm / a**3 + OMEGA_R / a**4 + self.omega_L() + self.extra(a)
        return np.sqrt(np.maximum(tot, 1e-30)) / self.h

class LCDM(Model):
    name = "LCDM"

class LegacyBeta(Model):
    """v1 UFE model, with its flatness bug FIXED. beta(z) = beta0 + beta1 z/(1+z)
    multiplying the matter term:  omega_m (1+beta(z)) (1+z)^3."""
    name = "Legacy-beta (v1, flatness fixed)"
    def __init__(self, h, omega_c, beta0=0.0, beta1=0.0, omega_b=OMEGA_B_PLANCK):
        super().__init__(h, omega_c, omega_b)
        self.b0, self.b1 = beta0, beta1
    def extra(self, a):
        z = 1 / a - 1
        return self.wm * (self.b0 + self.b1 * z / (1 + z)) / a**3

class TorsionEDE(Model):
    """Torsion-born early dark energy (Barbero–Immirzi field), fluid approximation."""
    name = "Torsion-born EDE (v2)"
    def __init__(self, h, omega_c, f, log10_zc, n=3, omega_b=OMEGA_B_PLANCK):
        super().__init__(h, omega_c, omega_b)
        self.f, self.zc, self.n = f, 10**log10_zc, n
        self.ac = 1 / (1 + self.zc)
        self.p = 3 * (1 + (n - 1) / (n + 1))          # 3(1+w_n)
        bg_c = self.wm / self.ac**3 + OMEGA_R / self.ac**4  # Lambda negligible at z_c
        self.rho_c = f / (1 - f) * bg_c if f > 0 else 0.0
    def extra(self, a):
        if self.rho_c == 0:
            return 0.0 * a
        return 2 * self.rho_c / ((a / self.ac)**self.p + 1)

# ---------------------------------------------------------------- distances
_NGRID = 20001

def sound_horizon(m, z_end):
    """r_s(z_end) in Mpc, Simpson in ln a from a=1e-10."""
    N = np.linspace(np.log(1e-10), -np.log1p(z_end), _NGRID)
    a = np.exp(N)
    cs = 1 / np.sqrt(3 * (1 + 3 * m.wb / (4 * OMEGA_G) * a))
    y = cs / (a * m.E(a))
    return CH / m.h * _simpson(y, N)

def _simpson(y, x):
    dx = x[1] - x[0]
    return dx / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())

class Distances:
    """Comoving distance table D_C(z) for one model (Mpc), z up to z*+."""
    def __init__(self, m, zmax=1200.0):
        self.m = m
        u = np.linspace(0, np.log1p(zmax), _NGRID)       # u = ln(1+z)
        z = np.expm1(u)
        a = 1 / (1 + z)
        y = (1 + z) / m.E(a)                             # dz/E = (1+z) du / E
        cum = np.concatenate([[0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(u))])
        self.u, self.DC_tab = u, CH / m.h * cum
    def DC(self, z):
        return np.interp(np.log1p(z), self.u, self.DC_tab)
    def DH(self, z):
        return CH / self.m.h / self.m.E(1 / (1 + np.asarray(z, float)))
    def DV(self, z):
        return (z * self.DC(z)**2 * self.DH(z))**(1 / 3)

def derived(m):
    zs, zd = z_star(m.wb, m.wm), z_drag(m.wb, m.wm)
    rs, rd = sound_horizon(m, zs), sound_horizon(m, zd)
    D = Distances(m)
    return dict(zs=zs, zd=zd, rs=rs, rd=rd, DCs=D.DC(zs), theta=rs / D.DC(zs), D=D,
                H0=100 * m.h, Om=m.wm / m.h**2, rdh=rd * m.h)

# ---------------------------------------------------------------- full field solve
from scipy.integrate import solve_ivp

class TorsionField(Model):
    """Torsion-born EDE, FULL Klein-Gordon solve of the Barbero-Immirzi field.
    Params: log10_v0 (potential scale in units 3 M_Pl^2 (100 km/s/Mpc)^2), F (M_Pl), theta_i, n.
    Derived: peak energy fraction f and its redshift z_c (stored after construction)."""
    name = "Torsion-born EDE (v2, full field)"
    N0, N1 = np.log(1e-8), 0.0          # integrate all the way to today (a = 1)
    def __init__(self, h, omega_c, log10_v0, F, theta_i=2.8, n=3, omega_b=OMEGA_B_PLANCK, rtol=1e-8):
        super().__init__(h, omega_c, omega_b)
        v0, wm = 10**log10_v0, self.wm
        wL0 = max(h**2 - wm - OMEGA_R, 0.0)  # late-time Lambda in the background (field energy today is tiny when released early)
        V = lambda p: v0 * (1 - np.cos(p / F))**n
        dV = lambda p: v0 * n * (1 - np.cos(p / F))**(n - 1) * np.sin(p / F) / F
        def rhs(N, y):
            p, q = y; a = np.exp(N); bg = wm / a**3 + OMEGA_R / a**4 + wL0
            E2 = (bg + V(p)) / (1 - q * q / 6)
            dlnE = -1.5 * (wm / a**3 + 4 / 3 * OMEGA_R / a**4) / E2 - q * q / 2
            return [q, -(3 + dlnE) * q - 3 * dV(p) / E2]
        Ns = np.linspace(self.N0, self.N1, 8001)
        s = solve_ivp(rhs, (self.N0, self.N1), [theta_i * F, 0.0], method="DOP853",
                      t_eval=Ns, rtol=rtol, atol=1e-12)
        p, q = s.y; a = np.exp(Ns); bg = wm / a**3 + OMEGA_R / a**4 + wL0
        E2 = (bg + V(p)) / (1 - q * q / 6)
        rho = np.maximum(E2 - bg, 1e-300)
        self._N, self._lr = Ns, np.log(rho)
        self._rho_i = V(theta_i * F)
        m = (Ns > np.log(1e-3)) & (Ns < np.log(1e-2))
        self._slope = np.polyfit(Ns[m], self._lr[m], 1)[0]
        frac = rho / E2; k = int(np.argmax(frac))
        self.f, self.zc = float(frac[k]), float(1 / a[k] - 1)
        self.w_late = float(-1 - self._slope / 3)
    def extra(self, a):
        N = np.log(np.asarray(a, float))
        out = np.exp(np.interp(N, self._N, self._lr))
        out = np.where(N < self.N0, self._rho_i, out)
        return np.where(N > self.N1, np.exp(self._lr[-1] + self._slope * (N - self.N1)), out)
