"""JANUS tick 49: derived tau=i model over band_i vs D1413 (PREREG_D1453)."""
import json, mpmath as mp
G = {}; exec(open('field_tests/scripts/d1449/vac_grid.py').read().split("rows = []")[0], G)
T_, solve = G['T_'], G['solve']; c = T_['c']
rows = []
for ns in ('0.970', '0.9725', '0.975'):
    for r in ('4.8e-4', '5.25e-4', '5.7e-4'):
        try:
            a, e, ok = solve(T_['obs'], (mp.mpf('1.4'), mp.log(mp.mpf('23.3')+c)/mp.sqrt(2)), mp.mpf('1e-4'), mp.mpf(ns), mp.mpf(r))
            rows.append(dict(ns=float(ns), r=float(r), alpha=a, eps=e, converged=ok, pull_PACT=(a-0.0060)/0.0055, pull_PACTLB=(a-0.0062)/0.0052))
        except Exception as ex:
            rows.append(dict(ns=float(ns), r=float(r), converged=False, error=str(ex)[:80]))
        print(rows[-1], flush=True)
ok = [x for x in rows if x.get('converged')]
A = [x['alpha'] for x in ok]; d13 = [-0.001044288652928553, -0.0008416546830411823]
mv = [min(A)/d13[0]-1, max(A)/d13[1]-1]
out = dict(D='D1453', rows=rows, n_converged=len(ok), alpha_range=[min(A), max(A)], eps_range=[min(x['eps'] for x in ok), max(x['eps'] for x in ok)],
           pull_PACT=[min(x['pull_PACT'] for x in ok), max(x['pull_PACT'] for x in ok)],
           pull_PACTLB=[min(x['pull_PACTLB'] for x in ok), max(x['pull_PACTLB'] for x in ok)], edge_moves_vs_D1413=mv)
out['verdict'] = 'D1413 SUPERSEDED' if max(abs(v) for v in mv) > 0.005 else 'D1413 CONFIRMED'
json.dump(out, open('field_tests/results/D1453_band_i_derived.json', 'w'), indent=1); print(out['verdict'], out['n_converged'])
