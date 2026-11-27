"""D2284: string threshold inputs for the Ring Engine (see PREREG_D2284).
Btilde = sum_j Ehat_j (b'_3 - 12/7 b'_2 + 5/7 b'_1) moves alpha_s; Dtilde = sum_j Ehat_j (b'_1 - b'_2) moves M12 and the proton lifetime."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rings as R
import bloom as B
def apply(terms, Btilde=0.0, Dtilde=0.0):
    d_inv_as = Btilde / (4 * math.pi); dlnM = -2 * math.pi * (Dtilde / (4 * math.pi)) / (28 / 5)
    out = []
    for t in terms:
        if t['id'] == 'alpha_s': t = dict(t, ours=1 / (1 / t['ours'] + d_inv_as))
        elif t['id'] == 'proton': t = dict(t, ours=t['ours'] * math.exp(4 * dlnM))
        out.append(t)
    return out
def pull(t): return B.lnL_term(t)[1]
def evaluate(Btilde=0.0, Dtilde=0.0, s_m32=1.0):
    P = R.one_pass(s_m32=s_m32); T = apply(P['terms'], Btilde, Dtilde); kfit = sum(k['n'] for k in B.D['fitted_knobs'])
    lnL = B.target(T, kfit)[0]; get = {t['id']: t for t in T}
    return dict(lnL=lnL, alpha_s=get['alpha_s']['ours'], pull_as=pull(get['alpha_s']), proton=get['proton']['ours'], pull_p=pull(get['proton']),
                wino=get['wino']['ours'], pull_w=pull(get['wino']))
if __name__ == '__main__':
    base = evaluate(0, 0); out = dict(base=base)
    grid = [x / 100 for x in range(-1000, 201)]
    rows = [(b, evaluate(b, 0)) for b in grid]
    for k in (1, 2):
        ok = [b for b, r in rows if abs(r['pull_as']) <= k]; out[f'Btilde_within_{k}sigma'] = [min(ok), max(ok)] if ok else None
    best = min(rows, key=lambda r: abs(r[1]['pull_as'])); out['Btilde_centre'] = best[0]; out['at_centre'] = best[1]
    drows = [(d, evaluate(best[0], d)) for d in [x / 10 for x in range(-200, 201)]]
    okp = [d for d, r in drows if r['pull_p'] <= 1e-9 or r['proton'] >= 2.4]; out['Dtilde_proton_allowed'] = [min(okp), max(okp)] if okp else None
    c = best[1]; out['conflict_check'] = 'PASS' if abs(c['pull_as']) <= 1 and abs(c['pull_w']) <= 1 else 'FAIL'
    out['dlnL_vs_none'] = c['lnL'] - base['lnL']
    json.dump(out, open(os.path.join(R.AEGIS, 'field_tests', 'results', 'd2284_threshold_target.json'), 'w'), indent=1, default=float)
    print(json.dumps(out, indent=1, default=float))
