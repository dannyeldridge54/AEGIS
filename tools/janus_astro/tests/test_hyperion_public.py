# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Public Hyperion checks (no research scripts): published values or independent routes."""
import math, pytest
from tools.janus_astro import mapper_feed as F, galaxy as G, gw

def test_vc_mwpotential2014():                        # Bovy 2015: v_c(R0 = 8 kpc) = 220 km/s by construction
    pytest.importorskip('galpy')
    assert abs(220.0*G.MW().vcirc(1.0) - 220.0) < 0.5

def test_lsr_circular_in_mcmillan17():                # McMillan 2017: v_c(R0 = 8.21) = 233.1 km/s, so the LSR orbit is circular
    pytest.importorskip('galpy')
    o = F.orbit_params_galpy([-8.21], [0.0], [0.0208], [0.0], [233.1], [0.0], pot='McMillan17')
    assert abs(o['rapo'][0]/8.21 - 1) < 0.005 and o['ecc'][0] < 0.005

def test_galpy_matches_own_integrator():             # two independent integrators agree (D9, D1196)
    pytest.importorskip('galpy')
    s = (-8.5, 1, 0.3, 30, 200, 20); g = F.orbit_params_galpy(*[[c] for c in s], pot='MWPotential2014'); h = F.orbit_params(*s, t_gyr=3.0)
    assert abs(g['rperi'][0] - h['rperi']) < 0.001

def test_7pn_tidal_phase_vs_mandal():                # Mandal et al. 2412.01706 Eq. 4.48, re-implemented independently (D1211)
    m1, m2, L1, L2, f = 1.4*1.98847e30, 1.3*1.98847e30, 400.0, 600.0, 400.0
    d7 = gw.taylorf2_tidal_dphase_hfb(f, m1, m2, L1, L2, order=7) - gw.taylorf2_tidal_dphase_hfb(f, m1, m2, L1, L2, order=6.5)
    M = m1 + m2; nu = m1*m2/M**2; D = (m1 - m2)/M; X1, X2 = m1/M, m2/M
    mp = 0.5*(X2*X1**4*L1 + X1*X2**4*L2); mm = 0.5*(X2*X1**4*L1 - X1*X2**4*L2); v = (math.pi*gw.G*M*f/gw.c**3)**(1/3)
    ref = -(9*v**5/(16*nu**2))*((136190135/27433728 + 978554825/4572288*nu - 281935/6048*nu**2 + 5/3*nu**3)*mp + D*(136190135/27433728 + 213905/2592*nu + 1585/1296*nu**2)*mm)*v**4
    assert abs(d7 - ref) <= 1e-9*max(1.0, abs(ref))

def test_bbn_primat():                                # Pitrou et al. 2021: Y_p = 0.24709 at omega_b = 0.02236
    bbn = pytest.importorskip('tools.janus_astro.bbn', exc_type=ImportError)
    assert abs(bbn.Yp(0.02236) - 0.24709) < 3e-4

def test_cli_orbit_equals_pipeline():                 # the aegis command uses the same code as the Star Mapper feed
    pytest.importorskip('galpy')
    from tools.janus_astro import mapper_orbits as MO
    r = dict(source_id='1', ra='269.452', dec='4.6934', parallax=str(1000/1.8266), parallax_error='0.03', radial_velocity='-110.5',
             pmra='-802.8', pmdec='10362.4', phot_g_mean_mag='8.2', r_med_geo='1.8266')
    o = MO.process_rows([r])[0]
    assert 0 < o[10] < o[11] and 0 <= o[13] < 1
