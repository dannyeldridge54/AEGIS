#!/usr/bin/env python3
"""D2084: two-loop gauge running (no Yukawas) for exact unification alpha1=alpha2=alpha3 at Ms; predict alpha_s(MZ)."""
import numpy as np, math
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
MZ = 91.1876; a2i0 = 127.95*0.23122; aYi0 = 127.95*(1 - 0.23122); a1i0 = 0.6*aYi0
SM = (np.array([41/10, -19/6, -7]), np.array([[199/50, 27/10, 44/5], [9/10, 35/6, 12], [11/10, 9/2, -26]]))
MS = (np.array([33/5, 1, -3]), np.array([[199/25, 27/5, 88/5], [9/5, 25, 24], [11/5, 9, 14]]))
def rhs(t, y, b, B, two):
    a = 1/y; return -b/(2*math.pi) - (two*(B @ a)/(8*math.pi**2))
def up(a3i, Msusy, two):
    y = np.array([a1i0, a2i0, a3i]); t0 = math.log(MZ); ts = math.log(max(Msusy, MZ))
    if ts > t0: y = solve_ivp(rhs, (t0, ts), y, args=(*SM, two), rtol=1e-10, atol=1e-12).y[:, -1]
    ev = lambda t, y, *a: y[0] - y[1]; ev.terminal = True
    s = solve_ivp(rhs, (ts, math.log(1e19)), y, args=(*MS, two), events=ev, rtol=1e-10, atol=1e-12)
    te, ye = s.t_events[0][0], s.y_events[0][0]; return math.exp(te), ye
def predict(Msusy, two=1.0):
    f = lambda a3i: (lambda r: r[1][2] - r[1][0])(up(a3i, Msusy, two))
    a3i = brentq(f, 5.0, 12.0, xtol=1e-12); Ms, y = up(a3i, Msusy, two); return 1/a3i, Ms, 1/y[0]
if __name__ == '__main__':
    c = predict(MZ, 0.0); print('CONTROL one-loop, Msusy=MZ: alpha_s %.4f Ms %.2e' % c[:2], 'PASS' if abs(c[0] - 0.1167) <= 0.0005 else 'FAIL')
    for m in (500, 1000, 3000, 10000):
        a, Ms, aG = predict(m); print('two-loop Msusy %5d GeV: alpha_s %.4f  pull %+.1f sigma  Ms %.2e  alpha_G^-1 %.2f' % (m, a, (a - 0.1180)/0.0009, Ms, aG))
