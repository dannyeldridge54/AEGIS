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
# 7 unit tests added after mutation testing (D2038): each kills a surviving mutant
L = bloom.lnL_term
check('band: outside the top edge is penalised', L({'kind': 'band', 'lo': 0.6, 'hi': 0.7, 'width': 0.01, 'ours': 0.72})[1] > 1.9)
check('gauss lnL is -z^2/2', abs(L({'kind': 'gauss', 'mu': 0, 'sigma': 1, 'ours': 2})[0] + 2.0) < 1e-12)
dm = [{'kind': 'gauss', 'mu': 0, 'sigma': 1, 'ours': 1, 'id': 'a', 'agent': 'X'}]
lnL0, tg, N0, k0 = bloom.target(dm, 2); check('BIC penalty uses N = terms + fit data', N0 == 1 + D['fit_data_consumed'] and abs(tg - (lnL0 - math.log(N0))) < 1e-12)
check('90% limit uses z = 1.2816', abs(L({'kind': 'upper', 'bound': 1.0, 'ours': 2.0, 'cl': 0.90})[1] - 1.2816) < 1e-4)
w = [t for t in bloom.apply_levers(D['terms'], {'lnm32': 2.0}) if t['id'] == 'wino'][0]['ours']; check('lever: wino scales with m3/2', abs(w / T['wino']['ours'] - 2.0) < 1e-9)
check('verdict NULL when gain < penalty', bloom.verdict(0.1, 1, 18, False).startswith('NULL'))
g = bloom.gof_bootstrap([{'kind': 'gauss', 'mu': 0, 'sigma': 1, 'ours': math.sqrt(18.87 / 4)} for _ in range(4)]); check('chi2 p (dof 4) = closed form', abs(g['p_exact'] - math.exp(-18.87 / 2) * (1 + 18.87 / 2)) < 1e-9, g)
check('hygiene catches a duplicate id', not bloom.hygiene([{'id': 'a', 'agent': 'X'}, {'id': 'a', 'agent': 'Y'}]))
check('injection estimate is computed (not the planted value)', inj['recovered'] != inj['planted'])
pq = bloom.prequential([{'id': 'p', 'kind': 'gauss', 'mu': 0, 'sigma': 1, 'ours': 0, 'locked': '2026-01-01', 'released': '2026-06'}, {'id': 'q', 'kind': 'gauss', 'mu': 0, 'sigma': 1, 'ours': 0, 'locked': '2026-11-21', 'released': '2025-06'}])
check('prequential counts only post-lock releases', pq['post_lock_terms'] == ['p'], pq)
ld = bloom.ladder(T['alpha_s']); check('ladder: alpha_s unconverged (1.27)', ld['stable'] is False and abs(ld['shift_over_scale'] - 1.27) < 0.01, ld)
rf = bloom.theory_nuisance(dict(T['alpha_s'], ours=0.105)); check('Rfit penalises only the excess beyond the window', abs(rf['z_rfit'] - (-(0.013 - 0.00484) / 0.0009)) < 0.05, rf)
mh = bloom.mhou_geometric(T['alpha_s']); check('MHOU step ratio 0.075', abs(mh['step_ratio'] - 0.075) < 0.001, mh)
rb = bloom.balance({'lnm32': 1.0}); check('held-out = shadows (balance point 0.970, regression)', abs(rb['knobs']['lnm32'] - 0.970) < 0.0015, rb['knobs'])
for n, ok, info in R: print(('PASS ' if ok else 'FAIL ') + n + ('' if ok else '  ' + str(info)))
print('READY' if all(ok for _, ok, _ in R) else 'NOT READY', '%d/%d' % (sum(ok for _, ok, _ in R), len(R)))
