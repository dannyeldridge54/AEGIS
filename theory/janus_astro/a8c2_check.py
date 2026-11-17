import math, sys, time, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import mapper_feed as F, galaxy as G
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True)); ok = {}
mw = G.MW()
r = np.random.default_rng(2026); n = 200
ra = r.uniform(0, 360, n); dec = np.degrees(np.arcsin(r.uniform(-1, 1, n))); d = r.uniform(0.05, 5, n)
p1, v1 = F.galactocentric(ra, dec, d, r.normal(0, 20, n), r.normal(0, 20, n), r.normal(0, 50, n))
r = np.random.default_rng(11)
ph = r.uniform(-0.37, 0.37, n); Rg = 8.0 + r.uniform(-3, 3, n); zg = r.uniform(-0.5, 0.5, n)
x, y = -Rg*np.cos(ph), Rg*np.sin(ph)
vR, vphi, vz = r.normal(0, 35, n), r.uniform(220, 232, n) + r.normal(0, 25, n), r.normal(0, 20, n)
er, ep = np.array([x, y])/Rg, np.array([-y, x])/Rg   # radial and azimuthal unit vectors (azimuth sense chosen so Sun's v_y > 0)
ep = -ep if (ep[1, 0]*1 < 0 and x[0] < 0) else ep
vx, vy = vR*er[0] + vphi*ep[0], vR*er[1] + vphi*ep[1]
p2, v2 = np.array([x, y, zg]), np.array([vx, vy, vz])
for name, p, v in (('P1 extreme', p1, v1), ('P2 disk', p2, v2)):
    t0 = time.perf_counter(); B = F.orbit_params_batch2(*p, *v, t_gyr=3.0, mw=mw); tb = (time.perf_counter() - t0)/n
    E = [F.orbit_params(*p[:, i], *v[:, i], mw=mw, t_gyr=3.0) for i in range(n)]
    w = {k: 0.0 for k in ('rperi', 'rapo', 'ecc', 'zmax')}; good = True
    for i in range(n):
        for k in ('rperi', 'rapo', 'ecc'):
            e = abs(B[k][i]/E[i][k] - 1); w[k] = max(w[k], e); good &= e <= 1e-3
        ez = abs(B['zmax'][i] - E[i]['zmax']); er_ = ez/E[i]['zmax']; w['zmax'] = max(w['zmax'], min(er_, ez)); good &= (er_ <= 1e-3 or ez <= 1e-3)
    good &= tb <= 0.010; ok[name] = good
    P(f'{name}: worst ' + ', '.join(f'{k} {x_:.1e}' for k, x_ in w.items()) + f'; {tb*1e3:.2f} ms/star ({B["steps"]} steps)', 'PASS' if good else 'FAIL')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if x_ else "FAIL"}' for k, x_ in ok.items()), '-> A8c2', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
open('field_tests/results/janus_astro_a8c2.txt', 'w').write('\n'.join(out) + '\n')
