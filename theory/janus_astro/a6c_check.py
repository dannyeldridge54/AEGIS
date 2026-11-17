import math, sys, time, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import fast, mapper_feed as F, galaxy as G, jfactor as J
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
t0 = time.perf_counter(); fast.orbits_fast(*p2[:, :2], *v2[:, :2], mw=mw); tcomp = time.perf_counter() - t0
worst = 0.0
for name, p, v in (('extreme', p1, v1), ('disk', p2, v2)):
    t0 = time.perf_counter(); A = fast.orbits_fast(*p, *v, mw=mw); ta = time.perf_counter() - t0
    t0 = time.perf_counter(); B = F.orbit_params_batch3(*p, *v, mw=mw); tb = time.perf_counter() - t0
    e = max(float(np.max(np.abs(A[k]/B[k] - 1))) for k in ('rperi', 'rapo', 'zmax', 'ecc')); worst = max(worst, e)
    P(f'R1 {name}: max rel diff {e:.1e}; fast {ta/n*1e3:.3f} ms/star vs batch3 {tb/n*1e3:.2f} ms/star ({tb/ta:.0f}x)')
ok['R1'] = worst <= 1e-9; P(f'   (numba compile, first call: {tcomp:.1f} s)')
profs = {'Einasto': J.einasto(20.0, 0.17), 'NFW': J.nfw(20.0), 'Burkert': J.burkert(12.67),
         'core1': J.cored(J.einasto(20.0, 0.17), 1.0), 'core3': J.cored(J.einasto(20.0, 0.17), 3.0)}
def vec(shape, rho_sun=0.39, r_sun=8.5):
    k = rho_sun/shape(r_sun); return lambda rr: k*np.array([shape(float(q)) for q in rr])
w2 = 0.0
for nm, sh in profs.items():
    rho = J.normalise(sh, 0.39, 8.5); t0 = time.perf_counter(); ref = J.J_route_B(rho, 8.5); tr = time.perf_counter() - t0
    t0 = time.perf_counter(); fj = fast.jfactor_fast(vec(sh), 8.5); tf = time.perf_counter() - t0
    e = abs(fj/ref - 1); w2 = max(w2, e); P(f'R2 {nm}: J fast {fj:.6e} vs ref {ref:.6e} rel {e:.1e}; {tf:.2f} s vs {tr:.1f} s')
ok['R2'] = w2 <= 1e-6
P('VERDICTS:', ' '.join(f'{k}={"PASS" if x_ else "FAIL"}' for k, x_ in ok.items()), '-> A6c', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
open('field_tests/results/janus_astro_a6c.txt', 'w').write('\n'.join(out) + '\n')
