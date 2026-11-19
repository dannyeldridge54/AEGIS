"""JANUS tick 52: alpha_s window per vacuum conditioned on SO n_s +-0.002 (PREREG_D1456)."""
import json, numpy as np, mpmath as mp
G = {}; exec(open('field_tests/scripts/d1449/vac_grid.py').read().split("rows = []")[0], G)
R_, T_, solve = G['R_'], G['T_'], G['solve']; c = T_['c']
chains = {'rho': ([0.971663, 0.973232, 0.974828], [4.52911e-4, 4.70877e-4, 4.89722e-4], 0.974393),
          'tau_i': ([0.97368, 0.97415, 0.97462, 0.97509, 0.97556], [4.6846e-4, 4.7584e-4, 4.8335e-4, 4.9100e-4, 4.9878e-4], 0.97462)}
out = dict(D='D1456', vacua={})
for v, (ns, rr, c0) in chains.items():
    b, a = np.polyfit(ns, rr, 1); res = max(abs(np.polyval([b, a], ns)-rr)/rr)
    pts = []
    for dn in (-0.002, 0.0, 0.002):
        n = c0+dn; r = float(np.polyval([b, a], n))
        if v == 'rho': al, p, ok = solve(R_['obs'], (mp.mpf('1.2'), mp.log(mp.mpf('14.6'))/mp.sqrt(2)), mp.mpf('1e-6'), mp.mpf(n), mp.mpf(r))
        else: al, p, ok = solve(T_['obs'], (mp.mpf('1.4'), mp.log(mp.mpf('23.3')+c)/mp.sqrt(2)), mp.mpf('1e-4'), mp.mpf(n), mp.mpf(r))
        pts.append(dict(ns=n, r=r, alpha=al, param=p, converged=ok))
    w = [pts[0]['alpha'], pts[2]['alpha']]
    out['vacua'][v] = dict(slope_dr_dns=b, fit_max_rel_res=res, points=pts, window=[min(w), max(w)],
                           width_rel=abs(w[1]-w[0])/abs(pts[1]['alpha']))
    print(v, out['vacua'][v], flush=True)
W = [out['vacua'][k]['window'] for k in ('rho', 'tau_i')]
out['overlap'] = not (W[0][1] < W[1][0] or W[1][1] < W[0][0])
out['verdict'] = 'windows overlap' if out['overlap'] else 'windows separate'
json.dump(out, open('field_tests/results/D1456_so_conditioned.json', 'w'), indent=1); print(out['verdict'])
