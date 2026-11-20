import os, sys, copy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from tools.lhc import importers as I, settings as S, stats
def bkg_only(b=3.0, n=3):
    ws = S.pyhf_workspace(0.0, b, n); ws['channels'][0]['samples'] = [ws['channels'][0]['samples'][1]]; return ws
def patchset(s=5.0):
    return {'metadata': {'references': {'hepdata': 'ins0000000'}, 'description': 'test', 'digests': {'sha256': 'a'*64},
                         'labels': ['m'], 'analysis_id': 'TEST'},
            'patches': [{'metadata': {'name': 'sig_700', 'values': [700]},
                         'patch': [{'op': 'add', 'path': '/channels/0/samples/0',
                                    'value': {'name': 'signal', 'data': [s], 'modifiers': [{'name': 'mu', 'type': 'normfactor', 'data': None}]}}]}],
            'version': '1.0.0'}
def test_workspace_roundtrip_and_limit_vs_exact_poisson():
    ws = I.load_workspace(S.pyhf_workspace(1.0, 3.0, 3))
    ul = I.upper_limit(ws)['mu95_obs']           # mu x 1 signal event
    exact = stats.ul_poisson(3.0, 3)             # exact Poisson CLs N95 = 5.395 (selftest value)
    assert abs(ul - exact)/exact < 0.15          # asymptotics vs exact at small counts: same ballpark
def test_patchset_apply_gives_signal():
    ws = I.load_workspace(bkg_only())
    pw = I.apply_patch(ws, patchset(), 'sig_700', verify=False)
    assert 'signal' in [s['name'] for s in pw['channels'][0]['samples']]
    assert 0 <= I.cls(pw, 1.0)['CLs_obs'] <= 1
def test_hepdata_roundtrip():
    y = S.scan('run3', 'wino', (500, 700), 'hepdata')
    t = I.load_hepdata_table(y)
    assert t['x'] == [500.0, 700.0] and abs(t['y']['sigma(pp -> pair)']['values'][1] - S.point('run3', 'wino', 700)['sigma_fb']) < 1e-3
def test_hepdata_errors():
    d = {'independent_variables': [{'header': {'name': 'm', 'units': 'GeV'}, 'values': [{'low': 100, 'high': 200}]}],
         'dependent_variables': [{'header': {'name': 'sig'}, 'values': [{'value': 2.0, 'errors': [{'asymerror': {'plus': 0.3, 'minus': -0.2}}]}]}]}
    t = I.load_hepdata_table(d); assert t['x'] == [150.0] and t['y']['sig']['err_minus'] == [0.2]
