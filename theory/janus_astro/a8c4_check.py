import math, sys, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import fast, mapper_feed as F, galaxy as G
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True)); ok = {}
mw = G.MW(); n = 200
r = np.random.default_rng(2026)
ra = r.uniform(0, 360, n); dec = np.degrees(np.arcsin(r.uniform(-1, 1, n))); d = r.uniform(0.05, 5, n)
p1, v1 = F.galactocentric(ra, dec, d, r.normal(0, 20, n), r.normal(0, 20, n), r.normal(0, 50, n))
r = np.random.default_rng(11)
ph = r.uniform(-0.37, 0.37, n); Rg = 8.0 + r.uniform(-3, 3, n); zg = r.uniform(-0.5, 0.5, n)
x, y = -Rg*np.cos(ph), Rg*np.sin(ph); vR, vphi, vz = r.normal(0, 35, n), r.uniform(220, 232, n) + r.normal(0, 25, n), r.normal(0, 20, n)
er, ep = np.array([x, y])/Rg, np.array([-y, x])/Rg; ep = -ep if (ep[1, 0] < 0 and x[0] < 0) else ep
p2, v2 = np.array([x, y, zg]), np.array([vR*er[0] + vphi*ep[0], vR*er[1] + vphi*ep[1], vz])
e2ok = True
for name, p, v in (('extreme', p1, v1), ('disk', p2, v2)):
    A = fast.orbits_fast(*p, *v, mw=mw)
    Ev = [F.orbit_params_exact_events(*p[:, i], *v[:, i], mw=mw) for i in range(n)]
    w = {k: 0.0 for k in ('rperi', 'rapo', 'ecc', 'zmax')}
    for i in range(n):
        for k in ('rperi', 'rapo', 'ecc'):
            e = abs(A[k][i]/Ev[i][k] - 1); w[k] = max(w[k], e); e2ok &= e <= 1e-3
        ez = abs(A['zmax'][i] - Ev[i]['zmax']); er_ = ez/Ev[i]['zmax']; w['zmax'] = max(w['zmax'], min(ez, er_)); e2ok &= (ez <= 1e-3 or er_ <= 1e-3)
    P(f'E2 {name}: fast vs event reference worst ' + ', '.join(f'{k} {x_:.1e}' for k, x_ in w.items()))
    if name == 'extreme':
        S = [F.orbit_params(*p[:, i], *v[:, i], mw=mw, t_gyr=3.0) for i in range(n)]
        diff = [i for i in range(n) if abs(S[i]['rperi']/Ev[i]['rperi'] - 1) > 1e-4]
        closer = [i for i in diff if abs(A['rperi'][i] - Ev[i]['rperi']) < abs(S[i]['rperi'] - Ev[i]['rperi'])]
        frac = len(closer)/len(diff) if diff else float('nan'); ok['E1'] = (not diff) or frac >= 0.9
        worst_s = max(abs(S[i]['rperi']/Ev[i]['rperi'] - 1) for i in range(n))
        P(f'E1 extreme: sampled reference vs event reference r_peri worst {worst_s:.1e}; {len(diff)} stars differ > 1e-4; fast closer in {len(closer)} ({frac:.2f})')
ok['E2'] = e2ok
P('VERDICTS:', ' '.join(f'{k}={"PASS" if x_ else "FAIL"}' for k, x_ in ok.items()), '-> A8c4', 'VALIDATED' if ok['E2'] else 'NOT VALIDATED', '| E1 answer:', 'reference sampling CONFIRMED' if ok['E1'] else 'NOT confirmed')
open('field_tests/results/janus_astro_a8c4.txt', 'w').write('\n'.join(out) + '\n')
