"""PREREG_CORE1 tests K1-K5."""
import json, os, pathlib, shutil, sys, time
HERE = pathlib.Path(__file__).resolve().parent
os.environ['AEGIS_CORE_STATE'] = str(HERE / 'state_test'); shutil.rmtree(HERE / 'state_test', ignore_errors=True)
sys.path.insert(0, str(HERE)); import core as K
S = K.specs(); res = {'n_tools': len(S)}
res['K1'] = {n: K.validate(s['inputSchema'], s['example']) for n, s in S.items() if K.validate(s['inputSchema'], s['example'])}
t0 = time.time(); calls = {}
for n, s in S.items():
    try: r = K.call(n, s['example']); calls[n] = dict(err=r['isError'], msg=r['content'][0]['text'][:160] if r['isError'] else '', s=r['provenance']['seconds'])
    except Exception as e: calls[n] = dict(crash=f'{type(e).__name__}: {e}')
res['K2_seconds'] = round(time.time() - t0, 1)
res['K2_pass'] = sorted(n for n, c in calls.items() if c.get('err') is False)
res['K2_errors'] = {n: c['msg'] for n, c in calls.items() if c.get('err')}
res['K2_crashes'] = {n: c['crash'] for n, c in calls.items() if 'crash' in c}
res['K2_err_without_msg'] = [n for n, c in calls.items() if c.get('err') and not c['msg']]
# K3 cache
probe = 'chronos_make_now'; r1 = K.call(probe, S[probe]['example']); t1 = time.perf_counter(); r2 = K.call(probe, S[probe]['example']); dt = (time.perf_counter() - t1) * 1000
res['K3'] = dict(ms=round(dt, 2), identical=r1['structuredContent'] == r2['structuredContent'], cached=r2['provenance']['cached'], linked=r2['provenance']['source_id'] is not None)
# K4 provenance
recs = [json.loads(l) for l in (K.LEDGER).read_text().splitlines()]
need = {'id', 'tool', 'args', 'args_hash', 'code_hash', 'result_hash', 'isError', 'cached', 'source_id', 'parents', 't', 'seconds'}
res['K4'] = dict(records=len(recs), expected=len(S) + 2, all_fields=all(need <= set(r) for r in recs))
# K5 bad input
b1 = K.call('chronos_make_now', {'nuclide': 'F-18', 'A_needed': 'lots', 'hours': 2.5}); b2 = K.call('chronos_make_now', {'nuclide': 'F-18', 'hours': 2.5})
res['K5'] = dict(wrong_type=b1['isError'] and 'A_needed' in b1['content'][0]['text'], missing=b2['isError'] and 'A_needed' in b2['content'][0]['text'],
                 msgs=[b1['content'][0]['text'], b2['content'][0]['text']])
v = dict(K1=not res['K1'], K2=not res['K2_crashes'] and not res['K2_err_without_msg'], K3=res['K3']['identical'] and res['K3']['cached'] and res['K3']['linked'] and res['K3']['ms'] <= 20,
         K4=res['K4']['records'] == res['K4']['expected'] and res['K4']['all_fields'], K5=res['K5']['wrong_type'] and res['K5']['missing'])
v['PASS'] = all(v.values()); res['verdict'] = v; res['K2_pass_rate'] = f"{len(res['K2_pass'])}/{len(S)}"
out = HERE.parent.parent / 'field_tests' / 'results' / 'core1.json'; out.write_text(json.dumps(res, indent=1, default=str))
print(json.dumps({k: res[k] for k in ('n_tools', 'K2_pass_rate', 'K2_seconds', 'K3', 'K4', 'verdict')}, indent=1)); print(json.dumps(res['K2_errors'], indent=1)[:3000]); print(res['K1'], res['K2_crashes'])
