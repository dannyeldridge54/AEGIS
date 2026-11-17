"""Stellar structure. Lane-Emden polytropes (two routes: series start + DOP853, and an independent RK45 run at
different tolerance), exact n = 0, 1, 5 solutions, polytrope mass/radius scalings, Chandrasekhar mass,
Eddington luminosity, Kelvin-Helmholtz time."""
import math, numpy as np
from scipy.integrate import solve_ivp
from .const import G, c, hbar, m_u, m_p, sigma_T, M_sun, R_sun, L_sun, yr

def lane_emden(n, method='DOP853', rtol=1e-12, atol=1e-14, xi_max=50.0):
    """Returns (xi1, omega_n = -xi1^2 theta'(xi1), sol). Starts at xi0 from the series theta = 1 - xi^2/6 + n xi^4/120."""
    xi0 = 1e-4
    th0 = 1 - xi0**2/6 + n*xi0**4/120; dth0 = -xi0/3 + n*xi0**3/30
    def rhs(x, y):
        th = y[0]; thn = abs(th)**n * (1 if th >= 0 else -1) if n != int(n) else th**n
        return [y[1], -thn - 2*y[1]/x]
    ev = lambda x, y: y[0]; ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, [xi0, xi_max], [th0, dth0], method=method, rtol=rtol, atol=atol, events=ev, dense_output=True)
    if not s.t_events[0].size: return math.inf, None, s
    x1 = float(s.t_events[0][0]); d1 = float(s.y_events[0][0][1])
    return x1, -x1*x1*d1, s

def lane_emden_exact(n, xi):
    xi = np.asarray(xi, float)
    if n == 0: return 1 - xi**2/6
    if n == 1: return np.where(xi > 0, np.sin(xi)/np.where(xi > 0, xi, 1), 1.0)
    if n == 5: return (1 + xi**2/3)**-0.5
    raise ValueError('exact solutions only for n = 0, 1, 5')

def chandrasekhar_mass(mu_e=2.0, omega3=None):
    """M_Ch = (sqrt(3 pi)/2) omega_3 (hbar c / G)^{3/2} / (mu_e m_u)^2, in kg (ultra-relativistic n = 3 polytrope)."""
    if omega3 is None: omega3 = lane_emden(3)[1]
    return math.sqrt(3*math.pi)/2 * omega3 * (hbar*c/G)**1.5 / (mu_e*m_u)**2

def eddington_luminosity(M, X=0.7):
    """Electron-scattering Eddington limit L = 4 pi G M c / kappa, kappa = sigma_T (1+X) / (2 m_p)."""
    kappa = sigma_T*(1+X)/(2*m_p)
    return 4*math.pi*G*M*c/kappa

def kelvin_helmholtz_time(M=M_sun, R=R_sun, L=L_sun):
    return G*M*M/(R*L)

def polytrope_mass_radius(n, K, rho_c):
    """Newtonian polytrope P = K rho^{1+1/n}: returns (M, R) in SI from Lane-Emden xi1, omega_n."""
    x1, w, _ = lane_emden(n)
    a = math.sqrt((n+1)*K*rho_c**(1/n - 1)/(4*math.pi*G))
    return 4*math.pi*a**3*rho_c*w, a*x1
