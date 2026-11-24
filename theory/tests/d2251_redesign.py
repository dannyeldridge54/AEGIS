"""D2251 (PREREG_D2251_REACTOR_REDESIGN): long NT redesign search over the exhaust / core-radiation squeeze."""
import json, random, itertools, sys, math
from multiprocessing import Pool
SRC = open('theory/tests/d2244_nt.py').read(); SRC = SRC[:SRC.rindex("if __name__ == '__main__':")]
G = {'__name__': 'd2251'}; exec(SRC, G)
ENG, H = G['ENG'], G['H']; H['H98'] = 1.0; H['refl'] = 0.6
_m_nt = ENG['machine']
def machine_r(R, B):
    m = _m_nt(R, B); m['f_reflect'] = H['refl']; return m
ENG['machine'] = machine_r
LAD = dict(R=[5.0, 6.0, 7.0, 8.0, 9.0], B=[4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0], fAr=[0.0005, 0.001, 0.0014, 0.002, 0.003, 0.005],
           leg=[1, 2, 3, 4, 5], blk=[2], Paux=[10.0, 20.0, 30.0, 50.0], dens=[0.9], nu=[0.4, 0.5, 0.6], enr=[3, 5, 10])
KEYS = list(LAD)
def ev(p):
    try:
        e = ENG['evaluate'](*p, 20.0)
    except Exception as ex:
        return dict(point=dict(zip(KEYS, p)), burn=False, err=str(ex)[:80])
    out = dict(point=dict(zip(KEYS, p)), P_net=e.get('P_net'), P_fus=e.get('P_fus'), Q_e=e.get('Q_e'), c_SOL=e.get('c_SOL'))
    if 'raw' not in e:
        out['burn'] = False; return out
    raw = dict(e['raw']); heat = e['P_alpha'] + p[KEYS.index('Paux')]
    frad = 1 - e['Psep'] / heat
    viol = {k: x for k, x in raw.items() if k not in ('LH', 'coil') and x > 0}
    if e['Psep_R'] > 17.0: viol['PsepR'] = e['Psep_R'] / 17.0 - 1
    if e['Psep'] < 1.0: viol['Psep_low'] = (1.0 - e['Psep']) / 10 + 0.1
    if e['coil'] > 20.0: viol['coil'] = e['coil'] / 20.0 - 1
    if e['P_net'] <= 0: viol['P_net'] = -e['P_net'] / 100 + 0.1
    v60 = dict(viol); v67 = dict(viol)
    if frad > 0.60: v60['f_rad'] = frad / 0.60 - 1
    if frad > 0.67: v67['f_rad'] = frad / 0.67 - 1
    out.update(burn=True, Psep=e['Psep'], Psep_R=e['Psep_R'], f_rad=frad, wall=e['wall'], coil=e['coil'], TBR=e['TBR'],
               betaN=(raw['betaN'] + 1) * 2.8, synch_frac=e['P_synch'] / e['P_alpha'], viol60=v60, viol67=v67,
               nb3sn_ok=e['coil'] <= 12.0)
    return out
def score(r, key='viol60'):
    if not r.get('burn'): return -100.0
    v = r[key]
    return r['P_net'] if not v else -sum(v.values())
def polish(args):
    start, refl, key = args
    H['refl'] = refl; ENG['evaluate'].cache_clear()
    cur = dict(start); best = ev(tuple(cur[k] for k in KEYS)); path = [(dict(cur), score(best, key))]
    for sweep in range(12):
        changed = False
        for k in KEYS:
            if len(LAD[k]) < 2: continue
            i = LAD[k].index(cur[k])
            for j in (i - 1, i + 1):
                if 0 <= j < len(LAD[k]):
                    t = dict(cur, **{k: LAD[k][j]}); r = ev(tuple(t[q] for q in KEYS))
                    if score(r, key) > score(best, key) + 1e-9: cur, best, changed = t, r, True
        path.append((dict(cur), score(best, key)))
        if not changed: break
    return dict(start=start, end=cur, result=best, sweeps=len(path) - 1, refl=refl, key=key)
def init(refl):
    H['refl'] = refl
if __name__ == '__main__':
    H['refl'] = 0.6
    c = ENG['evaluate'](7.0, 9.0, 0.008, 3, 2, 50.0, 0.9, 0.6, 3, 20.0)
    heat = c['P_alpha'] + 50.0; print('CONTROL P_net %.1f f_rad %.3f' % (c['P_net'], 1 - c['Psep'] / heat), flush=True)
    grid = list(itertools.product(*[LAD[k] for k in KEYS]))
    rng = random.Random(2251); pts = rng.sample(grid, 6000)
    allres, summary, pol = {}, {}, {}
    for refl in (0.6, 0.8):
        with Pool(2, initializer=init, initargs=(refl,)) as pool:
            res = pool.map(ev, pts, chunksize=40)
        burn = [r for r in res if r.get('burn')]
        print(f'== f_reflect {refl}: burning {len(burn)} of {len(res)}', flush=True)
        for key in ('viol60', 'viol67'):
            feas = [r for r in burn if not r[key]]
            print(f'  {key}: feasible {len(feas)}', 'best', feas and max(feas, key=lambda r: r['P_net'])['point'], flush=True)
        starts = [r['point'] for r in sorted(burn, key=lambda r: -score(r, 'viol60'))[:15]]
        with Pool(2, initializer=init, initargs=(refl,)) as pool:
            pr = pool.map(polish, [(s, refl, 'viol60') for s in starts])
        pol[str(refl)] = pr
        for p in sorted(pr, key=lambda p: -score(p['result'], 'viol60'))[:5]:
            r = p['result']
            print('  polish ->', p['end'], 'score %.3f' % score(r, 'viol60'), 'P_net', r.get('P_net') and round(r['P_net']), 'f_rad', r.get('f_rad') and round(r['f_rad'], 3),
                  'PsepR', r.get('Psep_R') and round(r['Psep_R'], 1), 'viol60', {k: round(v, 3) for k, v in (r.get('viol60') or {}).items()}, flush=True)
        allres[str(refl)] = res
        summary[str(refl)] = dict(burning=len(burn), feasible60=sum(1 for r in burn if not r['viol60']), feasible67=sum(1 for r in burn if not r['viol67']))
    json.dump(dict(control=dict(P_net=c['P_net'], f_rad=1 - c['Psep'] / heat), summary=summary, polish=pol, samples=allres),
              open('field_tests/results/d2251_redesign.json', 'w'), default=float)
    print('DONE', summary)
