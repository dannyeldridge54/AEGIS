# AEGIS-FP RM72HOFHJV3JXBRY · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Scalar-sector sufficient stability condition (BTR 2209.10553 Eq. 5.10; D1140): Ω'/φ₀' ≥ −8/(γ(D−2)²) everywhere ⇒ b ≥ 0 ⇒ all scalar m² ≥ 0."""
import sympy as sp, mpmath as mp
from .background import y
def scalar_condition(bg, npts=4000, eps=1e-6):
    D, g = bg['D'], bg['gam']; R = sp.lambdify(y, sp.diff(bg['A'], y)/sp.diff(bg['P'], y), 'mpmath'); thr = -sp.Rational(8)/(g*(D - 2)**2)
    if bg['y_end'] == sp.oo: raise NotImplementedError('critical (infinite y) range: pass a finite y range in v0.2')
    mp.mp.dps = 40; ye = mp.mpf(sp.N(bg['y_end'], 40))
    vals = [R((eps + (1 - 2*eps)*i/mp.mpf(npts - 1))*ye) for i in range(npts)]
    return dict(min=float(min(vals)), max=float(max(vals)), threshold=float(thr), stable=all(v >= thr for v in vals))
