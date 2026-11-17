import math, sys, time
sys.path.insert(0, '.')
from tools.janus_astro import jfactor as J
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
rsun, rhosun = 8.5, 0.39
shapes = {'Einasto': J.einasto(20.0, 0.17), 'NFW': J.nfw(20.0), 'Burkert': J.burkert(12.67),
          'Einasto core 1 kpc': J.cored(J.einasto(20.0, 0.17), 1.0), 'Einasto core 3 kpc': J.cored(J.einasto(20.0, 0.17), 3.0)}
res = {}; ok1 = ok2 = True
for name, sh in shapes.items():
    rho = J.normalise(sh, rhosun, rsun); t = time.time()
    a = J.J_route_A(rho, rsun); b = J.J_route_B(rho, rsun); e = abs(a-b)/abs(b); n = abs(rho(rsun)-rhosun)/rhosun
    ok1 &= e <= 1e-3; ok2 &= n <= 1e-12; res[name] = b
    P(f'{name}: J_A={a:.5e} J_B={b:.5e} GeV^2 cm^-5 rel={e:.1e} rho(r_sun)-check={n:.1e} ({time.time()-t:.0f} s)')
P('T1', 'PASS' if ok1 else 'FAIL', 'T2', 'PASS' if ok2 else 'FAIL', '->', 'J VALIDATED' if ok1 and ok2 else 'NOT VALIDATED')
P('Application [estimate]: wino fraction limit per profile (ON-region only; true weakening larger for cores)')
fmaxE = {0.66: 0.16, 1.0: 0.24, 1.85: 0.44}; fpred = {0.66: 0.14, 1.0: 0.26, 1.85: 0.67}
for name in shapes:
    ratio = res['Einasto']/res[name]
    row = ', '.join(f'{m} TeV: f_max={fmaxE[m]*math.sqrt(ratio):.2f} vs f={fpred[m]} {"PASS" if fpred[m] <= fmaxE[m]*math.sqrt(ratio) else "FAIL"}' for m in fmaxE)
    P(f'  {name}: J_Ein/J = {ratio:.3g}; {row}')
open('field_tests/results/janus_astro_a7a.txt', 'w').write('\n'.join(out) + '\n')
