import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from tools.janus_calc import settings as S
def test_phi2_matches_selftest():
    p = S.predict('phi2', 60)
    assert abs(p['ns'] - 0.966439) < 1e-4 and abs(p['r'] - 0.132189) < 1e-4    # aegis selftest values
def test_phi2_fails_r_bound_and_starobinsky_passes():
    assert S.score(S.predict('phi2', 60))['r:BK18'] == 'FAIL'
    assert S.score(S.predict('starobinsky', 55))['r:BK18'] == 'pass'
def test_all_models_and_export():
    rows = S.table(55)
    assert len(rows) == len(S.MODELS) and all(0.9 < r['ns'] < 1.0 for r in rows)
    assert S.export(rows, 'csv').startswith('model')
