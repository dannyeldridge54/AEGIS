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

def test_j3_constraint_sets():
    assert {'ACT-DR6', 'P-ACT-LB', 'P-ACT-LB2', 'SPT-3G-D1', 'CMB-SPA+DESI'} <= set(S.CONSTRAINTS['ns'])
    assert S.CONSTRAINTS['r']['PR4+BK18'][0] == 0.032
    sc = S.score(S.predict('starobinsky', 55))
    assert len(sc) == len(S.CONSTRAINTS['ns']) + len(S.CONSTRAINTS['r']) and sc['r:PR4+BK18'] == 'pass'
