"""D2255 (PREREG_D2255_LEVER_MAP): exhaustive lever map, H98 x P_sep/R limit, on the D2251 engine."""
import json, itertools
from multiprocessing import get_context
SRC = open('theory/tests/d2251_redesign.py').read(); SRC = SRC[:SRC.rindex("if __name__ == '__main__':")]
G = {'__name__': 'd2255'}; exec(SRC, G)
ENG, H = G['ENG'], G['H']
LAD = dict(R=[6.0, 7.0, 8.0, 9.0], B=[5.0, 6.0, 7.0, 8.0, 9.0], fAr=[0.0005, 0.001, 0.002, 0.003, 0.005], leg=[3, 5], blk=[2],
           Paux=[10.0, 30.0, 50.0], dens=[0.9], nu=[0.6], enr=[3, 10])
KEYS = list(LAD)
def ev(a):
    p, h98 = a
    H['H98'] = h98; H['refl'] = 0.6
    try:
        e = ENG['evaluate'](*p, 20.0)
    except Exception as ex:
        return dict(point=dict(zip(KEYS, p)), H98=h98, burn=False, err=str(ex)[:80])
    out = dict(point=dict(zip(KEYS, p)), H98=h98, P_net=e.get('P_net'), P_fus=e.get('P_fus'))
    if 'raw' not in e: out['burn'] = False; return out
    raw = dict(e['raw']); heat = e['P_alpha'] + p[KEYS.index('Paux')]; frad = 1 - e['Psep'] / heat
    base = sorted(k for k, x in raw.items() if k not in ('LH', 'coil') and x > 0)
    if e['Psep'] < 1.0: base.append('Psep_low')
    if e['coil'] > 20.0: base.append('coil')
    if e['P_net'] <= 0: base.append('P_net')
    out.update(burn=True, base=base, Psep_R=e['Psep_R'], f_rad=frad, wall=e['wall'], coil=e['coil'], TBR=e['TBR'], Q_e=e.get('Q_e'))
    return out
def feasible(r, lim, cap):
    return r.get('burn') and not r['base'] and r['Psep_R'] <= lim and r['f_rad'] <= cap
if __name__ == '__main__':
    grid = list(itertools.product(*[LAD[k] for k in KEYS])); res = []
    for h98 in (1.0, 1.2, 1.4):
        with get_context('fork').Pool(2, maxtasksperchild=200) as pool:
            r = pool.map(ev, [(p, h98) for p in grid], chunksize=20)
        res += r
        b = [x for x in r if x.get('burn')]
        print(f'H98 {h98}: burning {len(b)} of {len(r)}; errors {sum(1 for x in r if x.get("err"))}', flush=True)
    c = [x for x in res if x['H98'] == 1.0 and x['point'] == dict(R=9.0, B=9.0, fAr=0.005, leg=3, blk=2, Paux=10.0, dens=0.9, nu=0.6, enr=10)]
    print('CONTROL R9 B9 Ar0.5% Paux10 (H98 1.0):', c and {k: c[0].get(k) for k in ('burn', 'P_net', 'f_rad', 'Psep_R', 'base')}, flush=True)
    table = {}
    for cap in (0.85, 0.67):
        print(f'== core radiation cap {cap}')
        for h98 in (1.0, 1.2, 1.4):
            row = []
            for lim in (17, 25, 35):
                F = [x for x in res if x['H98'] == h98 and feasible(x, lim, cap)]
                best = max(F, key=lambda x: x['P_net']) if F else None
                table[f'cap{cap}|H98{h98}|lim{lim}'] = dict(n=len(F), eta3=sum(1 for x in F if x['point']['enr'] == 3), best=best)
                row.append(f'lim {lim}: {len(F):3d} ({sum(1 for x in F if x["point"]["enr"] == 3)} at eta3)' + (f' best {round(best["P_net"])} MW R{best["point"]["R"]} B{best["point"]["B"]} Ar{best["point"]["fAr"]} f_rad {best["f_rad"]:.2f} PsepR {best["Psep_R"]:.1f}' if best else ''))
            print(f'  H98 {h98}: ' + ' | '.join(row), flush=True)
    json.dump(dict(table=table, results=res), open('field_tests/results/d2255_levers.json', 'w'), default=float)
    print('DONE')
