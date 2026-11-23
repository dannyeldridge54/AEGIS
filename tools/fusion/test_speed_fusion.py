"""SPEED-fusion V1-V4."""
import json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F, fusion_fast as X
Ea = F.two_body_split('DT')[1]; rnd = random.Random(7); rel = lambda a, b: abs(a - b) / max(abs(b), 1e-300)
v1 = 0.0
for _ in range(50):
    n, T, fh = rnd.uniform(0.7e20, 1.3e20), rnd.uniform(3, 25), rnd.uniform(0.01, 0.06)
    a = F.plasma(F.ITER, n, T, Ea, fh); b = X.plasma_fast(F.ITER, n, T, Ea, fh)
    v1 = max(v1, max(rel(b[k], a[k]) for k in a if isinstance(a[k], float)))
v2 = 0.0; cases = [(F.ITER, None, None), (F.ITER_400, None, None)] + [(F.ITER, F.ITER['Ip'] / (3.14159265 * 4) * 1e20 * (0.6 + 0.04 * i), 50.0) for i in range(10)]
t0 = time.time(); ref = [F.operating_point(m, Ea, n_avg=n, P_aux=p) for m, n, p in cases]; tr = time.time() - t0
t0 = time.time(); fst = [X.operating_point_fast(m, Ea, n_avg=n, P_aux=p) for m, n, p in cases]; tf = time.time() - t0
for a, b in zip(ref, fst):
    if (a is None) != (b is None): v2 = float('inf'); continue
    if a: v2 = max(v2, max(rel(b[k], a[k]) for k in a if isinstance(a[k], float)))
t0 = time.time(); gr = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'prom3.json')))['E4']['best']; tref = 511.0
t0 = time.time(); gf = X.goal_dials_fast(F.ITER, Ea, F.PLANT_DEMO); tg = time.time() - t0
v3 = dict(same_point=bool(abs(gf['n_avg'] - gr['n_avg']) <= 1e-6 * gr['n_avg'] and gf['P_aux'] == gr['P_aux']), P_net_rel=rel(gf['P_net'], gr['P_net']))
r = dict(V1_max_rel=v1, V2_max_rel=v2, V2_speed=tr / tf, V3=v3, V4=dict(ref_s=tref, fast_s=tg, speedup=tref / tg))
r['verdict'] = dict(V1=v1 <= 1e-10, V2=v2 <= 1e-8, V3=v3['same_point'] and v3['P_net_rel'] <= 1e-8, V4=tref / tg >= 10); r['verdict']['PASS'] = all(r['verdict'].values())
json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'speed_fusion.json'), 'w'), indent=1, default=str); print(json.dumps(r, indent=1, default=str))
