#!/usr/bin/env python3
"""Loom fast fitter (D2173 Addendum 1, TOOL). Same theory, same likelihoods, same verdict rule as weave_lcdm_pr4.py;
only the search is organised for speed:
 (a) PARALLEL STARTS: the N minimiser starts run as N separate processes (one core each) instead of one after another;
 (b) WARM STARTS: each start's reference point is drawn around the best fit already on disk for a neighbouring pair
     (same model), so the minimiser begins near the basin instead of at the generic prior centre;
 (d) THREADS: CAMB is OpenMP-parallel, so each start gets cores/N threads instead of 1;
 (e) SMALLER FIRST STEP when warm: BOBYQA rhobeg 0.25 (in prior-scaled units) instead of the default, so it does not jump out of the known basin;
 (c) every start is kept and reported; the lowest chi2_eff wins (as in PREREG_D2163).
Usage: python loom_fast.py <L|W|C> <sn> <hillipop|camspec> [N=4] [warm_json ...]
Writes pr4_<model>_<sn>[_<hl>]_fast.json next to weave_lcdm_pr4.py."""
import os, sys, json, subprocess, time, glob
HERE = os.path.dirname(os.path.abspath(__file__)); FIT = os.path.join(HERE, '..', '..', 'field_tests', 'weave_lcdm')
model, sn, hl = sys.argv[1], sys.argv[2], sys.argv[3]
N = int(sys.argv[4]) if len(sys.argv) > 4 else 4
THR = str(max(1, int(os.environ.get('LOOM_CORES', os.cpu_count() or 4)) // N))   # (d) split the machine's threads across the starts
warm = sys.argv[5:] or sorted(glob.glob(os.path.join(FIT, f'pr4_{model}_*.json')))
pt = None
for w in warm:
    try:
        d = json.load(open(w)); pt = d['point']; break
    except Exception: pass
t0 = time.time(); procs = []
for i in range(N):
    env = dict(os.environ, BEST_OF='1', OUT_SUFFIX=f'_fast{i}', OMP_NUM_THREADS=THR, OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
               **({'OVERRIDE_BOBYQA': json.dumps({'rhobeg': 0.25, 'rhoend': 0.05})} if pt and not os.environ.get('OVERRIDE_BOBYQA') else {}),
               LOOM_SEED=str(1000 + i), LOOM_WARM=json.dumps(pt) if pt else '')
    log = open(os.path.join(HERE, f'fast_{model}_{sn}_{hl}_{i}.log'), 'w')
    procs.append(subprocess.Popen([sys.executable, os.path.join(FIT, 'weave_lcdm_pr4.py'), model, sn, hl], env=env, stdout=log, stderr=subprocess.STDOUT))
for p in procs: p.wait()
suf = '' if hl == 'hillipop' else '_' + hl
runs = []
for i in range(N):
    f = os.path.join(FIT, f'pr4_{model}_{sn}_fast{i}{suf}.json')
    if os.path.exists(f): runs.append(json.load(open(f)))
best = min(runs, key=lambda r: r['chi2_eff']) if runs else None
out = dict(tool='loom_fast D2173-A1', model=model, sn=sn, hl=hl, starts=N, warm_from=warm[:1] if pt else [], wall_seconds=time.time() - t0,
           chi2_eff_all=[r['chi2_eff'] for r in runs], best=best)
json.dump(out, open(os.path.join(FIT, f'pr4_{model}_{sn}{suf}_fast.json'), 'w'), indent=1)
print('FAST DONE', model, sn, hl, round(best['chi2_eff'], 3) if best else None, round(time.time() - t0), 's', flush=True)
