"""Independent reproduction of arXiv:2405.18813 Model III (D1915)."""
import numpy as np, cmath, math
from scipy.optimize import minimize
w = cmath.exp(2j*math.pi/3)
def E2(t, N=60):
    q = cmath.exp(2j*math.pi*t); s = 0
    for n in range(1, N):
        sig = sum(d for d in range(1, n+1) if n % d == 0); s += sig*q**n
    return 1 - 24*s
dle = lambda t: 1j*math.pi/12*E2(t)          # d ln eta / d tau
def Ytrip(t):
    a, b, c, d = dle(t/3), dle((t+1)/3), dle((t+2)/3), dle(3*t)
    Y1 = 1j/(2*math.pi)*(a + b + c - 27*d)
    Y2 = -1j/math.pi*(a + w*w*b + w*c)
    Y3 = -1j/math.pi*(a + w*b + w*w*c)
    return Y1, Y2, Y3
def Y4(t): Y1,Y2,Y3 = Ytrip(t); return Y1**2 + 2*Y2*Y3
def Y6(t): Y1,Y2,Y3 = Ytrip(t); return Y1**3 + Y2**3 + Y3**3 - 3*Y1*Y2*Y3
a0, b3, al = 2, -3, 0.1
def V(x):
    t1 = complex(x[0], x[1])
    if t1.imag <= 0.05: return 1e9
    t2 = b3/(a0*t1)
    if t2.imag <= 0.05: return 1e9
    return (2*t1.imag)**4*abs(Y4(t1))**2 + al**2*(2*t2.imag)**6*abs(Y6(t2))**2
Y1,_,_ = Ytrip(0.5j+1.5j); print('check Y1(2i) ~ 1:', round(abs(Y1),4))
target = complex(-0.529, 0.867)
starts = [(-0.55, 0.88), (-0.45, 0.95), (-0.65, 0.80)]
res = []
for s in starts:
    r = minimize(V, s, method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-12, maxiter=4000))
    t = complex(*r.x); res.append((t, r.fun))
    print('start %s -> tau1 = %.4f%+.4fi  V = %.4f  |tau1 - paper| = %.4f  |tau1 - omega| = %.4f' % (s, t.real, t.imag, r.fun, abs(t-target), abs(t-w)))
d = [abs(t-target) for t, _ in res]
v = 'PASS' if max(d) < 0.01 and all(f > 0 for _, f in res) else ('PARTIAL' if min(d) < 0.03 else 'FAIL')
print('VERDICT:', v)
