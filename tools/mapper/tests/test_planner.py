import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from tools.mapper import planner as P
def test_altitude_vs_independent_formula():
    # independent check: altitude from hour angle with astropy's own sidereal time
    from astropy.time import Time; import astropy.units as u, math
    p = P.plan('okc', '2026-11-20T04:00:00', aperture_mm=80, which=('stars',))
    t = Time('2026-11-20T04:00:00'); lst = t.sidereal_time('apparent', longitude=-97.5164*u.deg).deg
    r = next(x for x in p['targets'] if x['name'] == 'Vega') if any(x['name'] == 'Vega' for x in p['targets']) else p['targets'][0]
    H = math.radians((lst - r['ra'] + 540) % 360 - 180); d = math.radians(r['dec']); f = math.radians(35.4676)
    alt = math.degrees(math.asin(math.sin(f)*math.sin(d) + math.cos(f)*math.cos(d)*math.cos(H)))
    assert abs(alt - r['alt_now']) < 0.6     # refraction-free spherical formula vs astropy (precession/nutation/aberration ~0.3 deg)
def test_aperture_limits_targets_and_sorting():
    small = P.plan('okc', '2026-11-20T04:00:00', aperture_mm=10, which=('messier',))
    big = P.plan('okc', '2026-11-20T04:00:00', aperture_mm=200, which=('messier',))
    assert big['n'] >= small['n']
    vis = [r for r in big['targets'] if r['visible_now']]
    assert all(vis[i]['pct_of_best'] >= vis[i + 1]['pct_of_best'] for i in range(len(vis) - 1))
def test_exports():
    p = P.plan('okc', '2026-11-20T04:00:00', aperture_mm=80, which=('messier',))
    assert P.to_csv(p).startswith('name,') and '<VOTABLE' in P.to_votable(p) and P.to_astroplan_csv(p).startswith('name,ra_deg')
