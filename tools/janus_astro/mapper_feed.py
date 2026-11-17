"""Hyperion -> Star Mapper feed: Gaia astrometry (ra, dec, distance, pmra, pmdec, radial_velocity) to Galactocentric
phase space, absolute magnitude, and Milky Way orbit parameters (pericentre, apocentre, z_max, eccentricity, energy, L_z)
in Hyperion's validated MWPotential2014 model (galaxy.py, A5a/D1061).
Conventions (fixed, stated): ICRS -> Galactic with the standard north Galactic pole RA_NGP = 192.85948 deg,
Dec_NGP = 27.12825 deg and l_NCP = 122.93192 deg; Galactocentric frame as astropy's (Sun at x ~ -R0; z_sun tilt);
Sun: R0 (in-plane) = 8.0 kpc, z_sun = 20.8 pc, v_sun = (11.1, 232.24, 7.25) km/s (MWPotential2014's v0 = 220 plus the
Schoenrich et al. 2010 solar motion)."""
import math, numpy as np
D2R = math.pi/180
RA_NGP, DEC_NGP, L_NCP = 192.85948*D2R, 27.12825*D2R, 122.93192*D2R
R0_XY, Z_SUN = 8.0, 0.0208                       # kpc
V_SUN = np.array([11.1, 232.24, 7.25])           # km/s, Galactocentric cartesian
K_PM = 4.740470463533348                          # km/s per (mas/yr * kpc)
def _T():
    """Rotation matrix ICRS cartesian -> Galactic cartesian, built from the pole definition."""
    s, c = math.sin, math.cos
    T1 = np.array([[c(L_NCP), s(L_NCP), 0], [s(L_NCP), -c(L_NCP), 0], [0, 0, 1]])
    T2 = np.array([[-s(DEC_NGP), 0, c(DEC_NGP)], [0, -1, 0], [c(DEC_NGP), 0, s(DEC_NGP)]])
    T3 = np.array([[c(RA_NGP), s(RA_NGP), 0], [s(RA_NGP), -c(RA_NGP), 0], [0, 0, 1]])
    return T1 @ T2 @ T3
T_ICRS_GAL = _T()
def icrs_to_galactic(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec)
    v = np.array([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)])
    g = T_ICRS_GAL @ v
    return np.degrees(np.arctan2(g[1], g[0])) % 360, np.degrees(np.arcsin(np.clip(g[2], -1, 1)))
def galactocentric(ra, dec, d_kpc, pmra, pmdec, rv):
    """Arrays in; returns x, y, z (kpc) and vx, vy, vz (km/s) in astropy's Galactocentric convention."""
    ra, dec = np.radians(ra), np.radians(dec)
    cr, sr, cd, sd = np.cos(ra), np.sin(ra), np.cos(dec), np.sin(dec)
    pos = d_kpc*np.array([cd*cr, cd*sr, sd])
    e_r = np.array([cd*cr, cd*sr, sd]); e_a = np.array([-sr, cr, 0*sr]); e_d = np.array([-sd*cr, -sd*sr, cd])
    vel = rv*e_r + K_PM*d_kpc*(pmra*e_a + pmdec*e_d)
    p, v = T_ICRS_GAL @ pos, T_ICRS_GAL @ vel
    dgc = math.hypot(R0_XY, Z_SUN); p[0] = p[0] - dgc
    th = math.asin(Z_SUN/dgc); H = np.array([[math.cos(th), 0, math.sin(th)], [0, 1, 0], [-math.sin(th), 0, math.cos(th)]])
    return H @ p, H @ v + V_SUN[:, None]
def abs_mag_G(G, parallax_mas):
    """M_G = G + 5 log10(parallax / mas) - 10 (no extinction correction; flagged as such)."""
    return G + 5*np.log10(parallax_mas) - 10
def orbit_params(x, y, z, vx, vy, vz, mw=None, t_gyr=5.0, n=20001):
    """One star (kpc, km/s): integrate in MWPotential2014 for t_gyr; returns rperi, rapo (spherical r in kpc), zmax (kpc),
    ecc = (rapo - rperi)/(rapo + rperi), energy (km^2/s^2), Lz (kpc km/s)."""
    from . import galaxy as G
    mw = mw or G.MW(); r0, v0 = 8.0, 220.0
    R = math.hypot(x, y); phi = math.atan2(y, x)
    vR = (x*vx + y*vy)/R; vT = (x*vy - y*vx)/R
    tn = t_gyr/(r0*3.0856775814913673e16/v0/3.15576e16)
    t = np.linspace(0, tn, n)
    s = mw.orbit((R/r0, vR/v0, vT/v0, z/r0, vz/v0, phi), t)
    rs = np.sqrt(s.y[0]**2 + s.y[1]**2 + s.y[2]**2)*r0
    rp, ra = float(rs.min()), float(rs.max())
    E = 0.5*(vx*vx + vy*vy + vz*vz) + mw.phi(R/r0, z/r0)*v0*v0
    return dict(rperi=rp, rapo=ra, zmax=float(np.abs(s.y[2]).max()*r0), ecc=(ra - rp)/(ra + rp), E=E, Lz=R*vT)
