"""Compact objects. TOV integrator (any barotropic EoS rho(P)); exact Schwarzschild interior for checks;
Kerr equatorial circular orbits: ISCO by the Bardeen-Press-Teukolsky closed form and by minimising E(r);
horizon, photon sphere."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar, brentq
from .const import G, c, M_sun

def schwarzschild_radius(M): return 2*G*M/c**2

def tov(rho_of_P, P_c, r_max=1e6, rtol=1e-11, atol=0.0, p_surf=0.0):
    """rho_of_P: total energy density / c^2 (kg/m^3) as a function of pressure (Pa). Returns (R [m], M [kg])."""
    def rhs(r, y):
        P, m = y; rho = rho_of_P(max(P, 0.0))
        dm = 4*math.pi*r*r*rho
        dP = -G*(rho + P/c**2)*(m + 4*math.pi*r**3*P/c**2)/(r*r*(1 - 2*G*m/(r*c*c)))
        return [dP, dm]
    r0 = 1e-3; rho0 = rho_of_P(P_c)
    ev = lambda r, y: y[0] - p_surf; ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, [r0, r_max], [P_c, 4/3*math.pi*r0**3*rho0], method='DOP853', rtol=rtol, atol=[P_c*1e-16, 1e-30], events=ev)
    return float(s.t_events[0][0]), float(s.y_events[0][0][1])

def schwarzschild_interior_Pc(rho, R):
    """Exact central pressure of a uniform-density star of radius R (Schwarzschild 1916)."""
    M = 4/3*math.pi*R**3*rho; u = math.sqrt(1 - 2*G*M/(R*c*c))
    return rho*c*c*(1 - u)/(3*u - 1), M

def kerr_isco(a, prograde=True):
    """r_isco / (GM/c^2) for spin a = J c/(G M^2), Bardeen-Press-Teukolsky (1972) closed form."""
    z1 = 1 + (1-a*a)**(1/3)*((1+a)**(1/3) + (1-a)**(1/3)); z2 = math.sqrt(3*a*a + z1*z1)
    s = -1 if prograde else 1
    return 3 + z2 + s*math.sqrt((3-z1)*(3+z1+2*z2))

def kerr_circular_E(r, a, prograde=True):
    """Specific energy of an equatorial circular orbit (G = c = M = 1), BPT eq. 2.12."""
    s = 1 if prograde else -1
    num = r**1.5 - 2*r**0.5 + s*a; den = r**0.75*math.sqrt(r**1.5 - 3*r**0.5 + 2*s*a)
    return num/den

def kerr_isco_numeric(a, prograde=True):
    """Second route: the ISCO is the minimum of E(r) over circular orbits."""
    s = 1 if prograde else -1
    # photon orbit (lower edge of circular orbits)
    rph = 2*(1 + math.cos(2/3*math.acos(-s*a)))
    res = minimize_scalar(lambda r: kerr_circular_E(r, a, prograde), bounds=(rph*1.0000001, 20.0), method='bounded', options={'xatol': 1e-12})
    return res.x

def kerr_horizon(a): return 1 + math.sqrt(1 - a*a)
