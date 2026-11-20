import json, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from tools.lhc import settings as S, recast_dt, future
def test_presets_and_points():
    for run in S.RUNS:
        for model in S.MODELS:
            m = 50.0*S.RUNS[run][0] if model == 'wino' else min(50.0*S.RUNS[run][0], 1400.0)   # inside each table's range
            p = S.point(run, model, m); assert p['sigma_fb'] > 0
def test_run3_matches_xsec_table():
    from tools.lhc import xsec
    assert abs(S.point('run3', 'wino', 700)['sigma_fb'] - xsec.total(700, '13.6')['sum']) < 1e-12
def test_reach_matches_future():
    assert abs(S.reach('hl-lhc')['wino_reach_GeV'] - future.reach(14.0, 3000.0)) < 1e-9
def test_slha_width_matches_lifetime():
    from tools.lhc import lifetime
    w = lifetime.widths(700.0); line = [l for l in S.slha(700.0).splitlines() if l.startswith('DECAY')][0]
    assert abs(float(line.split()[2]) * w['tau_ns'] * 1e-9 / 6.582119569e-25 - 1) < 1e-5
def test_pyhf_workspace_valid():
    import pyhf
    ws = pyhf.Workspace(S.pyhf_workspace(5.0, 3.0, 3, 0.5)); assert ws.model().config.poi_name == 'mu'
def test_hepdata_has_both_blocks():
    y = S.scan('run2', 'higgsino', (200, 400), 'hepdata'); assert 'independent_variables' in y and 'dependent_variables' in y
