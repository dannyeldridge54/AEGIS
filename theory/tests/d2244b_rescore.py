"""D2244 rescore after DEVIATIONS (R112): f_rad,core <= 0.6 cap, P_net > 0, dedupe."""
import json
d = json.load(open('field_tests/results/d2244_nt.json')); out = {}
for h, S in d['samples'].items():
    burn = [r for r in S if r.get('burn')]
    for r in burn:
        Pa = r['P_fus'] * 3.52 / 17.59; r['f_rad_core'] = 1 - r['Psep'] / (Pa + r['point']['Paux'])
    for cls in ('Nb3Sn', 'HTS'):
        for cap in (False, True):
            feas = [r for r in burn if not r[f'{cls}|main'] and r['P_net'] > 0 and (not cap or r['f_rad_core'] <= 0.6)]
            distinct = {}
            for r in feas:
                p = r['point']; distinct.setdefault((p['R'], p['B'], p['fAr'], p['Paux']), r)
            key = f'H98={h}|{cls}|{"capped" if cap else "uncapped"}'
            best = max(feas, key=lambda r: r['P_net']) if feas else None
            min_frad = min((r['f_rad_core'] for r in burn if not r[f'{cls}|main'] and r['P_net'] > 0), default=None)
            out[key] = dict(burning=f'{len(burn)}/{len(S)}', n_feasible=len(feas), n_distinct=len(distinct),
                            eta3=sum(r['point']['enr'] == 3 for r in feas), best=best and dict(point=best['point'], P_net=best['P_net'],
                            P_fus=best['P_fus'], f_rad_core=best['f_rad_core']), min_frad_among_netpositive=min_frad)
            print(key, out[key]['burning'], 'feasible', len(feas), 'distinct', len(distinct), 'eta3', out[key]['eta3'],
                  'best', best and (best['point']['R'], best['point']['B'], round(best['P_net']), round(best['f_rad_core'], 3)),
                  'min f_rad (net+, other limits ok)', min_frad and round(min_frad, 3))
    allnp = [r for r in burn if r['P_net'] > 0]
    print('  H98', h, 'net-positive burning samples:', len(allnp), 'min f_rad among them', min((r['f_rad_core'] for r in allnp), default=None))
json.dump(out, open('field_tests/results/d2244b_rescore.json', 'w'), indent=1, default=float)
