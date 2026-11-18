# AEGIS-FP GP3ES5EXJ6QFHPRN · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""PT1 fast SERAPIS-E emulator (lock PREREG_PT1). Quadratic surrogate in u=ln(C/1.25e-6) fit to the 5 PW6 exact points
(D1268) at T_R 7.389e8 GeV, MSSM g*. Label: tool (interpolant; valid C~1.0-1.6e-6 at that T_R). Reference: predict_fast."""
import math
from .meter import TABLE   # (ns, C, P, Nstar, r, alpha_s)
TR0 = 7.389e8; C0 = 1.25e-6
def _fit(xs, ys):
    import numpy as np; return np.polyfit(xs, ys, 2)
def _coeffs():
    import numpy as np
    u = [math.log(row[1]/C0) for row in TABLE]
    ns = [row[0] for row in TABLE]; lr = [math.log(row[4]) for row in TABLE]; al = [row[5] for row in TABLE]
    return _fit(u, ns), _fit(u, lr), _fit(u, al)
_NS, _LR, _AL = _coeffs()
def emulate(C):
    import numpy as np
    u = math.log(float(C)/C0)
    return dict(C=float(C), T_R=TR0, ns=float(np.polyval(_NS, u)), r=float(math.exp(np.polyval(_LR, u))),
                alpha_s=float(np.polyval(_AL, u)), engine='PT1 quadratic emulator (fixed T_R)', valid='C 1.0-1.6e-6')
