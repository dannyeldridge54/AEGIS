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
def galactocentric(ra, dec, d_kpc, pmra, pmdec, rv, r0_xy=None, v_sun=None):
    """Arrays in; returns x, y, z (kpc) and vx, vy, vz (km/s) in astropy's Galactocentric convention.
    r0_xy / v_sun default to the MWPotential2014 frame (R0_XY, V_SUN); D10 passes the McMillan17 frame."""
    r0_xy = R0_XY if r0_xy is None else r0_xy; v_sun = V_SUN if v_sun is None else np.asarray(v_sun, float)
    ra, dec = np.radians(ra), np.radians(dec)
    cr, sr, cd, sd = np.cos(ra), np.sin(ra), np.cos(dec), np.sin(dec)
    pos = d_kpc*np.array([cd*cr, cd*sr, sd])
    e_r = np.array([cd*cr, cd*sr, sd]); e_a = np.array([-sr, cr, 0*sr]); e_d = np.array([-sd*cr, -sd*sr, cd])
    vel = rv*e_r + K_PM*d_kpc*(pmra*e_a + pmdec*e_d)
    p, v = T_ICRS_GAL @ pos, T_ICRS_GAL @ vel
    dgc = math.hypot(r0_xy, Z_SUN); p[0] = p[0] - dgc
    th = math.asin(Z_SUN/dgc); H = np.array([[math.cos(th), 0, math.sin(th)], [0, 1, 0], [-math.sin(th), 0, math.cos(th)]])
    return H @ p, H @ v + v_sun[:, None]
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

def orbit_params_batch(x, y, z, vx, vy, vz, t_gyr=3.0, dt=0.01, mw=None):
    """Many stars at once (arrays, kpc and km/s): kick-drift-kick leapfrog in natural units (r0 = 8 kpc, v0 = 220 km/s),
    fixed step dt; r_peri / r_apo / z_max from every step. Returns dict of arrays."""
    from . import galaxy as G
    mw = mw or G.MW(); r0, v0 = 8.0, 220.0
    X = np.array([x, y, z], float)/r0; V = np.array([vx, vy, vz], float)/v0
    def acc(X):
        R = np.hypot(X[0], X[1]); FR, Fz = G.force_array(mw, R, X[2])
        return np.array([FR*X[0]/R, FR*X[1]/R, Fz])
    tn = t_gyr/(r0*3.0856775814913673e16/v0/3.15576e16); n = int(math.ceil(tn/dt)); h = tn/n
    r = np.sqrt((X**2).sum(0)); rp, ra, zm = r.copy(), r.copy(), np.abs(X[2])
    a = acc(X)
    for _ in range(n):
        V += 0.5*h*a; X += h*V; a = acc(X); V += 0.5*h*a
        r = np.sqrt((X**2).sum(0)); np.minimum(rp, r, out=rp); np.maximum(ra, r, out=ra); np.maximum(zm, np.abs(X[2]), out=zm)
    return dict(rperi=rp*r0, rapo=ra*r0, zmax=zm*r0, ecc=(ra - rp)/(ra + rp))

def _vertex(t0, t1, t2, y0, y1, y2):
    """Extremum of the parabola through three points (unequal spacing); falls back to y1 if degenerate."""
    d0, d1 = t1 - t0, t2 - t1
    a = ((y2 - y1)/d1 - (y1 - y0)/d0)/(d0 + d1)
    b = (y1 - y0)/d0 - a*(t1 + t0)            # y = a t^2 + b t + c through the points
    tv = np.where(np.abs(a) > 0, -b/(2*a), t1)
    c = y1 - a*t1*t1 - b*t1
    yv = a*tv*tv + b*tv + c
    ok = (tv > t0) & (tv < t2)
    return np.where(ok, yv, y1)
def orbit_params_batch2(x, y, z, vx, vy, vz, t_gyr=3.0, eta=0.01, mw=None, max_steps=200000):
    """A8c2: per-star adaptive kick-drift-kick (dt_i = eta * r_i/|v_i|, capped at 0.02 natural units), every star
    independent so each takes its own step; turning points of r and |z| refined by a parabola through the last three
    samples. Natural units r0 = 8 kpc, v0 = 220 km/s."""
    from . import galaxy as G
    mw = mw or G.MW(); r0, v0 = 8.0, 220.0
    X = np.array([x, y, z], float)/r0; V = np.array([vx, vy, vz], float)/v0; N = X.shape[1]
    def acc(X):
        R = np.hypot(X[0], X[1]); FR, Fz = G.force_array(mw, R, X[2])
        return np.array([FR*X[0]/R, FR*X[1]/R, Fz])
    T = t_gyr/(r0*3.0856775814913673e16/v0/3.15576e16)
    t = np.zeros(N); r = np.sqrt((X**2).sum(0)); az = np.abs(X[2])
    rp, ra, zm = r.copy(), r.copy(), az.copy()
    hist_t = [t.copy(), t.copy()]; hist_r = [r.copy(), r.copy()]; hist_z = [az.copy(), az.copy()]
    a = acc(X); live = np.ones(N, bool); steps = 0
    while live.any() and steps < max_steps:
        sp = np.sqrt((V**2).sum(0)); h = np.minimum(eta*r/np.maximum(sp, 1e-12), 0.02); h = np.where(live, np.minimum(h, T - t), 0.0)
        V += 0.5*h*a; X += h*V; a = acc(X); V += 0.5*h*a; t += h; steps += 1
        r = np.sqrt((X**2).sum(0)); az = np.abs(X[2])
        for hy, cur, ext, fn in ((hist_r, r, rp, np.minimum), (hist_r, r, ra, np.maximum), (hist_z, az, zm, np.maximum)):
            y0, y1 = hy[0], hy[1]
            if fn is np.minimum: turn = (y1 <= y0) & (y1 <= cur)
            else: turn = (y1 >= y0) & (y1 >= cur)
            v = _vertex(hist_t[0], hist_t[1], t, y0, y1, cur)
            fn(ext, np.where(turn & live, v, ext), out=ext); fn(ext, np.where(live, cur, ext), out=ext)
        hist_t = [hist_t[1], t.copy()]; hist_r = [hist_r[1], r.copy()]; hist_z = [hist_z[1], az.copy()]
        live = t < T - 1e-12
    return dict(rperi=rp*r0, rapo=ra*r0, zmax=zm*r0, ecc=(ra - rp)/(ra + rp), steps=steps)

def orbit_params_batch3(x, y, z, vx, vy, vz, t_gyr=3.0, eta=0.01, eta_in=0.006, r_in_kpc=1.0, mw=None, max_steps=400000):
    """A8c3: as batch2, faster — bulge enclosed mass from a 20000-point log-r table (linear interpolation in ln r),
    turning-point parabolas evaluated only where a turn occurs, two-tier step (eta_in inside r_in_kpc)."""
    from . import galaxy as G
    from scipy.special import gamma, gammainc
    mw = mw or G.MW(); p = mw.p; r0, v0 = 8.0, 220.0
    s = (3 - p['alpha'])/2; lr_tab = np.linspace(math.log(1e-5), math.log(200.0), 20000)
    Mb_tab = 2*math.pi*p['bamp']*p['rc']**(3 - p['alpha'])*gamma(s)*gammainc(s, (np.exp(lr_tab)/p['rc'])**2)
    def acc(X):
        R = np.hypot(X[0], X[1]); r = np.sqrt(R*R + X[2]*X[2])
        Mb = np.interp(np.log(r), lr_tab, Mb_tab)
        fs = (-Mb/r**2 - p['hamp']*(np.log1p(r/p['ha'])/r**2 - 1/(r*(p['ha'] + r))))/r
        sq = np.sqrt(X[2]*X[2] + p['b']**2); D = (R*R + (p['a'] + sq)**2)**1.5
        fd = -p['damp']/D
        return np.array([(fs + fd)*X[0], (fs + fd)*X[1], fs*X[2] + fd*X[2]*(p['a'] + sq)/sq])
    X = np.array([x, y, z], float)/r0; V = np.array([vx, vy, vz], float)/v0; N = X.shape[1]
    T = t_gyr/(r0*3.0856775814913673e16/v0/3.15576e16); rin = r_in_kpc/r0
    t = np.zeros(N); r = np.sqrt((X**2).sum(0)); az = np.abs(X[2])
    rp, ra, zm = r.copy(), r.copy(), az.copy()
    t1, t2 = t.copy(), t.copy(); r1, r2 = r.copy(), r.copy(); z1, z2 = az.copy(), az.copy()
    a = acc(X); live = np.ones(N, bool); steps = 0
    while live.any() and steps < max_steps:
        sp = np.sqrt((V**2).sum(0)); et = np.where(r < rin, eta_in, eta)
        h = np.minimum(et*r/np.maximum(sp, 1e-12), 0.02); h = np.where(live, np.minimum(h, T - t), 0.0)
        V += 0.5*h*a; X += h*V; a = acc(X); V += 0.5*h*a; t = t + h; steps += 1
        r = np.sqrt((X**2).sum(0)); az = np.abs(X[2])
        for y2, y1, cur, ext, lo in ((r2, r1, r, rp, True), (r2, r1, r, ra, False), (z2, z1, az, zm, False)):
            turn = ((y1 <= y2) & (y1 <= cur)) if lo else ((y1 >= y2) & (y1 >= cur))
            idx = np.nonzero(turn & live)[0]
            if idx.size:
                v = _vertex(t2[idx], t1[idx], t[idx], y2[idx], y1[idx], cur[idx])
                ext[idx] = np.minimum(ext[idx], v) if lo else np.maximum(ext[idx], v)
            if lo: np.minimum(ext, np.where(live, cur, ext), out=ext)
            else: np.maximum(ext, np.where(live, cur, ext), out=ext)
        t2, t1 = t1, t; r2, r1 = r1, r; z2, z1 = z1, az
        live = t < T - 1e-12
    return dict(rperi=rp*r0, rapo=ra*r0, zmax=zm*r0, ecc=(ra - rp)/(ra + rp), steps=steps)

def orbit_params_exact_events(x, y, z, vx, vy, vz, t_gyr=3.0, mw=None):
    """A8c4 reference: DOP853 (rtol 1e-12) with EVENTS at every turning point — d(r^2)/dt = 0 (peri/apo) and v_z = 0
    (z extrema) — so extremes are located to integrator precision, with no sampling."""
    from scipy.integrate import solve_ivp
    from . import galaxy as G
    mw = mw or G.MW(); r0, v0 = 8.0, 220.0
    X0 = np.array([x, y, z])/r0; V0 = np.array([vx, vy, vz])/v0
    def rhs(_, s):
        R = math.hypot(s[0], s[1]); FR, Fz = mw.force(R, s[2])
        return [s[3], s[4], s[5], FR*s[0]/R, FR*s[1]/R, Fz]
    ev_r = lambda _, s: s[0]*s[3] + s[1]*s[4] + s[2]*s[5]
    ev_z = lambda _, s: s[5]
    T = t_gyr/(r0*3.0856775814913673e16/v0/3.15576e16)
    sol = solve_ivp(rhs, [0, T], np.concatenate([X0, V0]), method='DOP853', rtol=1e-12, atol=1e-13, events=[ev_r, ev_z])
    r_all = [np.linalg.norm(X0), np.linalg.norm(sol.y[:3, -1])] + [float(np.linalg.norm(q[:3])) for q in sol.y_events[0]]
    z_all = [abs(X0[2]), abs(sol.y[2, -1])] + [abs(float(q[2])) for q in sol.y_events[1]]
    rp, ra = min(r_all)*r0, max(r_all)*r0
    return dict(rperi=rp, rapo=ra, zmax=max(z_all)*r0, ecc=(ra - rp)/(ra + rp))

def orbit_params_galpy(x, y, z, vx, vy, vz, pot='MWPotential2014', t_gyr=3.0, n=3001):
    """D9: galpy-backed orbits (C integrator dop853_c) in MWPotential2014 or McMillan17 (C8/D1194: McMillan17 passes
    Horta+2026 at R_sun, MWPotential2014 fails). Inputs Galactocentric cartesian arrays (kpc, km/s); returns dict of arrays
    r_peri, r_apo (spherical r, kpc), z_max (kpc), ecc. Axisymmetric potentials, so the sense of rotation does not matter."""
    import warnings; warnings.filterwarnings('ignore')
    import astropy.units as u
    from galpy.orbit import Orbit
    if pot == 'McMillan17':
        from galpy.potential.mwpotentials import McMillan17 as P; ro, vo = 8.21, 233.1
    else:
        from galpy.potential import MWPotential2014 as P; ro, vo = 8.0, 220.0
    x, y, z, vx, vy, vz = (np.atleast_1d(np.asarray(a, float)) for a in (x, y, z, vx, vy, vz))
    R = np.hypot(x, y); phi = np.arctan2(y, x)
    vR = (x*vx + y*vy)/R; vT = (x*vy - y*vx)/R
    vxvv = np.array([R/ro, vR/vo, vT/vo, z/ro, vz/vo, phi]).T   # natural units (DEVIATIONS_D9 D1)
    o = Orbit(vxvv, ro=ro, vo=vo, radec=False)
    o.integrate(np.linspace(0, t_gyr, n)*u.Gyr, P, method='dop853_c')
    ts = np.linspace(0, t_gyr, n)*u.Gyr
    r = np.sqrt(o.R(ts)**2 + o.z(ts)**2); r = np.atleast_2d(r)
    zz = np.atleast_2d(np.abs(o.z(ts)))
    rp, ra = r.min(axis=1), r.max(axis=1)
    return dict(rperi=rp, rapo=ra, zmax=zz.max(axis=1), ecc=(ra - rp)/(ra + rp))
