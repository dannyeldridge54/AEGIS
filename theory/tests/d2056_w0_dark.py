import math
import numpy as np
from scipy.optimize import fsolve
av, ad, Av = 2*math.pi/6, 2*math.pi/12, 0.54
def F(v, Ad):
    tv, td = v; V = tv**1.5 + td**1.5; W = Av*math.exp(-av*tv) + Ad*math.exp(-ad*td)
    Kv = -2*(1.5*tv**0.5)/V; Kd = -2*(1.5*td**0.5)/V      # dK/dt (real-part toy; dK/dT = Kt/2 absorbed consistently)
    return [-av*Av*math.exp(-av*tv) + 0.5*Kv*W, -ad*Ad*math.exp(-ad*td) + 0.5*Kd*W]
hits = []
for Ad in [s*10**e for s in (1, -1) for e in np.linspace(-2, 2, 41)]:
    for g in [(20.15, 40.3), (15, 30), (25, 50), (10, 20), (30, 60), (20, 20)]:
        sol, info, ok, msg = fsolve(F, g, args=(Ad,), full_output=True)
        if ok == 1 and sol[0] > 1 and sol[1] > 1 and max(abs(np.array(F(sol, Ad)))) < 1e-14:
            hits.append((Ad, round(sol[0], 3), round(sol[1], 3)))
hits = sorted(set(hits))
print('solutions found:', len(hits)); [print('  A_d %+9.3f  t_v %8.3f  t_d %8.3f' % h) for h in hits[:20]]
good = [h for h in hits if abs(h[1]-20.15) <= 2.015 and 0.1 <= abs(h[0]) <= 10]
print('PASS' if good else 'FAIL', good[:5])
