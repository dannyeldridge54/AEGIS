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

# ---- A2: TaylorF2 frequency-domain phase, non-spinning point particles, up to 3.5PN ----
EULER_GAMMA = 0.5772156649015329
def taylorf2_phase(f, m1, m2, order=7):
    """Psi(f) for h(f) ~ A f^{-7/6} exp(-i Psi) up to an arbitrary a + b f (t_c, phi_c), masses in kg, f in Hz (array).
    Psi = 3/(128 eta v^5) sum_k phi_k v^k, v = (pi G M f / c^3)^{1/3} (Buonanno-Iyer-Ochsner-Pan-Sathyaprakash 2009, Table I).
    order = twice the PN order (0..7)."""
    import numpy as np
    M = m1 + m2; eta = m1*m2/M**2; pi = math.pi
    v = (pi*G*M*np.asarray(f, float)/c**3)**(1/3)
    phi = [1.0, 0.0, 3715/756 + 55*eta/9, -16*pi,
           15293365/508032 + 27145*eta/504 + 3085*eta**2/72,
           None,
           None,
           pi*(77096675/254016 + 378515*eta/1512 - 74045*eta**2/756)]
    s = np.ones_like(v)
    for k in range(1, order+1):
        if k == 5:
            s = s + pi*(38645/756 - 65*eta/9)*(1 + 3*np.log(v))*v**5
        elif k == 6:
            p6 = (11583231236531/4694215680 - 640*pi**2/3 - 6848*EULER_GAMMA/21
                  + (-15737765635/3048192 + 2255*pi**2/12)*eta + 76055*eta**2/1728 - 127825*eta**3/1296)
            s = s + (p6 - 6848/21*np.log(4*v))*v**6
        else:
            s = s + phi[k]*v**k
    return 3/(128*eta*v**5)*s
