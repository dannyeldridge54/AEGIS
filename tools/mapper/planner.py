# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Mapper observing planner (M1a + M2 + M1d): "what can MY telescope see tonight from MY site", sorted the way observers asked
for (percent of the object's culmination altitude 90 - |lat - dec| reached now, as KStars users proposed, so plans re-sort as the night moves; zenith-hole demotion for
alt-az Dobsonians), with exports other tools read (CSV, VOTable, an astroplan-style target table).
Positions: astropy (AltAz with the site and time). Catalogues: the Sky Map's Messier + bright-star files.
Limiting magnitude: visual rule of thumb m_lim ≈ 2.1 + 5 log10(D_mm) (labelled as an estimate)."""
import json, math, os, io
import numpy as np
SKY = os.path.join(os.path.dirname(__file__), '..', '..', 'apps', 'skymap', 'data')
SITES = {'okc': (35.4676, -97.5164, 366.0, 'Oklahoma City, OK'), 'greenwich': (51.4769, -0.0005, 46.0, 'Royal Observatory Greenwich')}

def catalogue(which=('messier', 'stars')):
    out = []
    if 'messier' in which:
        for o in json.load(open(os.path.join(SKY, 'messier.json')))['objects']:
            out.append(dict(name=o['id'] + (f" ({o['common']})" if o.get('common') else ''), kind=o['type'], mag=o.get('mag'), ra=o['ra'], dec=o['dec']))
    if 'stars' in which:
        for s in json.load(open(os.path.join(SKY, 'stars.json')))['stars']:
            out.append(dict(name=s.get('name') or s.get('desig'), kind='star', mag=s.get('mag'), ra=s['ra'], dec=s['dec']))
    return out

def mag_limit(aperture_mm):
    """Visual limiting magnitude estimate for an aperture (mm); rule of thumb, not a photometric model."""
    return 2.1 + 5*math.log10(aperture_mm)

def plan(site='okc', when=None, aperture_mm=80.0, min_alt=20.0, zenith_hole=None, hours=10.0, step_min=15, which=('messier', 'stars')):
    """Rank targets for a night. site: key of SITES or (lat, lon, height_m). when: ISO time (UTC) of 'now'; default = now.
    Returns rows with alt_now, az_now, best_alt tonight, time_best, airmass_now, pct_of_best, visible_now, observable."""
    from astropy.coordinates import EarthLocation, SkyCoord, AltAz
    from astropy.time import Time
    import astropy.units as u
    lat, lon, h, label = SITES[site] if isinstance(site, str) else (*site, 'custom site')
    loc = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=h*u.m)
    t0 = Time(when) if when else Time.now()
    times = t0 + np.arange(0, hours*60 + 1, step_min)*u.min
    cat = [c for c in catalogue(which) if c['mag'] is None or c['mag'] <= mag_limit(aperture_mm)]
    sc = SkyCoord([c['ra'] for c in cat]*u.deg, [c['dec'] for c in cat]*u.deg)
    frame = AltAz(obstime=times[:, None], location=loc)
    altaz = sc[None, :].transform_to(frame)
    alt = altaz.alt.deg; az = altaz.az.deg
    rows = []
    for j, c in enumerate(cat):
        a = alt[:, j]; ib = int(np.argmax(a)); best = float(a[ib]); now = float(a[0])
        in_hole = zenith_hole is not None and now > 90 - zenith_hole
        am = 1/math.sin(math.radians(now)) if now > 5 else None
        rows.append(dict(name=c['name'], kind=c['kind'], mag=c['mag'], ra=c['ra'], dec=c['dec'],
                         alt_now=round(now, 2), az_now=round(float(az[0, j]), 2), airmass_now=round(am, 3) if am else None,
                         best_alt=round(best, 2), time_best=times[ib].isot[:16] + 'Z',
                         culmination_alt=round(90 - abs(lat - c['dec']), 2),
                         pct_of_best=round(100*now/(90 - abs(lat - c['dec'])), 1) if now > 0 and abs(lat - c['dec']) < 90 else 0.0,
                         visible_now=now >= min_alt and not in_hole, observable=best >= min_alt, zenith_hole=in_hole))
    rows = [r for r in rows if r['observable']]
    rows.sort(key=lambda r: (not r['visible_now'], -r['pct_of_best'], r['mag'] if r['mag'] is not None else 99))
    return dict(site=label, lat=lat, lon=lon, start_utc=t0.isot[:16] + 'Z', aperture_mm=aperture_mm,
                mag_limit_estimate=round(mag_limit(aperture_mm), 2), min_alt=min_alt, n=len(rows), targets=rows)

def to_csv(p):
    import csv
    buf = io.StringIO(); cols = list(p['targets'][0]) if p['targets'] else []
    w = csv.DictWriter(buf, fieldnames=cols); w.writeheader(); [w.writerow(r) for r in p['targets']]
    return buf.getvalue()

def to_votable(p):
    """IVOA VOTable (astropy) with units on ra, dec, alt, az."""
    from astropy.table import Table
    from astropy.io.votable import from_table
    import astropy.units as u
    t = Table(rows=[{k: (v if v is not None else np.nan) for k, v in r.items()} for r in p['targets']])
    for c, un in (('ra', u.deg), ('dec', u.deg), ('alt_now', u.deg), ('az_now', u.deg), ('best_alt', u.deg)):
        if c in t.colnames: t[c].unit = un
    t.meta['description'] = f"AEGIS Mapper plan for {p['site']} from {p['start_utc']}"
    buf = io.BytesIO(); from_table(t).to_xml(buf); return buf.getvalue().decode()

def to_astroplan_csv(p):
    """name, ra, dec in degrees: the minimal target table astroplan / N.I.N.A. / Stellarium importers accept."""
    return 'name,ra_deg,dec_deg\n' + ''.join(f"{r['name']},{r['ra']:.5f},{r['dec']:.5f}\n" for r in p['targets'])
