"""D423 (locked PREREG_D423_PART2B): second pass, Part 2 — with Route A (ε = 3.04e-7, D419), the potential grows like (1 + ε/x)² at small x.
Compute: where slow roll starts on the small-x side (ε_V = 1), the total e-folds available up to the end of inflation, x and Δφ there, and
the field range from that start to capture. AI-assisted."""
import math, sys, os
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.join(ROOT, "theory", "inflation")); sys.argv = sys.argv[:1]
import cliff_v2 as C
lnV0, Fc = C.version("exp", 4 / math.pi); DL0 = C.DL; c = C.c
eps_w = 3.036e-7
xof = lambda p: math.exp(c * p)
DL = lambda p: DL0(p) - 2 * c * eps_w / (xof(p) + eps_w)
e1 = lambda p: 0.5 * DL(p) ** 2
ps = np.linspace(-40, 2, 20000); ev = np.array([e1(p) for p in ps]); sgn = np.array([DL(p) for p in ps])
pend = brentq(lambda p: e1(p) - 1, *[ps[k] for k in range(len(ps) - 1) if ps[k] > -8 and ev[k] < 1 <= ev[k + 1]][:1], ps[[k for k in range(len(ps) - 1) if ps[k] > -8 and ev[k] < 1 <= ev[k + 1]][0] + 1])
small = [k for k in range(len(ps) - 1) if ps[k] < -8 and ev[k] >= 1 > ev[k + 1]]
pstart = brentq(lambda p: e1(p) - 1, ps[small[-1]], ps[small[-1] + 1]) if small else None
print(f"sign of dlnV/dφ on the small-x side: {'negative (V rises toward small x; field rolls to larger x)' if DL(-20) < 0 else 'positive'}")
if pstart is None:
    print("no ε_V = 1 point on the small-x side in [−40, −8]: slow roll extends to the scan edge")
else:
    Ntot = quad(lambda q: -1 / DL(q), pstart, pend, limit=500)[0]
    print(f"slow roll starts at p = {pstart:.3f} (x = {xof(pstart):.2e}); end p = {pend:.3f} (x = {xof(pend):.2e})")
    print(f"total e-folds available = {Ntot:.1f}  (need N* = 57.2 → margin {Ntot - 57.2:+.1f})")
    print(f"Δφ start → end = {pend - pstart:.2f} M_P; start → capture (x = 29.81) = {math.log(29.81)/c - pstart:.2f} M_P")
