import math, sys, time, json, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import mapper_feed as F, galaxy as G
import astropy.units as u, astropy.coordinates as AC
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True)); ok = {}
r = np.random.default_rng(2026); n = 200
ra = r.uniform(0, 360, n); dec = np.degrees(np.arcsin(r.uniform(-1, 1, n))); d = r.uniform(0.05, 5, n)
pmra, pmdec, rv = r.normal(0, 20, n), r.normal(0, 20, n), r.normal(0, 50, n)
l, b = F.icrs_to_galactic(ra, dec)
c = AC.SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=d*u.kpc, pm_ra_cosdec=pmra*u.mas/u.yr, pm_dec=pmdec*u.mas/u.yr, radial_velocity=rv*u.km/u.s, frame='icrs')
g = c.galactic
dl = np.abs(((l - g.l.deg + 180) % 360) - 180)*np.cos(np.radians(b)); db = np.abs(b - g.b.deg)
e1 = float(np.max(np.hypot(dl, db))); ok['F1'] = e1 <= 1e-6; P(f'F1 (l,b) vs astropy: max {e1:.2e} deg')
frame = AC.Galactocentric(galcen_distance=math.hypot(8.0, 0.0208)*u.kpc, z_sun=20.8*u.pc, galcen_v_sun=AC.CartesianDifferential([11.1, 232.24, 7.25]*u.km/u.s), roll=0*u.deg)
gc = c.transform_to(frame)
p, v = F.galactocentric(ra, dec, d, pmra, pmdec, rv)
ap = np.array([gc.x.to(u.kpc).value, gc.y.to(u.kpc).value, gc.z.to(u.kpc).value]); av = np.array([gc.v_x.to(u.km/u.s).value, gc.v_y.to(u.km/u.s).value, gc.v_z.to(u.km/u.s).value])
dx, dv = float(np.max(np.abs(p - ap))), float(np.max(np.abs(v - av))); ok['F2'] = dx <= 1e-6 and dv <= 1e-4
P(f'F2 Galactocentric vs astropy: max |dx| {dx:.2e} kpc, max |dv| {dv:.2e} km/s')
from galpy.orbit import Orbit; from galpy.potential import MWPotential2014
mw = G.MW(); worst = 0.0; tcost = []
tn = 5.0/(8*3.0856775814913673e16/220/3.15576e16); t = np.linspace(0, tn, 20001)
for i in range(30):
    x, y, z, vx, vy, vz = p[0, i], p[1, i], p[2, i], v[0, i], v[1, i], v[2, i]
    t0 = time.perf_counter(); o = F.orbit_params(x, y, z, vx, vy, vz, mw); tcost.append(time.perf_counter() - t0)
    R = math.hypot(x, y); phi = math.atan2(y, x); vR = (x*vx + y*vy)/R; vT = (x*vy - y*vx)/R
    og = Orbit([R/8, vR/220, vT/220, z/8, vz/220, phi]); og.integrate(t, MWPotential2014, method='dop853_c')
    rr = np.sqrt(og.R(t, use_physical=False)**2 + og.z(t, use_physical=False)**2)*8
    gp = dict(rperi=rr.min(), rapo=rr.max(), zmax=np.abs(og.z(t, use_physical=False)).max()*8)
    gp['ecc'] = (gp['rapo'] - gp['rperi'])/(gp['rapo'] + gp['rperi'])
    e = max(abs(o[k]/gp[k] - 1) for k in ('rperi', 'rapo', 'zmax', 'ecc')); worst = max(worst, e)
ok['F3'] = worst <= 1e-4; P(f'F3 orbit params vs galpy (30 stars, 5 Gyr): worst relative {worst:.2e}; Hyperion {np.median(tcost)*1e3:.0f} ms per star')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if v_ else "FAIL"}' for k, v_ in ok.items()), '-> A8a', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
sun = F.orbit_params(-math.hypot(8.0, 0.0208), 0.0, 0.0208, 11.1, 232.24, 7.25, mw)
P('Sun:', {k: round(v_, 3) for k, v_ in sun.items()})
rec = dict(source_id='synthetic-0', l=float(l[0]), b=float(b[0]), x=float(p[0, 0]), y=float(p[1, 0]), z=float(p[2, 0]),
           M_G_noext=float(F.abs_mag_G(12.0, 1/d[0])), **{k: round(float(v_), 4) for k, v_ in F.orbit_params(p[0, 0], p[1, 0], p[2, 0], v[0, 0], v[1, 0], v[2, 0], mw).items()})
P('Sample feed record:', json.dumps(rec))
open('field_tests/results/janus_astro_a8a.txt', 'w').write('\n'.join(out) + '\n')
