#!/usr/bin/env python3
"""Bridge: merge all workers' catalogues into tools/seed/bridge/{workers,archive,best}.json for the dashboard."""
import json, os, glob, math, time
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, 'bridge'); os.makedirs(OUT, exist_ok=True)
def jl(p): return [json.loads(l) for l in open(p)] if os.path.exists(p) else []
def tail(p, n=1):
    if not os.path.exists(p): return ''
    L = [l.strip() for l in open(p) if l.strip() and not l.startswith('chi [') and 'VERDICT (unified' not in l]; return L[-1] if L else ''
W = []; allrecs = []
def stat(name, recs, status):
    ok = [r for r in recs if r.get('alpha_s') is not None]
    safe = [r for r in ok if r.get('safe')]; hits = [r for r in safe if (r.get('Ms') or 0) >= 4e15 and abs(r['alpha_s'] - 0.118) <= 0.0018]
    best = min((abs(r['alpha_s'] - 0.118) for r in safe if (r.get('Ms') or 0) >= 4e15), default=None)
    W.append(dict(worker=name, status=status[:120], models=len(recs), exotic_safe=len(safe), hits=len(hits), best_dalpha=None if best is None else round(best, 4)))
    for r in recs: r['_worker'] = name; allrecs.append(r)
# 1 cloud core 1: D2105 outward (log + results)
o = os.path.join(H, 'outward_results.json'); recs = json.load(open(o)).get('safe', []) if os.path.exists(o) else []
stat('Cloud core 1 (outward levels, D2105)', recs, tail('/tmp/claude-0/outward.log'))
# 2 cloud core 2: sonar-magnet
stat('Cloud core 2 (sonar-magnet, D2107)', jl(os.path.join(H, 'sonar', 'nodes.jsonl')), tail(os.path.join(H, 'sonar', 'run.log')))
# 3 PC shards (staged into uploads at check-ins) + cloud torus catalogues
pc = []
for p in glob.glob('/mnt/user-data/uploads/**/shard_*/catalog.jsonl', recursive=True): pc += jl(p)
stat('PC all cores (torus B4+, D2106)', pc, 'staged %d shard files' % len(glob.glob('/mnt/user-data/uploads/**/shard_*/catalog.jsonl', recursive=True)))
tc = []
for p in glob.glob(os.path.join(H, 'torus*', 'catalog.jsonl')): tc += jl(p)
stat('Cloud torus (earlier slices)', tc, 'stopped; record kept')
arch = {}
for r in allrecs:
    if r.get('alpha_s') is None: continue
    chi = [float(eval(c)) if isinstance(c, str) else float(c) for c in r['chi']]
    cell = tuple(round(math.log(c)*4)/4 for c in chi); sc = abs(r['alpha_s'] - 0.118)/0.0018 + 5*(not r.get('safe')) + 3*((r.get('Ms') or 0) < 4e15)
    if cell not in arch or sc < arch[cell]['score']:
        arch[cell] = dict(ln_chi1=cell[0], ln_chi2=cell[1], ln_chi3=cell[2], score=round(sc, 2), alpha_s=round(r['alpha_s'], 4), exotic_safe=bool(r.get('safe')), worker=r['_worker'])
best = sorted(arch.values(), key=lambda a: a['score'])[:15]
stamp = time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())
for n, d in (('workers', W), ('archive', list(arch.values())), ('best', best)): json.dump(d, open(os.path.join(OUT, n + '.json'), 'w'))
print(stamp, json.dumps(W, indent=0)[:1500]); print('cells', len(arch))
