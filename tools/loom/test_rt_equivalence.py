#!/usr/bin/env python3
"""D1993 exactness test: engine v5 must reproduce engine v4 bit-for-bit on vclock runs (seeds 501-503, 20,000 pulses each)."""
import sys, os, time, json, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loom_rt4 as A, loom_rt5 as B
res = {}
for seed in (501, 502, 503):
    out = []
    for M in (A, B):
        t0 = time.perf_counter(); o = M.engine(1e9, seed, events=True, live_cfg=(0.16, 20), pbt=True, vclock=True, max_pulses=20000); dt = time.perf_counter() - t0
        out.append((o, dt))
    (a, ta), (b, tb) = out
    same = dict(alarms=a['alarms'] == b['alarms'], transitions=a['transitions'] == b['transitions'], gp_counts=a['gp_counts'] == b['gp_counts'],
                knobs=bool((a['x'] == b['x']).all()), fits=a['fits'] == b['fits'], pulses=a['p'] == b['p'])
    res[seed] = dict(same=same, all_same=all(same.values()), v4_pulses_per_s=round(a['p'] / ta, 1), v5_pulses_per_s=round(b['p'] / tb, 1), speedup=round(ta / tb, 2))
ok = all(r['all_same'] for r in res.values())
json.dump(dict(prereg='PREREG_D1993_speed.md', results=res, exact=ok), open('field_tests/results/d1993_equivalence.json', 'w'), indent=1)
print(json.dumps(res, indent=1)); print('EXACT' if ok else 'NOT EXACT'); sys.exit(0 if ok else 1)
