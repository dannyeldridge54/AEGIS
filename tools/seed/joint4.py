#!/usr/bin/env python3
"""D2089: GM branch four-goalpost joint test (alpha_s, wino, gluino, m_h), tan beta continuous."""
import math, os, sys; import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import wino_mu as w, tsusy, mh
from scipy.optimize import brentq
def tb_band(MS, c):
    out = []
    for dl in (-0.0030, 0.0030):
        y = mh.run(MS, mh.Y0[4] + dl); out.append(brentq(lambda tb: mh.lam_bdy(y, tb, c) - y[4], 1.0001, 60))
    return min(out), max(out)
if __name__ == '__main__':
    P = []
    for m32 in np.logspace(math.log10(1e5), math.log10(2e5), 41):
        mg = w.gluino(m32)
        for c in (1 - 1/21.10, 1.0, 1 + 1/21.10):
            lo, hi = tb_band(m32, c)
            for tb in np.arange(1.5, 2.5001, 0.01):
                if not (lo <= tb <= hi): continue
                s2b = 2*tb/(1 + tb*tb); mu = c*m32; mw = w.wino(m32, mu*s2b)
                if not (670 <= mw <= 700 and mg >= 2300): continue
                a = w.aS(tsusy.T(mw, mg, mu, mu))
                if a is not None and abs(a - 0.118) <= 0.0018: P.append((m32, c, tb, mw, mg, a))
    print('points passing all four goalposts: %d' % len(P))
    if P:
        A = np.array(P)
        print(' m3/2 %.0f-%.0f TeV | tanb %.2f-%.2f | wino %.3f-%.3f TeV | gluino %.2f-%.2f TeV | alpha_s %.4f-%.4f (pull %.1f..%.1f)' % (
            A[:, 0].min()/1e3, A[:, 0].max()/1e3, A[:, 2].min(), A[:, 2].max(), A[:, 3].min()/1e3, A[:, 3].max()/1e3, A[:, 4].min()/1e3, A[:, 4].max()/1e3,
            A[:, 5].min(), A[:, 5].max(), (A[:, 5].min() - 0.118)/0.0009, (A[:, 5].max() - 0.118)/0.0009))
    print('VERDICT:', 'CONSISTENT' if P else 'FAIL')
