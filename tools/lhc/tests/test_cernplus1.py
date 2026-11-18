# AEGIS-FP YM5IQDCVVJLT6RGZ · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""CERN+1 unit tests. Run from the repo root:  python -m pytest tools/lhc/tests -q"""
import math, pytest
from tools.lhc import xsec, lifetime, recast_dt, stats, theory_band, future, kinematics, selftest

def test_table_point_exact():            # a stored 13.6 TeV table entry is returned unchanged
    assert xsec.sigma(400, 'C1N2p', '13.6') == pytest.approx(94.95, rel=1e-6)

def test_leave_one_out_small():
    e = xsec.loo_error('13.6'); v = list(e.values()) if isinstance(e, dict) else e
    assert v is not None

def test_scaling_reproduces_13p6():
    for m in (300, 800, 1500):
        assert xsec.sigma_scaling(m, 'C1N2p', 13.6) == pytest.approx(xsec.sigma(m, 'C1N2p', '13.6'), rel=0.004)

def test_routes_agree_at_14():
    r = xsec.sigma_best(700, 'C1N2p', 14.0); assert r['route_spread'] < 0.01

@pytest.mark.parametrize('m', [50, 5000])
def test_mass_outside_table(m):
    with pytest.raises(ValueError, match='outside'): xsec.sigma(m)

def test_unknown_process():
    with pytest.raises(ValueError, match='unknown process'): xsec.sigma(700, 'XX')

def test_bad_energy():
    with pytest.raises(ValueError): xsec.sigma_best(700, 'C1N2p', -3)

def test_lifetime_values():
    assert 1e3*lifetime.dm(1000) == pytest.approx(164.11, abs=0.05)
    w = lifetime.widths(1000); assert w['ctau_cm'] == pytest.approx(5.831, abs=0.01)
    assert w['BR_pi'] + w['BR_e'] + w['BR_mu'] == pytest.approx(1.0, abs=1e-9)

def test_lifetime_bad_mass():
    with pytest.raises(ValueError, match='mass'): lifetime.dm(-5)

def test_dm_rises_with_mass():
    assert lifetime.dm(300) < lifetime.dm(1000) < lifetime.dm(3000)

def test_recasts_reproduce_atlas():
    assert recast_dt.limit_search('ATLAS_136') == pytest.approx(666.6, abs=0.5)
    assert recast_dt.limit_search('ATLAS_36') == pytest.approx(447.8, abs=0.5)

def test_unknown_search():
    with pytest.raises(ValueError, match='unknown search'): recast_dt.limit_search('BOGUS')

def test_exact_poisson():
    assert stats.ul_poisson(3.0, 3) == pytest.approx(5.395, abs=0.01)
    assert stats.ul_poisson(0.0, 0) == pytest.approx(3.0, abs=0.01)   # classic 3-event limit

def test_theory_band():
    b = theory_band.band('ATLAS_136')
    assert b['m_limit_GeV'] == pytest.approx(661.5, abs=0.6) and b['total_GeV'] == pytest.approx(10.0, abs=0.3)
    assert abs(b['published_GeV'] - b['m_limit_GeV']) < b['total_GeV']

def test_boost_median():
    import numpy as np
    assert 0.3 < float(np.median(kinematics.boost_samples(600, n=4000))) < 0.8

def test_future_ordering():
    t = future.table()
    assert t['HL-LHC']['low_bkg_TeV'] < t['HE-LHC']['low_bkg_TeV'] < t['FCC-hh']['low_bkg_TeV']

def test_selftests_T2_T3():
    r = selftest.run(); assert r['T2_pass'] and r['T3_pass']

def test_higgsino_scaling_reproduces_13p6():
    from tools.lhc import higgsino as H
    for p in H.PROCS:
        for m in (300, 800, 1400):
            assert H.sigma_scaling(m, p, 13.6) == pytest.approx(H.sigma(m, p, '13.6'), rel=0.004)

def test_higgsino_bad_inputs():
    from tools.lhc import higgsino as H
    with pytest.raises(ValueError): H.sigma(2000)
    with pytest.raises(ValueError): H.sigma(500, 'C1N2p')
