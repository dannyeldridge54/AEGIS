#!/usr/bin/env python3
"""2-minute knob burst: every fader x2 / x0.5 plus global knobs, all at once on 2 cores; catalog; combine keepers; verify."""
import subprocess, os, re, time, json
from concurrent.futures import ThreadPoolExecutor
B = '/home/claude/aegis/tools/compress/loomz10'; D = 'T300k'
N = ['o0','o1','o2','o3','o4','o5','o6','mlit','word','wpair','class','column','ltype','markup','match']
def run(tag, env):
    e = dict(os.environ); e.update(EV='1', CLASSMAP='maps2/DIR_ONE.map'); e.update(env); e = {k: v for k, v in e.items() if v != ''}; f = 'bt_%s.lz' % re.sub(r'\W', '_', tag)
    r = subprocess.run([B, 'c', D, f], env=e, capture_output=True, text=True); return tag, int(re.search(r'out (\d+)', r.stderr).group(1))
def g(i, f): v = [1.0] * 15; v[i] = f; return {'GAINS': ','.join('%g' % x for x in v)}
jobs = [('base', {})] + [('%s x%g' % (N[i], f), g(i, f)) for i in range(15) for f in (2.0, 0.5)]
jobs += [('LR1=1', {'LR1': '1'}), ('LR1=3', {'LR1': '3'}), ('SPIN=0', {'SPIN': '0'}), ('EV off', {'EV': ''})]
t0 = time.time()
with ThreadPoolExecutor(2) as ex: res = dict(ex.map(lambda j: run(*j), jobs))
base = res['base']; cat = sorted(((v - base) / base * 100, k) for k, v in res.items() if k != 'base')
print('base %d  (%d runs in %.0fs)' % (base, len(res), time.time() - t0))
for d, k in cat: print('  %-12s %+.3f%%%s' % (k, d, '  KEEP' if d < -0.01 else ''))
# combine keepers: best direction per node
gains = [1.0] * 15
for i in range(15):
    a, b = res['%s x2' % N[i]], res['%s x0.5' % N[i]]
    if min(a, b) < base * (1 - 1e-4): gains[i] = 2.0 if a < b else 0.5
env = {'GAINS': ','.join('%g' % x for x in gains)}
for k in ('LR1=1', 'LR1=3'):
    if res[k] < base * (1 - 1e-4) and res[k] == min(res['LR1=1'], res['LR1=3']): env['LR1'] = k[-1]
if res['SPIN=0'] < base * (1 - 1e-4): env['SPIN'] = '0'
comb = run('combined', env)[1]
print('COMBINED %d (%+.3f%% vs base) with %s' % (comb, (comb - base) / base * 100, env))
json.dump({'base': base, 'runs': res, 'combined': comb, 'combined_env': env}, open('burst.json', 'w'), indent=1)
