import json, itertools
E9 = {30: 86, 31: 95, 32: 104, 33: 118, 34: 129, 35: 140}; D = range(4, 10); feas = []
def comps(total, k):
    if k == 1: yield (total,); return
    for i in range(total + 1):
        for r in comps(total - i, k - 1): yield (i,) + r
for c in comps(40, 6):
    nd = dict(zip(D, c)); s = sum(d * nd[d] for d in D)
    if s % 2: continue
    e = s // 2; g = 40 * e - sum(nd[d] * (d * d + E9[39 - d]) for d in D)
    if g >= 0: feas.append(dict(n=nd, e=e, gamma=g))
es = sorted({f['e'] for f in feas}); mind = {}
for f in feas:
    m = min(d for d in D if f['n'][d]); mind[m] = mind.get(m, 0) + 1
out = dict(prereg='PREREG_D2001_tile_count.md', feasible_compositions=len(feas), e_range=[es[0], es[-1]] if es else None, by_min_degree=mind,
           regular9=next((f for f in feas if f['n'][9] == 40), None), max_gamma=max((f['gamma'] for f in feas), default=None),
           any_degree4=any(f['n'][4] > 0 for f in feas), max_n4=max((f['n'][4] for f in feas), default=0), examples=sorted(feas, key=lambda f: f['e'])[:5])
json.dump(out, open('field_tests/results/d2001_tiles.json', 'w'), indent=1); print(json.dumps({k: v for k, v in out.items() if k != 'examples'}, indent=1)); print(out['examples'][:3])
