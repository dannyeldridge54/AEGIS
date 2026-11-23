import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'gifts', 'chronos'))
import nuclide_pulse as P, fusion as F
import chronos as CH, chronos_a3 as A3
N = P.parse(); gs = [x for x in N if x['iso'] == 0]; iso = [x for x in N if x['iso'] in (1, 2)]
N1 = dict(ground_states=len(gs), isomers_i12=len(iso), all_rows=len(N)); N2 = dict(stable_gs=sum(x['stable'] for x in gs))
idx = {}
for x in N: idx.setdefault((x['Z'], x['A']), []).append(x)
T12 = dict(CH.T12); T12.update(A3.T12x); audit = []
for name, t in sorted(T12.items()):
    Z, A, isom = P.key(name); rows = idx.get((Z, A), [])
    row = next((r for r in rows if (r['iso'] > 0) == isom and r['t12_s']), None)
    if row is None: audit.append(dict(nuclide=name, chronos_s=t, nubase_s=None, rel=None, flag='NOT FOUND')); continue
    rel = t / row['t12_s'] - 1; audit.append(dict(nuclide=name, chronos_s=t, nubase_s=row['t12_s'], rel=rel, flag='FLAG' if abs(rel) > 0.005 else 'ok'))
N3 = dict(n=len(audit), flagged=[a for a in audit if a['flag'] != 'ok'], max_abs_rel_ok=max(abs(a['rel']) for a in audit if a['flag'] == 'ok'))
mass = {}
for k, (Z, A) in dict(n=(0, 1), H1=(1, 1), D=(1, 2), T=(1, 3), He3=(2, 3), He4=(2, 4)).items():
    r = next(r for r in idx[(Z, A)] if r['iso'] == 0); mass[k] = dict(engine=F.M[k], ame=A + r['me_keV'] / 931494.10242, diff=F.M[k] - (A + r['me_keV'] / 931494.10242))
N4 = dict(mass=mass, pass_=all(abs(v['diff']) <= 2e-9 for v in mass.values()))
cat = [dict(Z=x['Z'], A=x['A'], iso=x['iso'], name=x['name'], me_keV=x['me_keV'], est=x['me_est'], t12_s=x['t12_s'], stable=x['stable'], modes=x['modes']) for x in N]
json.dump(dict(source='NUBASE2020 via pynucastro 3.2.0', rows=cat), open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'nuclide_catalog.json'), 'w'))
r = dict(N1=N1, N2=N2, N3=N3, N4=N4); json.dump(r, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'nuclide_audit.json'), 'w'), indent=1, default=str)
print(json.dumps(dict(N1=N1, N2=N2, N3_n=N3['n'], N3_flagged=N3['flagged'], N3_max_ok=N3['max_abs_rel_ok'], N4=N4), indent=1, default=str))
