"""SI constants: CODATA 2018 via scipy.constants; IAU 2015 nominal solar values; Julian year."""
from scipy import constants as C
G, c, hbar, h, k_B, sigma_SB = C.G, C.c, C.hbar, C.h, C.k, C.Stefan_Boltzmann
m_p, m_e, m_u, sigma_T = C.m_p, C.m_e, C.atomic_mass, C.physical_constants['Thomson cross section'][0]
GM_sun = 1.3271244e20                    # IAU 2015 B3 nominal (m^3 s^-2)
M_sun = GM_sun / G
R_sun, L_sun = 6.957e8, 3.828e26        # IAU 2015 B3 nominal
pc = 3.0856775814913673e16; kpc, Mpc = 1e3*pc, 1e6*pc
yr = 365.25*86400.0
