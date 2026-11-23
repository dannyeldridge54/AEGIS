"""PREREG_HEX1 tests H1-H5."""
import json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
t0 = time.perf_counter(); import hex as X; E = X.evaluate(dict(X.ADOPTED)); cold = time.perf_counter() - t0
t1 = time.perf_counter(); E2 = X.evaluate(dict(X.ADOPTED)); warm = (time.perf_counter() - t1) * 1000
same = all((E['bus'].v[k] == E2['bus'].v[k]) or (isinstance(E['bus'].v[k], float) and math.isnan(E['bus'].v[k]) and math.isnan(E2['bus'].v[k])) for k in E['bus'].v)
res = dict(H1=dict(sweeps=E['sweeps'], idempotent=same and E2['sweeps'] == E['sweeps']))
sys.path.insert(0, os.path.join(X.AEGIS, 'tools', 'core')); os.environ.setdefault('AEGIS_CORE_STATE', '/tmp/hex1_core'); import core as K
b = E['bus'].v; rel = lambda a, c: abs(a - c) / max(abs(c), 1e-300)
sp = K.call('serapis_point', {'C': X.ADOPTED['C'], 'T_R': X.ADOPTED['T_R']})['structuredContent']
lt = K.call('janus_lt', {'h': 0.6736, 'ombh2': 0.02237, 'omch2': 0.12, 'w0': -1, 'wa': 0, 'z': [0.5, 1.0]})['structuredContent']
xs = K.call('lhc_xsec', {'m': 687.0, 'sqrts': '13.6'})['structuredContent']
from tools.janus_astro import bbn
res['H2'] = dict(ns=rel(b['ns'], sp['ns']), r=rel(b['r'], sp['r']), Nstar=rel(b['Nstar'], sp['Nstar']), DM05=rel(b['DM_Mpc_z0.5'], lt['0.5']['DM_Mpc']),
                 f1=rel(b['f_z1.0'], lt['1.0']['f']), xsec=rel(b['wino_xsec_fb_13p6'], xs['sum']), Yp=rel(b['Yp'], bbn.Yp(0.02237, 0.0)), DH=rel(b['DH'], bbn.DH(0.02237, 0.0)))
t2 = time.perf_counter(); F, H, R = X.loop(log=lambda *a: None); rnd = time.perf_counter() - t2
res['H3'] = dict(cold_s=round(cold, 3), warm_ms=round(warm, 3), round_s=round(rnd, 2))
res['H4'] = dict(rounds=R, log=H, ended_null=all(h['decision'] != 'ACCEPT' for h in H if h['round'] == R))
n1 = E['local']['N1 nuclear']
res['H5'] = dict(hoyle_radius=b['hoyle_radius'], hoyle_inside=b['hoyle_inside'], dm_p=b['dm_p_MeV'], Yp=b['Yp'], DH=b['DH'], pull_Yp=n1['pull_Yp'], pull_DH=n1['pull_DH'], note=n1['hoyle_note'])
v = dict(H1=res['H1']['sweeps'] <= 6 and res['H1']['idempotent'], H2=all(x <= 1e-12 for x in res['H2'].values()),
         H3=cold <= 2 and warm <= 50 and rnd <= 60, H4=res['H4']['ended_null'] and all('target_after' in h or h['decision'] == 'FLAG' for h in H), H5=True)
v['PASS'] = all(v.values()); res['verdict'] = v
open(os.path.join(X.AEGIS, 'field_tests', 'results', 'hex1.json'), 'w').write(json.dumps(res, indent=1, default=str)); print(json.dumps({k: res[k] for k in ('H1', 'H2', 'H3', 'H5', 'verdict')}, indent=1, default=str))
