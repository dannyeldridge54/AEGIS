# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Late-universe calculator vs independent routes and published values."""
import os, pytest
from tools.janus_lt.background import Cosmo
from tools.janus_lt import desi
from tools.janus_lt.growth import growth

P18 = Cosmo(67.66, 0.02242, 0.11933, Neff=3.046, mnu=0.06)

def test_distances_match_astropy_planck18():          # astropy's independent Planck18 cosmology
    P = pytest.importorskip('astropy.cosmology').Planck18
    for z in (0.5, 1.0, 2.33, 1089.9):
        assert abs(P18.DM(z)/P.comoving_distance(z).value - 1) < 1e-4, z

def test_desi_dr2_table_loads_from_anywhere(tmp_path):
    cwd = os.getcwd(); os.chdir(tmp_path)
    try: rows = desi.load()
    finally: os.chdir(cwd)
    assert len(rows) == 7 and sum(1 if r[5] != r[5] else 2 for r in rows) == 13   # DESI DR2 Table IV: 7 tracers, 13 numbers

def test_desi_prefers_evolving_dark_energy():         # DESI DR2: w0waCDM (-0.75, -0.86) fits BAO better than LambdaCDM at fixed r_d
    lcdm = desi.chi2(P18, 147.09); w = desi.chi2(Cosmo(67.66, 0.02242, 0.11933, w0=-0.75, wa=-0.86, Neff=3.046, mnu=0.06), 147.09)
    assert w < lcdm and 5 < lcdm < 60

def test_growth_rate_today():                         # f(0) ~ Omega_m^0.55 for LambdaCDM (Linder 2005), within 1%
    om = (0.02242 + 0.11933 + 0.06/93.14)/0.6766**2
    D, f = growth(P18, [0.0])[0.0]
    assert abs(D - 1) < 1e-9 and abs(f/om**0.55 - 1) < 0.01
