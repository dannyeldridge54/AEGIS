"""S4a (locked PREREG_S4a): Dudas-Mourad 9D orientifold vacuum, two routes."""
import numpy as np, math
from scipy.integrate import solve_ivp, quad
aE, g, ph0 = 1.0, 1.5, 0.0
A = lambda y: (1/18)*np.log(np.sqrt(aE)*y) - aE*y*y/16
P = lambda y: ph0 + (2/3)*np.log(np.sqrt(aE)*y) + 0.75*aE*y*y
def d(f, y, h=1e-5): return (f(y+h) - f(y-h))/(2*h)
def dd(f, y, h=1e-4): return (f(y+h) - 2*f(y) + f(y-h))/h**2
L = []
ys = np.linspace(0.05, 3.0, 600)
Ap, App, Pp, Ppp = d(A, ys), dd(A, ys), d(P, ys), dd(P, ys)
e1 = 36*Ap**2 + 8*App + 4*g*Ap*Pp + 0.25*Pp**2 + aE
e2 = 36*Ap**2 - 0.25*Pp**2 + aE
e3 = Ppp + 9*Ap*Pp + 0.5*g*Pp**2 - 2*g*aE
scale = np.maximum.reduce([abs(36*Ap**2), abs(8*App), abs(0.25*Pp**2), np.full_like(ys, aE), abs(Ppp)])
rA = max(abs(e1/scale).max(), abs(e2/scale).max(), abs(e3/scale).max())
L.append(f"Route A: max relative residual of eqs (2.3) on y in [0.05,3]: {rA:.2e} (eq1 {abs(e1/scale).max():.1e}, eq2 {abs(e2/scale).max():.1e}, eq3 {abs(e3/scale).max():.1e})")
# Route B: A'' from eq1, phi'' from eq3
def rhs(y, s):
    a, ap, p, pp = s
    app = -(36*ap**2 + 4*g*ap*pp + 0.25*pp**2 + aE)/8
    ppp = -(9*ap*pp + 0.5*g*pp**2 - 2*g*aE)
    return [ap, app, pp, ppp]
y0 = 0.5; s0 = [A(y0), d(A, y0, 1e-7), P(y0), d(P, y0, 1e-7)]
sol = solve_ivp(rhs, [y0, 2.5], s0, method='DOP853', rtol=1e-12, atol=1e-14, dense_output=True)
yb = np.linspace(y0, 2.5, 400); Sb = sol.sol(yb)
dA = abs(Sb[0] - A(yb)).max(); dP = abs(Sb[2] - P(yb)).max(); con = abs(36*Sb[1]**2 - 0.25*Sb[3]**2 + aE).max()
L.append(f"Route B: max |dA| {dA:.2e}, max |dphi| {dP:.2e}, constraint max {con:.2e}")
Lprop = quad(lambda y: math.exp(-0.75*P(y)), 1e-9, 50)[0]
L.append(f"e^phi at y=0.05: {math.exp(P(0.05)):.3e}; at y=3: {math.exp(P(3.0)):.3e}; proper length of y in (0,inf): {Lprop:.4f} (finite)")
ok = rA <= 1e-6 and dA <= 1e-8 and dP <= 1e-8 and con <= 1e-8
L.append('S4a VALIDATED' if ok else 'S4a NOT VALIDATED')
open('field_tests/results/s4a_dudas_mourad.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
