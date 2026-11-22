#!/usr/bin/env python3
"""D2091: D2089 four-goalpost scan with a residual KL tree gaugino mass M_tree = m32^2/m_sigma added (both signs)."""
import math, os, sys; import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import wino_mu as w, tsusy, joint4
def scan(msig, sgn):
    P = []
    for m32 in np.logspace(5, math.log10(2e5), 41):
        Mt = sgn*m32*m32/msig; mg = w.gluino(m32) + 2.27*Mt
        for c in (1 - 1/21.10, 1.0, 1 + 1/21.10):
            lo, hi = joint4.tb_band(m32, c)
            for tb in np.arange(1.5, 2.5001, 0.01):
                if not (lo <= tb <= hi): continue
                mu = c*m32; mw = w.wino(m32, mu*2*tb/(1 + tb*tb)) + 0.83*Mt
                if not (670 <= mw <= 700 and mg >= 2300): continue
                a = w.aS(tsusy.T(mw, mg, mu, mu))
                if a is not None and abs(a - 0.118) <= 0.0018: P.append((m32, tb, mw, mg, a, Mt))
    return P
if __name__ == '__main__':
    ok = 0; tot = 0
    for msig in (0.8e8, 1.6e8, 3.2e8):
        for sgn in (1, -1):
            P = scan(msig, sgn); tot += 1; ok += bool(P)
            if P:
                A = np.array(P); print('m_sigma %.1e sign %+d: %3d pts | m3/2 %.0f-%.0f TeV | M_tree %+.0f..%+.0f GeV | gluino %.2f-%.2f TeV | alpha_s %.4f-%.4f'
                      % (msig, sgn, len(P), A[:, 0].min()/1e3, A[:, 0].max()/1e3, A[:, 5].min(), A[:, 5].max(), A[:, 3].min()/1e3, A[:, 3].max()/1e3, A[:, 4].min(), A[:, 4].max()))
            else: print('m_sigma %.1e sign %+d: 0 pts' % (msig, sgn))
    print('VERDICT:', 'CONSISTENT' if ok == tot else ('PARTIAL' if ok else 'FAIL'), '(%d/%d)' % (ok, tot))
