"""JANUS tick 48: derived rho-model running over the audited box vs ACT (PREREG_D1452)."""
import json, mpmath as mp
G = {}; exec(open('field_tests/scripts/d1449/vac_grid.py').read().split("rows = []")[0], G)
R_, solve = G['R_'], G['solve']
rows = []
for ns in ('0.97166', '0.97381', '0.97596'):
    for r in ('4.389e-4', '4.643e-4', '4.897e-4'):
        a, C, ok = solve(R_['obs'], (mp.mpf('1.15'), mp.log(mp.mpf('14.6'))/mp.sqrt(2)), mp.mpf('1e-6'), mp.mpf(ns), mp.mpf(r))
        rows.append(dict(ns=float(ns), r=float(r), alpha=a, C=C, converged=ok,
                         pull_PACT=(a-0.0060)/0.0055, pull_PACTLB=(a-0.0062)/0.0052))
        print(rows[-1], flush=True)
ok = [x for x in rows if x['converged']]
P = [x['pull_PACT'] for x in ok]; L = [x['pull_PACTLB'] for x in ok]
d33 = dict(P=[-1.2561272727272728, -1.2752545454545454], L=[-1.3670576923076923, -1.3872884615384615])
shift = max(abs(min(P)-min(d33['P'])), abs(max(P)-max(d33['P'])), abs(min(L)-min(d33['L'])), abs(max(L)-max(d33['L'])))
out = dict(D='D1452', rows=rows, n_converged=len(ok), alpha_range=[min(x['alpha'] for x in ok), max(x['alpha'] for x in ok)],
           pull_PACT=[min(P), max(P)], pull_PACTLB=[min(L), max(L)], max_edge_shift_vs_D1433=shift)
out['verdict'] = 'D1433 SUPERSEDED' if shift > 0.1 else 'D1433 CONFIRMED'
json.dump(out, open('field_tests/results/D1452_box_derived_running.json', 'w'), indent=1)
print(out['verdict'], out['alpha_range'], out['pull_PACT'], out['pull_PACTLB'], shift)
