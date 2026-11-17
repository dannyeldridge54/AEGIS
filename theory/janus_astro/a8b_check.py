import math, sys, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import mapper_feed as F
import astropy.units as u, astropy.coordinates as AC
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True)); ok = {}
AG = np.array([[-0.0548755604162154, -0.8734370902348850, -0.4838350155487132],
               [+0.4941094278755837, -0.4448296299600112, +0.7469822444972189],
               [-0.8676661490190047, -0.1980763734312015, +0.4559837761750669]])   # Gaia DR3 doc Eq. 4.62
e = float(np.max(np.abs(F.T_ICRS_GAL - AG))); ok['G1'] = e <= 1e-12; P(f'G1 T_ICRS_GAL vs Gaia A_G: max {e:.1e}')
r = np.random.default_rng(2026); n = 200
ra = r.uniform(0, 360, n); dec = np.degrees(np.arcsin(r.uniform(-1, 1, n))); d = r.uniform(0.05, 5, n)
pmra, pmdec, rv = r.normal(0, 20, n), r.normal(0, 20, n), r.normal(0, 50, n)
l, b = F.icrs_to_galactic(ra, dec)
v = np.array([np.cos(np.radians(dec))*np.cos(np.radians(ra)), np.cos(np.radians(dec))*np.sin(np.radians(ra)), np.sin(np.radians(dec))])
g = AG @ v; lg, bg = np.degrees(np.arctan2(g[1], g[0])) % 360, np.degrees(np.arcsin(g[2]))
e2 = float(np.max(np.hypot(((l - lg + 180) % 360 - 180)*np.cos(np.radians(b)), b - bg))); ok['G2'] = e2 <= 1e-9; P(f'G2 (l,b) vs A_G direct: max {e2:.1e} deg')
p, vv = F.galactocentric(np.array([10.0]), np.array([20.0]), np.array([1e-12]), np.array([0.0]), np.array([0.0]), np.array([0.0]))
dgc = math.hypot(F.R0_XY, F.Z_SUN); th = math.asin(F.Z_SUN/dgc)
sun = np.array([-dgc*math.cos(th), 0.0, dgc*math.sin(th)])
e3a = float(np.max(np.abs(p[:, 0] - sun))); e3b = float(np.max(np.abs(vv[:, 0] - F.V_SUN)))
gc_icrs = AG.T @ np.array([1.0, 0, 0]); ra_gc = math.degrees(math.atan2(gc_icrs[1], gc_icrs[0])) % 360; dec_gc = math.degrees(math.asin(gc_icrs[2]))
pg, _ = F.galactocentric(np.array([ra_gc]), np.array([dec_gc]), np.array([dgc]), np.array([0.0]), np.array([0.0]), np.array([0.0]))
e3c = float(np.max(np.abs(pg[:, 0])))
ok['G3'] = e3a <= 1e-12 and e3b <= 1e-9 and e3c <= 1e-12
P(f'G3 Sun position {e3a:.1e} kpc, Sun velocity {e3b:.1e} km/s, GC -> origin {e3c:.1e} kpc (Sun at {sun.round(6)})')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if x else "FAIL"}' for k, x in ok.items()), '-> A8b', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
c = AC.SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=d*u.kpc, pm_ra_cosdec=pmra*u.mas/u.yr, pm_dec=pmdec*u.mas/u.yr, radial_velocity=rv*u.km/u.s, frame='icrs')
ga = c.galactic; eo = float(np.max(np.hypot(((l - ga.l.deg + 180) % 360 - 180)*np.cos(np.radians(b)), b - ga.b.deg)))
P(f'Reported: astropy Galactic vs Gaia convention: max {eo:.2e} deg ({eo*3.6e6:.1f} mas)')
open('field_tests/results/janus_astro_a8b.txt', 'w').write('\n'.join(out) + '\n')
