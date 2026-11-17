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

# ---- A2c: Newtonian-order amplitude, SNR, horizon and range ----
def amplitude0(f, Mc, D):
    """|h~(f)| for an optimally oriented (face-on, overhead) binary, leading order:
    sqrt(5/24) pi^{-2/3} (G Mc / c^3)^{5/6} f^{-7/6} c / D   (f in Hz, Mc in kg, D in m)."""
    import numpy as np
    return math.sqrt(5/24)*math.pi**(-2/3)*(G*Mc/c**3)**(5/6)*np.asarray(f, float)**(-7/6)*c/D
def snr_opt(Mc, D, psd, f_lo, f_hi, n=20000):
    """Optimal SNR rho^2 = 4 int |h|^2 / S_n df (log-spaced trapezoid); psd: callable S_n(f) [1/Hz]."""
    import numpy as np
    f = np.geomspace(f_lo, f_hi, n); S = np.array([psd(x) for x in f])
    y = amplitude0(f, Mc, D)**2/S
    return math.sqrt(4*np.trapezoid(y*f, np.log(f)))
FINN_CHERNOFF = 2.2648   # horizon / sky- and orientation-averaged range (Finn & Chernoff 1993; LIGO convention)
def horizon(Mc, psd, f_lo, f_hi, rho=8.0):
    return snr_opt(Mc, 1.0, psd, f_lo, f_hi)/rho          # SNR ∝ 1/D: D_h = rho(1 m)/8 in metres

# ---- A2c2: cosmological horizon and range ----
def theta_samples(n=1_000_000, seed=2026):
    """Finn-Chernoff orientation factor Theta in [0, 4] for an L-shaped detector, isotropic sky and orientation:
    F+ = 1/2 (1 + cos^2 th) cos 2ph cos 2ps - cos th sin 2ph sin 2ps,  Fx = 1/2 (1 + cos^2 th) cos 2ph sin 2ps + cos th sin 2ph cos 2ps,
    Theta = 2 sqrt(F+^2 (1 + cos^2 i)^2 + 4 Fx^2 cos^2 i)."""
    import numpy as np
    r = np.random.default_rng(seed)
    ct = r.uniform(-1, 1, n); ph = r.uniform(0, 2*math.pi, n); ps = r.uniform(0, 2*math.pi, n); ci = r.uniform(-1, 1, n)
    a = 0.5*(1 + ct**2)*np.cos(2*ph); b = ct*np.sin(2*ph)
    Fp = a*np.cos(2*ps) - b*np.sin(2*ps); Fx = a*np.sin(2*ps) + b*np.cos(2*ps)
    return np.sort(2*np.sqrt(Fp**2*(1 + ci**2)**2 + 4*Fx**2*ci**2))
def snr_opt_z(m1, m2, z, DL, psd, f_lo, n=4000):
    """Optimal SNR for a source at redshift z, luminosity distance DL (m): redshifted chirp mass, ISCO cut at f_isco/(1+z)."""
    Mcz = chirp_mass(m1, m2)*(1 + z); fhi = c**3/(6**1.5*math.pi*G*(m1 + m2))/(1 + z)
    return snr_opt(Mcz, DL, psd, f_lo, fhi, n) if fhi > f_lo else 0.0

# ---- A2b: aligned-spin TaylorF2 phase (coefficients: Khan et al. 2016, arXiv:1508.07253, Appendix B) ----
def taylorf2_phase_spin(f, m1, m2, chi1, chi2, order=7, spin_order=7):
    """Psi(f) up to a + b f, h ~ exp(-i Psi). Non-spin terms up to `order` (twice PN order); spin terms included only at
    PN orders 2k <= spin_order (1.5PN SO -> 3, 2PN SS -> 4, 2.5PN SO -> 5, 3PN SO -> 6, 3.5PN SO -> 7)."""
    import numpy as np
    M = m1 + m2; eta = m1*m2/M**2; d = (m1 - m2)/M; cs, ca = (chi1 + chi2)/2, (chi1 - chi2)/2; pi = math.pi
    x = pi*G*M*np.asarray(f, float)/c**3; v = x**(1/3)
    s = lambda k: 1.0 if k <= spin_order else 0.0
    p = {0: 1.0 + 0*v, 1: 0*v, 2: (3715/756 + 55*eta/9) + 0*v,
         3: -16*pi + s(3)*(113*d*ca/3 + (113/3 - 76*eta/3)*cs) + 0*v,
         4: (15293365/508032 + 27145*eta/504 + 3085*eta**2/72) + s(4)*((-405/8 + 200*eta)*ca**2 - 405/4*d*ca*cs + (-405/8 + 5*eta/2)*cs**2) + 0*v,
         5: (1 + np.log(x))*(38645*pi/756 - 65*pi*eta/9 + s(5)*(d*(-732985/2268 - 140*eta/9)*ca + (-732985/2268 + 24260*eta/81 + 340*eta**2/9)*cs)),
         6: (11583231236531/4694215680 - 6848*EULER_GAMMA/21 - 640*pi**2/3 + (-15737765635/3048192 + 2255*pi**2/12)*eta
             + 76055*eta**2/1728 - 127825*eta**3/1296 - 6848/63*np.log(64*x) + s(6)*(2270/3*pi*d*ca + (2270*pi/3 - 520*pi*eta)*cs)),
         7: (77096675*pi/254016 + 378515*pi*eta/1512 - 74045*pi*eta**2/756
             + s(7)*(d*(-25150083775/3048192 + 26804935*eta/6048 - 1985*eta**2/48)*ca
                     + (-25150083775/3048192 + 10566655595*eta/762048 - 1042165*eta**2/3024 + 5345*eta**3/36)*cs)) + 0*v}
    tot = sum(p[k]*v**k for k in range(order + 1))
    return 3/(128*eta)*x**(-5/3)*tot
