"""JANUS tick 45: Delta alpha_s(rho - tau=i) with both derived second-order models on a 3x3 (n_s, r) grid (PREREG_D1449)."""
import json, mpmath as mp
R_ = {}; T_ = {}
exec(open('field_tests/scripts/d1442/second_order.py').read().split("NS,R,AEX")[0], R_)
exec(open('field_tests/scripts/d1448/tau_i_exact.py').read().split("PTS = ")[0], T_)
mp.mp.dps = 30
def solve(obs, g, scale, NS, R):
    F = lambda a, phi: (lambda o: [o[0]-NS, (o[1]-R)*1000])(obs(phi, a*scale))
    s = mp.findroot(F, g, tol=1e-18); o = obs(s[1], s[0]*scale)
    ok = abs(o[0]-NS) < 1e-10 and abs(o[1]/R-1) < 1e-8
    return float(o[2]), float(s[0]*scale), bool(ok)
rows = []
for ns in ('0.9725', '0.9740', '0.9755'):
    for r in ('4.6e-4', '4.75e-4', '4.9e-4'):
        NS, R = mp.mpf(ns), mp.mpf(r)
        try:
            ar, Cr, okr = solve(R_['obs'], (mp.mpf('1.2'), mp.log(mp.mpf('14.6'))/mp.sqrt(2)), mp.mpf('1e-6'), NS, R)
            at, et, okt = solve(T_['obs'], (mp.mpf('1.4'), mp.log(mp.mpf('23.3')+T_['c'])/mp.sqrt(2)), mp.mpf('1e-4'), NS, R)
            d = ar-at
            rows.append(dict(ns=float(NS), r=float(R), alpha_rho=ar, C_rho=Cr, alpha_tau=at, eps_tau=et, converged=okr and okt,
                             delta=d, sig_SO=abs(d)/3.3e-3, sig_best_hypo=abs(d)/8.5e-4, resolve_ratio=abs(d)/(0.0014*abs(ar))))
        except Exception as ex:
            rows.append(dict(ns=float(NS), r=float(R), converged=False, error=str(ex)[:80]))
        print(rows[-1], flush=True)
ok = [x for x in rows if x.get('converged')]
out = dict(D='D1449', rows=rows, n_converged=len(ok), max_sig_SO=max(x['sig_SO'] for x in ok), max_sig_best_hypo=max(x['sig_best_hypo'] for x in ok),
           delta_range=[min(x['delta'] for x in ok), max(x['delta'] for x in ok)])
out['verdict'] = 'stays killed' if out['max_sig_SO'] < 3 else 'REVIVE candidate'
json.dump(out, open('field_tests/results/D1449_vac_derived.json', 'w'), indent=1); print(out['verdict'], out['max_sig_SO'], out['max_sig_best_hypo'], out['delta_range'])
