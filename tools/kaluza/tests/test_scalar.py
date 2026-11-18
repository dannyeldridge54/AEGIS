"""kaluza_scalar regression: the 10D critical scalar KK masses (D1214, two independent solvers)."""
import math, pytest
from tools.kaluza.scalar import kk_scalar

def test_10d_critical_pruefer_matches_D1214():
    r = kk_scalar(10, 1.5)
    assert r['kind'] == 'critical'
    assert r['m2'][0] == pytest.approx(2.9795596, rel=1e-6) and r['m2'][1] == pytest.approx(14.286529, rel=1e-6)

def test_10d_critical_fd_matches_pruefer():
    a, b = kk_scalar(10, 1.5), kk_scalar(10, 1.5, method='fd')
    for x, y in zip(a['m2'], b['m2']): assert y == pytest.approx(x, rel=1e-6)

def test_mL_over_pi_recorded_values():   # D1214: m L/π = 0.93175, 2.04027 (BTR 0.97, 2.13 — the open −4% gap)
    r = kk_scalar(10, 1.5)
    assert r['mL_over_pi'][0] == pytest.approx(0.93175, abs=2e-5) and r['mL_over_pi'][1] == pytest.approx(2.04027, abs=2e-5)

def test_interval_converged():   # the ξ cut-off: L changes < 1e-6 between ξ_max 7 and 8
    a, b = kk_scalar(10, 1.5, xi=(1e-4, 7.0))['L'], kk_scalar(10, 1.5)['L']
    assert abs(b/a - 1) < 1e-6
