import sys, time, json; sys.path.insert(0, '.'); sys.path.insert(0, '/home/claude/cubemind')
from tools.serapis_calc.meter import meter, TABLE, _exact
from aegis_tools.registry import call
L = []
ok1 = all(abs(meter(t[0])['P']/t[2] - 1) < 1e-6 for t in TABLE); L.append(f"T1 table points reproduce PW6: {ok1}")
ok2 = True
for ns in (0.973, 0.975):
    a = meter(ns); e = _exact(ns, 7.389e8); d = a['P']/e['P'] - 1; ok2 &= abs(d) <= 0.01
    L.append(f"T2 n_s {ns}: interp P {a['P']:.1f} C {a['C']:.4e} | exact P {e['P']:.1f} C {e['C']:.4e} | ΔP/P {d:+.3%}")
t = time.time(); r = call('string_meter', {'ns': 0.9744, 'ns_sigma': 0.0016}); dt = time.time() - t
L.append(f"T3 registry call {dt:.2f} s: {json.dumps(r)[:300]}"); ok3 = dt <= 5 and 'P' in r
rel = r.get('P_rel_sigma', 0); ok4 = 0.14/1.5 <= rel <= 0.14*1.5; L.append(f"T4 P_rel_sigma {rel:.3f} vs PW5 0.14: {ok4}")
L.append(f"VERDICT: T1 {'PASS' if ok1 else 'FAIL'} T2 {'PASS' if ok2 else 'FAIL'} T3 {'PASS' if ok3 else 'FAIL'} T4 {'PASS' if ok4 else 'FAIL'} → {'ADOPT' if ok1 and ok2 and ok3 else 'not adopted'}")
open('field_tests/results/t1_string_meter.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
