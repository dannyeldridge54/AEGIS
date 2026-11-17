import math, sys, time, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import mapper_feed as F, galaxy as G
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True)); ok = {}
mw = G.MW(); r = np.random.default_rng(7)
R = r.uniform(0.05, 4, 1000); Z = r.uniform(-1, 1, 1000)
FR, FZ = G.force_array(mw, R, Z); ref = np.array([mw.force(a, b) for a, b in zip(R, Z)])
e1 = float(max(np.max(np.abs(FR/ref[:, 0] - 1)), np.max(np.abs(FZ/ref[:, 1] - 1)))); ok['C1'] = e1 <= 1e-12; P(f'C1 force_array vs MW.force: {e1:.1e}')
r = np.random.default_rng(2026); n = 200
ra = r.uniform(0, 360, n); dec = np.degrees(np.arcsin(r.uniform(-1, 1, n))); d = r.uniform(0.05, 5, n)
pmra, pmdec, rv = r.normal(0, 20, n), r.normal(0, 20, n), r.normal(0, 50, n)
p, v = F.galactocentric(ra, dec, d, pmra, pmdec, rv)
t0 = time.perf_counter(); B = F.orbit_params_batch(*p, *v, t_gyr=3.0, mw=mw); tb = time.perf_counter() - t0
t0 = time.perf_counter(); E = [F.orbit_params(*p[:, i], *v[:, i], mw=mw, t_gyr=3.0) for i in range(n)]; te = time.perf_counter() - t0
worst = {k: 0.0 for k in ('rperi', 'rapo', 'ecc', 'zmax')}; okc2 = True
for i in range(n):
    for k in ('rperi', 'rapo', 'ecc'):
        e = abs(B[k][i]/E[i][k] - 1); worst[k] = max(worst[k], e); okc2 &= e <= 1e-3
    ez = abs(B['zmax'][i] - E[i]['zmax']); er = ez/E[i]['zmax']; worst['zmax'] = max(worst['zmax'], min(er, ez)); okc2 &= (er <= 1e-3 or ez <= 1e-3)
ok['C2'] = okc2; P('C2 batch vs exact (200 stars, 3 Gyr): worst ' + ', '.join(f'{k} {v_:.1e}' for k, v_ in worst.items()))
ok['C3'] = tb/n < 0.517; P(f'C3 cost: batch {tb/n*1e3:.2f} ms/star ({tb:.1f} s for {n}); exact {te/n*1e3:.0f} ms/star')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if x else "FAIL"}' for k, x in ok.items()), '-> A8c', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
open('field_tests/results/janus_astro_a8c.txt', 'w').write('\n'.join(out) + '\n')
