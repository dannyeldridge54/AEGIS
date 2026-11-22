#!/usr/bin/env python3
"""D2085: CPW Eq.16 effective threshold from v4's split spectrum -> two-loop alpha_s (twoloop.predict)."""
import math, os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import twoloop
def T(mW, mg, mH, mHt, ratio_lq=1.0): return mHt*(mW/mg)**(28/19)*ratio_lq**(3/19)*(mH/mHt)**(3/19)*(mW/mHt)**(4/19)
if __name__ == '__main__':
    mW, mg = 687.0, 4930.0
    for mu in (2.5e5, math.sqrt(2.5e5*7e5), 7e5):
        t = T(mW, mg, mu, mu); a, Ms, aG = twoloop.predict(t)
        print('mu %.2e GeV: T_SUSY %6.0f GeV -> alpha_s %.4f  pull %+.1f sigma  Ms %.2e' % (mu, t, a, (a - 0.1180)/0.0009, Ms))
