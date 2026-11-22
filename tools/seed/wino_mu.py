#!/usr/bin/env python3
"""D2086: joint (alpha_s, wino, gluino) feasibility with free higgsino mu; PGM gaugino formulas (1207.5453 Eqs 6,7,9), CPW T_SUSY, two-loop."""
import math, os, sys, json; import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import twoloop, tsusy
lg = math.log10
def gluino(m32): d = lg(m32/1e5); return 2.5e-2*(1 - 0.13*d - 0.04*d)*m32
def wino(m32, L): x = m32 + L; return 3.0e-3*(1 - 0.04*lg(x/1e5) + 0.02*lg(m32/1e5))*x if x > 0 else -1
Tg = np.logspace(math.log10(200), math.log10(2e5), 80); Ag = np.array([twoloop.predict(t)[0] for t in Tg])
aS = lambda t: float(np.interp(math.log(t), np.log(Tg), Ag)) if Tg[0] <= t <= Tg[-1] else None
if __name__ == '__main__':
    for t in (1000, 7000, 40000): print('table check T=%d: interp %.5f direct %.5f' % (t, aS(t), twoloop.predict(t)[0]))
    feas = []; v4 = None
    for tb in (1.5, 2, 3, 4):
        s2b = 2*tb/(1 + tb*tb)
        for m32 in np.logspace(math.log10(3e4), math.log10(3e6), 121):
            mg = gluino(m32)
            for sg in (1, -1):
                for amu in np.logspace(4, math.log10(3e6), 121):
                    L = sg*amu*s2b; mw = wino(m32, L)
                    if not (670 <= mw <= 700 and mg >= 2300): continue
                    t = tsusy.T(mw, mg, amu, amu); a = aS(t)
                    if a is not None and abs(a - 0.1180) <= 0.0018:
                        feas.append(dict(tanb=tb, m32=m32, mu=sg*amu, c=sg*amu/m32, wino=mw, gluino=mg, T=t, alpha_s=a))
    print('feasible points: %d' % len(feas))
    if feas:
        for tb in (1.5, 2, 3, 4):
            F = [f for f in feas if f['tanb'] == tb]
            if F: print(' tanb %.1f: n %d  m32 %.0f-%.0f TeV  mu %.0f..%.0f TeV  c=mu/m32 %.2f..%.2f  gluino %.1f-%.1f TeV  O(1)|c| in [0.3,3]: %d'
                        % (tb, len(F), min(f['m32'] for f in F)/1e3, max(f['m32'] for f in F)/1e3, min(f['mu'] for f in F)/1e3, max(f['mu'] for f in F)/1e3,
                           min(f['c'] for f in F), max(f['c'] for f in F), min(f['gluino'] for f in F)/1e3, max(f['gluino'] for f in F)/1e3,
                           sum(0.3 <= abs(f['c']) <= 3 for f in F)))
    # v4 as used so far: L = 0, gluino 4.93 TeV, mu in [0.25, 0.7] PeV
    for mu in (2.5e5, 7e5): print('v4 as-used (L=0, mu=%.2e): alpha_s %.4f' % (mu, aS(tsusy.T(687, 4930, mu, mu))))
    json.dump(feas, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wino_mu_results.json'), 'w'))
