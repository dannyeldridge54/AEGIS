import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from tools.janus_astro import settings as S, bbn as B
def test_bbn_matches_module_and_pulls():
    r = S.bbn(0.02237)
    assert r['Yp'] == B.Yp(0.02237) and r['DH'] == B.DH(0.02237)
    assert all(abs(p) < 5 for p in r['pulls'].values())
def test_ns_matches_validated_value():
    assert abs(S.neutron_star('SLy')['M_max_Msun'] - 2.048) < 0.002     # D1058/D1090
def test_jfactor_positive_all_profiles():
    for p in S.HALOS: assert S.jfactor(p)['J_GeV2_cm5'] > 0
def test_exports():
    rows = [S.bbn(0.02237), S.bbn(0.0224, 0.1)]
    assert S.export(rows, 'json').startswith('[') and S.export(rows, 'csv').startswith('omega_b') and S.export(rows, 'ecsv').startswith('# %ECSV')
