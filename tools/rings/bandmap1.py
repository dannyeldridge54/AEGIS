import itertools, json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hex as H
B = H.B
def marks(E):
    m = {}
    for t in E['terms']:
        if t.get('ours') is None: continue
        k = t['kind']; o = t['ours']
        if k == 'gauss': p = (o - t['mu']) / t['sigma']; m[t['id']] = ('IN' if abs(p) <= 1 else 'EDGE' if abs(p) <= 2 else 'OUT', round(p, 2))
        elif k == 'upper': m[t['id']] = ('IN' if o <= t['bound'] else 'OUT', o)
        elif k == 'lower': m[t['id']] = ('IN' if o >= t['bound'] else 'OUT', o)
        elif k == 'band': m[t['id']] = ('IN' if t['lo'] <= o <= t['hi'] else 'OUT', o)
    L = E['local']['N1 nuclear']
    for nm in ('pull_Yp', 'pull_DH'):
        p = L[nm]; m[nm[5:]] = ('IN' if abs(p) <= 1 else 'EDGE' if abs(p) <= 2 else 'OUT', round(p, 2))
    m['Hoyle'] = ('IN' if E['bus'].get('hoyle_inside') else 'OUT', round(E['bus'].get('hoyle_radius'), 3))
    m['genesis'] = ('IN' if E['bus'].get('genesis_viable') else 'OUT', None)
    return m
if __name__ == '__main__':
    t0 = time.perf_counter(); rows = []
    S = [0.3 * 10 ** (i / 8) for i in range(9)]; Cs = [1.0e-6 + 0.1e-6 * i for i in range(7)]; Ts = [1e8 * 50 ** (i / 4) for i in range(5)]
    for C, T, s in itertools.product(Cs, Ts, S):
        k = dict(C=float(f'{C:.4e}'), T_R=float(f'{T:.4e}'), s_m32=round(s, 4))
        try: E = H.evaluate(k)
        except Exception as e: rows.append(dict(knobs=k, error=str(e)[:80])); continue
        rows.append(dict(knobs=k, target=E['target'], marks=marks(E)))
    ok = [r for r in rows if 'marks' in r]; nodes = sorted({n for r in ok for n in r['marks']})
    frac = {n: sum(r['marks'][n][0] == 'IN' for r in ok) / len(ok) for n in nodes}
    allin = [r for r in ok if all(v[0] in ('IN', 'EDGE') for v in r['marks'].values())]
    nout = lambda r: sum(v[0] == 'OUT' for v in r['marks'].values())
    best = min(ok, key=lambda r: (nout(r), -r['target']))
    outs = {n: sum(r['marks'][n][0] == 'OUT' for r in ok) for n in nodes}
    res = dict(points=len(rows), errors=len(rows) - len(ok), in_fraction=frac, out_count=outs, all_in_or_edge=len(allin), best=best, seconds=time.perf_counter() - t0)
    json.dump(dict(res, rows=rows), open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'bandmap1.json'), 'w'), indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))
