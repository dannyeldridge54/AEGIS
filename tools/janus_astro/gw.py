"""Compact-binary gravitational waves at leading (Newtonian, 0PN) order: chirp mass, frequency evolution,
time to coalescence (closed form and by integrating df/dt), cycles, strain amplitude."""
import math
from scipy.integrate import solve_ivp, quad
from .const import G, c, pc

def chirp_mass(m1, m2): return (m1*m2)**0.6/(m1+m2)**0.2

def dfdt(f, Mc):
    """GW frequency evolution: df/dt = (96/5) pi^{8/3} (G Mc/c^3)^{5/3} f^{11/3}."""
    return 96/5*math.pi**(8/3)*(G*Mc/c**3)**(5/3)*f**(11/3)

def time_to_coalescence(f, Mc):
    """Closed form: tau = (5/256) (G Mc/c^3)^{-5/3} (pi f)^{-8/3}."""
    return 5/256*(G*Mc/c**3)**(-5/3)*(math.pi*f)**(-8/3)

def time_to_coalescence_numeric(f, Mc, f_hi=None):
    """Second route: integral of df / (df/dt) from f to f_hi (f_hi -> large; tail added analytically)."""
    f_hi = f_hi or 1e4*f
    val, _ = quad(lambda x: 1/dfdt(x, Mc), f, f_hi, epsabs=0, epsrel=1e-12, limit=200)
    return val + time_to_coalescence(f_hi, Mc)

def n_cycles(f1, f2, Mc):
    """Number of GW cycles between f1 and f2: integral of f / (df/dt) df."""
    return quad(lambda x: x/dfdt(x, Mc), f1, f2, epsrel=1e-12)[0]

def strain_amplitude(f, Mc, D):
    """Sky- and orientation-optimal h0 = 4 (G Mc/c^2)^{5/3} (pi f / c)^{2/3} / D."""
    return 4*(G*Mc/c**2)**(5/3)*(math.pi*f/c)**(2/3)/D
