"""D2244 (PREREG_D2244_NT_MODE): negative-triangularity mode, full reactor redo; D2243 engine + NT rule changes."""
import json, random
from multiprocessing import Pool
SRC = open('theory/tests/d2243_steady.py').read().split("if __name__ == '__main__':")[0]
assert "m = machine(R, B); m['line_model'] = 'adas';" in open('theory/tests/d2241_enrichment.py').read()
G = {'__name__': 'd2244'}; exec(SRC, G)                      # builds G['G'] (patched engine) with D2243 deviations
ENG = G['G']; H = {'H98': 1.0}
ENG['machine0'] = ENG['machine']
def machine_h(R, B):
    m = ENG['machine0'](R, B); m['H98'] = H['H98']; return m
ENG['machine'] = machine_h
LAD = dict(R=[6.2, 7.0, 8.0, 9.0], B=[5.3, 6.0, 7.0, 8.0, 9.0], fAr=[0.0014, 0.003, 0.005, 0.008], leg=[1, 2, 3, 4, 5],
           blk=[2], Paux=[10.0, 20.0, 30.0, 50.0], dens=[0.9], nu=[0.4, 0.5, 0.6], enr=[3, 5, 10])
KEYS = list(LAD)
def ev(p):
    e = ENG['evaluate'](*p, 20.0)
    out = dict(point=dict(zip(KEYS, p)), P_net=e.get('P_net'), P_fus=e.get('P_fus'), Q_e=e.get('Q_e'), c_SOL=e.get('c_SOL'))
    if 'raw' not in e: out['burn'] = False; return out
    raw = dict(e['raw']); B, R = p[1], p[0]; E2 = e['Psep'] * B / (3.0 * e['A'] * R)
    base = {k: x for k, x in raw.items() if k not in ('LH', 'coil') and x > 0}
    if e['Psep_R'] > 17.0: base['PsepR'] = e['Psep_R'] / 17.0 - 1
    if e['Psep'] < 1.0: base['Psep_low'] = 1.0
    betaN = (raw['betaN'] + 1) * 2.8
    out.update(burn=True, Psep=e['Psep'], Psep_R=e['Psep_R'], E2=E2, betaN=betaN, wall=e['wall'], coil=e['coil'], TBR=e['TBR'],
               synch_frac=e['P_synch'] / e['P_alpha'], f_LH=e['lh_ratio'])
    for cls, cm in (('Nb3Sn', 12.0), ('HTS', 20.0)):
        b = sorted(base) + (['coil'] if e['coil'] > cm else [])
        out[f'{cls}|main'] = b
        out[f'{cls}|beta25'] = b + (['betaN25'] if betaN > 2.5 else [])
        out[f'{cls}|E2'] = b + (['E2'] if E2 > 9.2 else [])
    return out
if __name__ == '__main__':
    c = ENG['evaluate'](9.0, 9.0, 0.003, 2, 2, 10.0, 0.85, 0.4, 10, 20.0)
    ctl_lh = c['lh_ratio'] < 1.2; print('CONTROL (D2243 rule fails L-H):', ctl_lh, round(c['lh_ratio'], 3), flush=True)
    grid = [tuple(v) for v in __import__('itertools').product(*[LAD[k] for k in KEYS])]
    rng = random.Random(2244); pts = rng.sample(grid, 2500)
    allres = {}; summ = {}
    for h in (1.0, 0.8):
        H['H98'] = h; ENG['evaluate'].cache_clear()
        with Pool(2) as pool: res = pool.map(ev, pts, chunksize=50)
        allres[str(h)] = res; burn = [r for r in res if r.get('burn')]
        print(f'== H98 {h}: burning {len(burn)} of {len(res)}', flush=True)
        for cls in ('Nb3Sn', 'HTS'):
            for rs in ('main', 'beta25', 'E2'):
                k = f'{cls}|{rs}'; feas = [r for r in burn if not r[k]]
                best = max(feas, key=lambda r: r['P_net']) if feas else None
                near = sorted(burn, key=lambda r: (len(r[k]), -(r['P_net'] or -1e9)))[:3]
                summ[f'{h}|{k}'] = dict(n_feasible=len(feas), n_eta3=sum(r['point']['enr'] == 3 for r in feas),
                                        min_eta=min([r['point']['enr'] for r in feas], default=None), best=best,
                                        nearest=[(r['point'], r[k], round(r['P_net'] or 0, 1)) for r in near])
                print(k, 'feasible', len(feas), 'eta3', summ[f'{h}|{k}']['n_eta3'], 'best',
                      best and (best['point'], round(best['P_net'], 1), round(best['P_fus'], 1), round(best['Q_e'], 2), round(best['betaN'], 2), round(best['synch_frac'], 2)),
                      '| nearest', summ[f'{h}|{k}']['nearest'][0][1:], flush=True)
    json.dump(dict(control=dict(fails_LH=ctl_lh, f_LH=c['lh_ratio']), summary=summ, samples=allres), open('field_tests/results/d2244_nt.json', 'w'), default=float)
