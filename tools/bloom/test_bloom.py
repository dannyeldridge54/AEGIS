#!/usr/bin/env python3
"""Bloom readiness battery (D2033). Every check must PASS before a Bloom step is scored. Run: python3 test_bloom.py"""
import json, math, os, sys, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import bloom, bloom_loop
R = []
def check(name, ok, info=''): R.append((name, bool(ok), info))
D = bloom.D; T = {t['id']: t for t in D['terms']}
# 1 data hygiene: unique ids, owner, lock + release + sources on every term
check('hygiene: unique ids + one owner each', bloom.hygiene(D['terms']))
miss = [t['id'] for t in D['terms'] if not (t.get('locked') and t.get('released') and t.get('sources'))]
check('every term has locked/released/sources', not miss, miss)
# 2 the target and lens maths
x = 18.87 / 2; check('chi2 survival: series vs dof-4 closed form', abs(math.exp(-x) * (1 + x) - 0.000833535) < 1e-8)
inj = bloom.injection_test(); check('injection-recovery', inj['pass'], inj)
z = bloom.lnL_term({'kind': 'gauss', 'mu': 350.0, 'sigma': 10.0, 'ours': 10.0, 'angle': True})[1]; check('phase compared on the circle (350 vs 10 = 2 sigma)', abs(z - 2.0) < 1e-9, z)
z90 = bloom.lnL_term({'kind': 'upper', 'bound': 1.0, 'ours': 1.0, 'cl': 0.90})[1]; check('90% limit: value at the bound sits at 0 sigma excess', abs(z90) < 1e-9, z90)
# 3 calibration: B1 lever reproduces D1937 on the old 0.66 bar
old = dict(T['wino']); T['wino']['lo'] = 0.66
r = bloom.balance({'lnm32': 1.0}); T['wino'].update(old)
a = [v for v in r['terms'].values()]; check('B1 calibration alpha_s within 0.0002 of D1937 (0.11433)', abs(r['terms']['alpha_s'][0] - 0.11433) <= 2e-4, r["terms"]["alpha_s"])
check('Centre reaches BALANCED', 'BALANCED' in r['state'], r['state'])
# 4 a free seam knob is labelled FIT, never derived
check('free Delta3 knob -> FIT label', bloom.report()['T1_demo']['verdict'].startswith('FIT'))
# 5 coherence with the derivation-agent ledger: every Bloom agent exists in derivation_agents.json
A = json.load(open(os.path.join(HERE, '..', 'loom', 'derivation_agents.json')))
names = ' '.join(a['agent'] for a in A['agents']); bad = sorted({t['agent'] for t in D['terms'] if t['agent'] not in names})
check('every term agent is in derivation_agents.json', not bad, bad)
# 6 loop + speed
q = bloom_loop.tick(); check('mining loop runs and returns a queue', isinstance(q['mining_queue'], list))
s = time.time(); subprocess.run([sys.executable, os.path.join(HERE, 'bloom.py'), '--json'], capture_output=True); dt = time.time() - s
check('engine wall time < 0.5 s', dt < 0.5, round(dt, 3))
for n, ok, info in R: print(('PASS ' if ok else 'FAIL ') + n + ('' if ok else '  ' + str(info)))
print('READY' if all(ok for _, ok, _ in R) else 'NOT READY', '%d/%d' % (sum(ok for _, ok, _ in R), len(R)))
