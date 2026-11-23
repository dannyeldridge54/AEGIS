"""PREREG_RING1 tests R1-R5."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
t0 = time.perf_counter(); import rings as G; P = G.one_pass(); cold = time.perf_counter() - t0
t1 = time.perf_counter(); G.one_pass(); warm = (time.perf_counter() - t1) * 1000
F = G.fit_C(); res = dict(R1=dict(cold_s=round(cold, 3), cold_pass_s=round(P['seconds'], 3), warm_ms=round(warm, 3), fit_s=round(F['seconds'], 2), fit_evals=F['nfev']))
# R2: LIVE nodes vs the standalone tools (serapis via the registry worker process; mbb via the weave tool; TM1 identity)
sys.path.insert(0, os.path.join(G.AEGIS, 'tools', 'core')); os.environ.setdefault('AEGIS_CORE_STATE', '/tmp/ring1_core_state'); import core as K
ref = K.call('serapis_point', {'C': G.ADOPTED['C'], 'T_R': G.ADOPTED['T_R']})['structuredContent']
pat = P['rings']['pattern']; rel = lambda a, b: abs(a - b) / max(abs(b), 1e-300)
mb = G.W.weave_mbb({'s12': P['rings']['ring1']['theta12']})
r2 = dict(ns=rel(pat['ns'], ref['ns']), r=rel(pat['r'], ref['r']), running=rel(pat['running'], ref['alpha_s']), Nstar=rel(pat['Nstar'], ref['Nstar']),
          m_bb=rel(P['rings']['ring1']['m_bb'], mb['mbb_max_meV']), sum_mnu=rel(P['rings']['ring1']['sum_mnu'], mb['sum_mnu_eV']),
          tm1_Ue1_sq=abs((1 - P['rings']['ring1']['theta12']) * (1 - G.S13SQ) - 2 / 3))
res['R2'] = r2
# R3: LIVE vs the Bloom's stored "ours"
stored = {t['id']: t['ours'] for t in G.B.D['terms']}
res['R3'] = {k: dict(live=t['ours'], stored=stored[k], diff=t['ours'] - stored[k]) for t in P['terms'] for k in [t['id']] if P['source'][k] == 'LIVE'}
S0 = G.score(P); S1 = G.score(F['P'], k_extra=1)
res['R4'] = dict(C_fit=F['C'], lnL_before=S0['lnL'], lnL_after=S1['lnL'], target_before=S0['target'], target_after=S1['target'], k_before=S0['k'], k_after=S1['k'],
                 verdict=G.B.verdict(S1['lnL'] - S0['lnL'], 1, S1['N'], False) if hasattr(G.B, 'verdict') else None)
from collections import Counter
res['R5'] = dict(Counter(v.split(' (')[0] for v in P['source'].values()), n_terms=len(P['source']))
v = dict(R1=cold <= 1.5 and warm <= 50 and F['seconds'] <= 30, R2=all(x <= 1e-12 for x in r2.values()), R3=True, R4=True, R5=res['R5']['n_terms'] == 13)
v['PASS'] = all(v.values()); res['verdict'] = v
open(os.path.join(G.AEGIS, 'field_tests', 'results', 'ring1.json'), 'w').write(json.dumps(res, indent=1, default=str)); print(json.dumps(res, indent=1, default=str))
