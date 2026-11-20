import os, numpy as np
from tools.mapper import finder as F
def test_gnomonic_centre_and_east():
    x, y, f = F.gnomonic(np.array([10.0, 11.0]), np.array([0.0, 0.0]), 10.0, 0.0)
    assert abs(x[0]) < 1e-12 and abs(y[0]) < 1e-12 and x[1] > 0.99 and f.all()     # +RA = east = +xi
def test_catalogue_and_counts():
    ra, dec, mag = F.stars(); assert len(ra) > 40000 and mag.max() <= 8.0
    i = np.argmin(mag); assert abs(ra[i] - 101.287) < 0.01                          # brightest = Sirius
def test_chart_m31(tmp_path):
    for ext in ('pdf', 'svg', 'png'):
        r = F.chart('M31', field_deg=6, fov_arcmin=(50, 180), aperture_mm=80, out=str(tmp_path / f'm31.{ext}'))
        assert os.path.getsize(r['out']) > 5000 and r['n_stars'] > 20 and abs(r['ra'] - 10.68) < 0.1

def test_resolve_exact_before_substring():
    assert F.resolve('M3')[2].startswith('M3') and not F.resolve('M3')[2].startswith('M31')
    assert F.resolve('orion nebula')[2].startswith('M42')
