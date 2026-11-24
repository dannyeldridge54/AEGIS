"""D2251b (DEVIATIONS DEV-1..7): re-score run-1 samples at f_rad caps 0.60/0.67/0.85, per (eta, cap, f_reflect); polish with the
0.67 and 0.85 keys; sensitivities (kappa 1.6; synchrotron x1.3) on the most-ready designs. Physics and samples unchanged."""
import json, math, sys
from multiprocessing import Pool
SRC = open('theory/tests/d2251_redesign.py').read(); SRC = SRC[:SRC.rindex("if __name__ == '__main__':")]
G = {'__name__': 'd2251b'}; exec(SRC, G)
ENG, H, ev, LAD, KEYS = G['ENG'], G['H'], G['ev'], G['LAD'], G['KEYS']
CAPS = (0.60, 0.67, 0.85)
def viol(r, cap):
    if not r.get('burn'): return None
    v = {k: x for k, x in r['viol60'].items() if k != 'f_rad'}
    if r['f_rad'] > cap: v['f_rad'] = r['f_rad'] / cap - 1
    return v
def sc(r, cap):
    v = viol(r, cap)
    if v is None: return -100.0
    return r['P_net'] if not v else -sum(v.values())
def polish(args):
    start, refl, cap = args
    H['refl'] = refl; ENG['evaluate'].cache_clear()
    cur = dict(start); best = ev(tuple(cur[k] for k in KEYS))
    for sweep in range(12):
        changed = False
        for k in KEYS:
            if len(LAD[k]) < 2: continue
            i = LAD[k].index(cur[k])
            for j in (i - 1, i + 1):
                if 0 <= j < len(LAD[k]):
                    t = dict(cur, **{k: LAD[k][j]}); r = ev(tuple(t[q] for q in KEYS))
                    if sc(r, cap) > sc(best, cap) + 1e-9: cur, best, changed = t, r, True
        if not changed: break
    return dict(start=start, end=cur, result=best, refl=refl, cap=cap)
def sens(args):
    point, refl, mode = args
    H['refl'] = refl; ENG['evaluate'].cache_clear()
    base_m = G['machine_r']
    if mode == 'kappa1.6':
        def mk(R, B):
            m = base_m(R, B); k0 = m['kappa']; f = (1 + 1.6 ** 2) / (1 + k0 ** 2)
            m.update(kappa=1.6, Ip=m['Ip'] * f, V=m['V'] * 1.6 / k0, S=m['S'] * math.sqrt(f)); return m
        ENG['machine'] = mk
    elif mode == 'synch1.3':
        F = ENG['X'].F; p0 = F.p_synch; F.p_synch = lambda m, n, T: 1.3 * p0(m, n, T)
    return dict(point=point, refl=refl, mode=mode, result=ev(tuple(point[k] for k in KEYS)))
if __name__ == '__main__':
    d = json.load(open('field_tests/results/d2251_redesign.json'))
    out = dict(counts={}, errors={}, polish=[], sens=[])
    for refl, S in d['samples'].items():
        out['errors'][refl] = sum(1 for r in S if r.get('err'))
        burn = [r for r in S if r.get('burn')]
        for cap in CAPS:
            for eta in (3, 5, 10):
                feas = [r for r in burn if r['point']['enr'] == eta and not viol(r, cap)]
                out['counts'][f'refl{refl}|cap{cap}|eta{eta}'] = len(feas)
        print('f_reflect', refl, 'burning', len(burn), 'of', len(S), 'engine errors', out['errors'][refl],
              {k: v for k, v in out['counts'].items() if k.startswith(f'refl{refl}')}, flush=True)
    jobs = []
    for refl, S in d['samples'].items():
        burn = [r for r in S if r.get('burn')]
        for cap in (0.67, 0.85):
            jobs += [(r['point'], float(refl), cap) for r in sorted(burn, key=lambda r: -sc(r, cap))[:10]]
    with Pool(2) as pool: pol = pool.map(polish, jobs)
    for p in pol:
        r = p['result']; v = viol(r, p['cap']) if r.get('burn') else None
        p['n_viol'] = None if v is None else len(v)
    out['polish'] = pol
    for refl in (0.6, 0.8):
        for cap in (0.60, 0.67, 0.85):
            cand = [p for p in pol if p['refl'] == refl and p['cap'] == cap] + [dict(end=q['end'], result=q['result'], refl=refl, cap=0.60) for q in d['polish'][str(refl)]] if cap == 0.60 else [p for p in pol if p['refl'] == refl and p['cap'] == cap]
            cand = sorted(cand, key=lambda p: -sc(p['result'], cap))
            if not cand: continue
            b = cand[0]; r = b['result']; v = viol(r, cap)
            print(f'refl {refl} cap {cap}: most-ready', b['end'], 'P_net', r.get('P_net') and round(r['P_net']), 'P_fus', r.get('P_fus') and round(r['P_fus']),
                  'f_rad', r.get('f_rad') and round(r['f_rad'], 3), 'PsepR', r.get('Psep_R') and round(r['Psep_R'], 1), 'wall', r.get('wall') and round(r['wall'], 2),
                  'coil', r.get('coil') and round(r['coil'], 1), 'n_viol', None if v is None else len(v), 'viol', v and {k: round(x, 3) for k, x in v.items()}, flush=True)
    tops = []
    for refl in (0.6, 0.8):
        for cap in (0.67, 0.85):
            c = sorted([p for p in pol if p['refl'] == refl and p['cap'] == cap], key=lambda p: -sc(p['result'], cap))[:2]
            tops += [(p['end'], refl, cap) for p in c]
    sj = [(pt, refl, mode) for pt, refl, cap in tops for mode in ('kappa1.6', 'synch1.3')]
    with Pool(2) as pool: sres = pool.map(sens, sj)
    for (pt, refl, cap), i in zip(tops, range(0, len(sres), 2)):
        for s in sres[i:i + 2]:
            r = s['result']; v = viol(r, cap)
            print(f'  sens {s["mode"]} refl {refl} cap {cap}:', pt, 'P_net', r.get('P_net') and round(r['P_net']), 'f_rad', r.get('f_rad') and round(r['f_rad'], 3),
                  'PsepR', r.get('Psep_R') and round(r['Psep_R'], 1), 'feasible', v is not None and not v, 'viol', v and {k: round(x, 3) for k, x in v.items()}, flush=True)
    out['sens'] = sres
    json.dump(out, open('field_tests/results/d2251b_rescore.json', 'w'), default=float)
    print('DONE')
