#!/usr/bin/env python3
"""D2087: Giudice-Masiero mu for an untwisted torus Higgs (BIM Eq 68): c = mu/m32 = 1 +- 1/x, sign +; test vs D2086 goalposts."""
import math, os, sys, json; import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import wino_mu as w, tsusy
x = 21.10; C = (1 - 1/x, 1 + 1/x)
def evalpt(m32, c, tb):
    s2b = 2*tb/(1 + tb*tb); mu = c*m32; L = mu*s2b; mw = w.wino(m32, L); mg = w.gluino(m32); a = w.aS(tsusy.T(mw, mg, mu, mu))
    return mw, mg, a, (670 <= mw <= 700 and mg >= 2300 and a is not None and abs(a - 0.118) <= 0.0018)
if __name__ == '__main__':
    for tb in (1.0, 1.5, 2, 3, 4):
        W = []; A = []; ok = 0
        for m32 in np.logspace(math.log10(2.5e5), math.log10(7e5), 41):
            for c in np.linspace(*C, 5):
                mw, mg, a, f = evalpt(m32, c, tb); W.append(mw); A.append(a if a else float('nan')); ok += f
        print('v4 band, tanb %.1f: wino %.2f-%.2f TeV, alpha_s %.4f-%.4f, feasible %d' % (tb, min(W)/1e3, max(W)/1e3, np.nanmin(A), np.nanmax(A), ok))
    F = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wino_mu_results.json')))
    G = [f for f in F if C[0] <= f['c'] <= C[1]]
    print('D2086 feasible points with c in [%.3f, %.3f]: %d' % (C[0], C[1], len(G)))
    for f in G: print('   tanb %.1f m32 %.0f TeV mu %.0f TeV wino %.3f gluino %.2f alpha_s %.4f' % (f['tanb'], f['m32']/1e3, f['mu']/1e3, f['wino']/1e3, f['gluino']/1e3, f['alpha_s']))
