"""D2243 (PREREG_D2243_STEADY_PASS): global random search over the D2241 engine, feasibility under four rule sets."""
import json, random, sys, math
from multiprocessing import Pool
SRC = open('theory/tests/d2241_enrichment.py').read().split("import copy\nLAD0")[0]
OLD = "return dict(score=pl['P_net'] if not viol else -sum(viol.values()) - 1, feasible=not viol,"
assert OLD in SRC and "LH=1.3 * op['P_LH'] / op['P_loss'] - 1" in SRC
SRC = SRC.replace(OLD, "return dict(lh_ratio=Psep / op['P_LH'], P_LH=op['P_LH'], P_synch=op['P_synch'], P_alpha=op['P_alpha'], Psep=Psep, A=m['R'] / m['a'], raw=v, " + OLD[len('return dict('):])
G0 = {'__name__': 'd2243c'}; exec(SRC, G0)
assert SRC.count('for it in range(2):') == 1
SRC = SRC.replace('for it in range(2):', 'for it in range(5):')
G = {'__name__': 'd2243'}; exec(SRC, G)
LAD = dict(R=[6.2, 7.0, 8.0, 9.0], B=[5.3, 6.0, 7.0, 8.0, 9.0], fAr=[0.0014, 0.003, 0.005, 0.008], leg=[1, 2, 3, 4, 5],
           blk=[2], Paux=[10.0, 20.0, 30.0, 50.0], dens=[0.7, 0.8, 0.85, 0.9], nu=[0.4, 0.5, 0.6], enr=[3, 5, 10])
KEYS = list(LAD)
def ev(p):
    e = G['evaluate'](*p, 20.0)
    out = dict(point=dict(zip(KEYS, p)), P_net=e.get('P_net'), P_fus=e.get('P_fus'), c_SOL=e.get('c_SOL'))
    if 'raw' not in e: out['burn'] = False; return out
    raw = dict(e['raw']); lhr = e['lh_ratio']; B, R = p[1], p[0]
    E2 = e['Psep'] * B / (3.0 * e['A'] * R); out.update(burn=True, lh_ratio=lhr, E2=E2, coil=e['coil'], Psep_R=e['Psep_R'])
    base = {k: x for k, x in raw.items() if k not in ('LH', 'coil') and x > 0}
    if e['Psep_R'] > 17.0: base['PsepR'] = e['Psep_R'] / 17.0 - 1
    if e['Psep'] < 1.0: base['Psep_low'] = 1.0
    out.update(synch_frac=e['P_synch'] / e['P_alpha'], Psep=e['Psep'])
    for cls, cm in (('Nb3Sn', 12.0), ('HTS', 20.0)):
        b = dict(base); 
        if e['coil'] > cm: b['coil'] = e['coil'] / cm - 1
        for rs, lhm, e2 in (('R13', 1.3, False), ('R12', 1.2, False), ('R13E', 1.3, True), ('R12E', 1.2, True)):
            v = sorted(b) + (['LH'] if lhr < lhm else []) + (['E2'] if e2 and E2 > 9.2 else [])
            out[f'{cls}|{rs}'] = v
    return out
if __name__ == '__main__':
    ctl = G0['evaluate'](9.0, 9.0, 0.003, 2, 1, 10.0, 0.85, 0.4, 10, 20.0)
    print('CONTROL', round(ctl['P_net'], 1), ctl['violations'], flush=True)
    rng = random.Random(2243); pts = list({tuple(rng.choice(LAD[k]) for k in KEYS) for _ in range(5200)})[:5000]
    pts.sort()
    with Pool(2) as pool: res = pool.map(ev, pts, chunksize=50)
    summ = {}
    for cls in ('Nb3Sn', 'HTS'):
        for rs in ('R13', 'R12', 'R13E', 'R12E'):
            k = f'{cls}|{rs}'; feas = [r for r in res if r.get('burn') and not r[k]]
            best = max(feas, key=lambda r: r['P_net']) if feas else None
            eta3 = [r for r in feas if r['point']['enr'] == 3]
            near = sorted([r for r in res if r.get('burn')], key=lambda r: (len(r[k]), -(r['P_net'] or -1e9)))[:3]
            summ[k] = dict(n_feasible=len(feas), n_feasible_eta3=len(eta3), min_eta=min([r['point']['enr'] for r in feas], default=None),
                           best=best, nearest=[(r['point'], r[k], round(r['P_net'], 1)) for r in near])
            print(k, 'feasible', len(feas), 'eta3', len(eta3), 'best', best and (best['point'], round(best['P_net'], 1)), flush=True)
    print('burning samples', sum(1 for r in res if r.get('burn')), 'of', len(res))
    json.dump(dict(control=dict(P_net=ctl['P_net'], violations=ctl['violations']), summary=summ, samples=res),
              open('field_tests/results/d2243_steady.json', 'w'), default=float)
