#!/usr/bin/env python3
"""D1993: run independent seeds of the woven field in parallel (one per CPU core) and triangulate them.
Usage: python3 tools/loom/parallel.py <seconds> <seed> [<seed> ...]  -> field_tests/results/par_<seeds>.json"""
import json, os, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def one(args):
    T, seed, name = args
    import loom_rt5 as R
    o = R.scored(T, seed=seed, out_name=name, archive=False)
    return dict(seed=seed, verdict=o['verdict'], accuracy=o['accuracy'], pulses_per_s=o['pulses_per_s'], tally=o['goalpost_tally'], done=o['done_seconds'],
                fits=o['fits_spent'], precision=(o['precision_fast'], o['precision_full']), far=o['false_alarm_rate'])
def triangulate(T, seeds, prefix='par'):
    os.makedirs('field_tests/results/auto', exist_ok=True)
    with Pool(min(len(seeds), os.cpu_count() or 1)) as pool:
        runs = pool.map(one, [(T, s, 'auto/%s_%d.json' % (prefix, s)) for s in seeds])
    tallies = [json.dumps(r['tally'], sort_keys=True) for r in runs]
    out = dict(seconds=T, seeds=seeds, runs=runs, all_pass=all(r['verdict'] == 'PASS' for r in runs), tally_agree=len(set(tallies)) == 1,
               total_pulses_per_s=round(sum(r['pulses_per_s'] for r in runs), 1))
    return out
if __name__ == '__main__':
    T = float(sys.argv[1]); seeds = [int(x) for x in sys.argv[2:]]
    o = triangulate(T, seeds); fn = 'field_tests/results/par_%s.json' % '_'.join(map(str, seeds)); json.dump(o, open(fn, 'w'), indent=1); print(json.dumps(o, indent=1))
