#!/usr/bin/env python3
"""D2097: hidden USp confinement scales for the unified PS model's completions (He-Li-Sun Eq 3.12)."""
import math, os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seed_v3 as s, exotics as e
from fractions import Fraction as Fr
chi = (Fr(1), Fr(3), Fr(2)); A, B, C = (-1, -1, 0, -1, -1, -1), (-1, 0, -3, -1, 1, 0), (0, -1, -3, -1, -1, -1)
K = 25.0/6; MS = 1.0e16
S = [w for w in s.ALL if s.zprod(w, chi)[1] == 0 and s.zprod(w, chi)[0] > 0]
R = tuple(t - 8*xa - 4*xb - 4*xc for t, xa, xb, xc in zip(s.TGT, s.X(A), s.X(B), s.X(C)))
comps = e.completions(S, chi, R, s.kcheck([(8, A), (4, B), (4, C)])); ok = 0
for n, cm in enumerate(comps):
    good = True; lines = []
    for N, h in cm:
        Ia, Ib, Ic = (abs(s.inter(h, v)) for v in (A, B, C)); ex = any(s.inter(h, v) or s.inter(h, v, True) for v in (A, B, C))
        beta = -6 + 2*Ia + Ib + Ic; ainv = K*float(s.zprod(h, chi)[0])
        lam = MS*math.exp(-2*math.pi*ainv/abs(beta)) if beta < 0 else None
        p = (not ex) or (beta < 0 and lam and 1e4 <= lam <= MS); good &= bool(p)
        lines.append('   ring N=%d Re z=%s exotic=%s beta=%+d alpha^-1=%.1f Lambda=%s %s' % (N, s.zprod(h, chi)[0], ex, beta, ainv, '%.1e' % lam if lam else '-', 'ok' if p else 'FAIL'))
    ok += good; print('completion %d: %s' % (n, 'PASS' if good else 'fail')); print('\n'.join(lines))
print('VERDICT:', 'PASS' if ok else 'FAIL', '(%d/%d completions)' % (ok, len(comps)))
