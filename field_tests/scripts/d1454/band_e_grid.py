"""JANUS tick 50: derived rho model over band_e vs D1421 / D693 (PREREG_D1454)."""
import json, mpmath as mp
G = {}; exec(open('field_tests/scripts/d1449/vac_grid.py').read().split("rows = []")[0], G)
R_, solve = G['R_'], G['solve']
rows = []
for ns in ('0.969', '0.972', '0.975'):
    for r in ('4.55e-4', '4.835e-4', '5.12e-4'):
        try:
            a, C, ok = solve(R_['obs'], (mp.mpf('1.2'), mp.log(mp.mpf('14.6'))/mp.sqrt(2)), mp.mpf('1e-6'), mp.mpf(ns), mp.mpf(r))
            rows.append(dict(ns=float(ns), r=float(r), alpha=a, C=C, converged=ok, pull_PACT=(a-0.0060)/0.0055, pull_PACTLB=(a-0.0062)/0.0052))
        except Exception as ex:
            rows.append(dict(ns=float(ns), r=float(r), converged=False, error=str(ex)[:80]))
        print(rows[-1], flush=True)
ok = [x for x in rows if x.get('converged')]
A = [x['alpha'] for x in ok]; d21 = [-0.0009420238528340553, -0.0010600356322000798]
mv = [max(A)/d21[0]-1, min(A)/d21[1]-1]
spread = {}
for r in sorted(set(x['r'] for x in ok)):
    s = [x['alpha'] for x in ok if x['r'] == r]; spread[str(r)] = (max(s)-min(s))/abs(sum(s)/len(s))
inside = min(A) >= -0.00106-0.00002 and max(A) <= -0.00094+0.00002
pulls = [x['pull_PACT'] for x in ok]+[x['pull_PACTLB'] for x in ok]
out = dict(D='D1454', rows=rows, n_converged=len(ok), alpha_range=[max(A), min(A)], edge_moves_vs_D1421=mv, ns_spread_rel_at_r=spread,
           inside_D693_window_pm2e5=inside, pull_PACT=[min(x['pull_PACT'] for x in ok), max(x['pull_PACT'] for x in ok)],
           pull_PACTLB=[min(x['pull_PACTLB'] for x in ok), max(x['pull_PACTLB'] for x in ok)], act_pass=all(abs(p) < 2 for p in pulls))
out['verdict'] = 'D1421 SUPERSEDED' if max(abs(v) for v in mv) > 0.005 else 'D1421 CONFIRMED'
json.dump(out, open('field_tests/results/D1454_band_e_derived.json', 'w'), indent=1); print(out['verdict'], out['n_converged'])
