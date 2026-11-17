"""S4e (locked PREREG_S4e_scalar_masses)."""
import sympy as sp, numpy as np, math
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
def setup(D, gam, A, P, y):
    B = -gam*P/2; V0 = 2*sp.exp(gam*P); J = sp.exp(B - A)
    Ay, Py = sp.diff(A, y), sp.diff(P, y)
    W = sp.Rational(D-2, 2)*(3*Ay/J - sp.exp(2*A)*gam*V0*J/(4*Py))
    b = 2*(D-3)*sp.exp(2*A)*V0*(sp.Rational(1, D-2) + sp.Rational(D-2, 8)*gam*Ay/Py)
    U = b + W**2 + sp.diff(W, y)/J
    f = lambda e: sp.lambdify(y, e, 'numpy')
    return f(U), f(J), f(sp.exp(B))
def spectrum(Uf, Jf, eBf, y1, y2, bc, nmodes=2):
    L = quad(eBf, y1, y2, limit=500, epsrel=1e-10)[0]
    th0 = 0.0 if bc == 'D' else math.pi/2
    def theta_end(m2):
        rhs = lambda yy, t: [Jf(yy)*(math.cos(t[0])**2 + (m2 - Uf(yy))*math.sin(t[0])**2)]
        s = solve_ivp(rhs, [y1, y2], [th0], method='LSODA', rtol=1e-9, atol=1e-11)
        return s.y[0, -1]
    out = []; k = 1
    m2s = np.concatenate([np.linspace(-50, 0, 6), np.logspace(-2, 4, 160)]); prev = None
    for m2 in sorted(set(m2s)):
        v = theta_end(m2)
        if prev is not None:
            for n in range(1, 40):
                tgt = th0 + n*math.pi if bc == 'D' else th0 + n*math.pi
                if (prev[1] - tgt)*(v - tgt) < 0:
                    r = brentq(lambda x: theta_end(x) - tgt, prev[0], m2, xtol=1e-10); out.append(r)
        prev = (m2, v)
        if len(out) >= nmodes: break
    return sorted(set(round(x, 10) for x in out))[:nmodes], L
y = sp.symbols('y', positive=True); Ls = []
# validation: 10D critical
D = 10; gc = 4*sp.sqrt(D-1)/(D-2); xi = sp.sqrt(sp.Rational(2*(D-1), D-2))*y
A = -(xi**2/2 - sp.log(xi))/(2*(D-1)); P = sp.Rational(D-2, 4)/sp.sqrt(D-1)*(xi**2/2 + sp.log(xi))
Uf, Jf, eBf = setup(D, gc, A, P, y)
c = float(sp.sqrt(sp.Rational(2*(D-1), D-2)))
y1 = 1e-4/c; y2 = 6.0/c
for z2 in (5.0, 6.0, 7.0):
    pass
res = {}
for bc in ('D', 'N'):
    m2s, L = spectrum(Uf, Jf, eBf, y1, y2, bc)
    r = [math.sqrt(x)*L/math.pi if x > 0 else float('nan') for x in m2s]; res[bc] = r
    Ls.append(f"10D critical, BC {bc}: m^2 = {m2s}, L = {L:.6f}, m L/pi = {r} (target 0.97, 2.13)"); print(Ls[-1], flush=True)
ok = None
for bc in ('D', 'N'):
    r = res[bc]
    if len(r) >= 2 and abs(r[0]/0.97 - 1) <= 0.03 and abs(r[1]/2.13 - 1) <= 0.03: ok = bc
Ls.append(f"V1: {'SOLVER VALIDATED with BC ' + ok if ok else 'NOT VALIDATED'}")
if ok:
    D = 6; gam = sp.Rational(D+2, D-2); dl = sp.nsimplify((gam/(4*sp.sqrt(D-1)/(D-2)) - 1)/2); xi = sp.sqrt(sp.Rational(2*(D-1), D-2))*y; w = sp.sqrt(-dl*(dl+1))
    A = -sp.Rational(1, 2*(D-1))*sp.log(sp.cos(w*xi)**(1/dl)*sp.sin(w*xi)**(-1/(dl+1))); P = sp.Rational(D-2, 4)/sp.sqrt(D-1)*sp.log(sp.cos(w*xi)**(1/dl)*sp.sin(w*xi)**(1/(dl+1)))
    Uf, Jf, eBf = setup(D, gam, A, P, y); yend = float(sp.pi/2/(w*sp.sqrt(sp.Rational(2*(D-1), D-2))))
    m2s, L = spectrum(Uf, Jf, eBf, 1e-4*yend, (1-1e-4)*yend, ok)
    r = [math.sqrt(x)*L/math.pi for x in m2s if x > 0]
    Ls.append(f"6D subcritical, BC {ok}: m^2 = {m2s}, L = {L:.6f}, m L/pi = {r}" + (f", m2/m1 = {r[1]/r[0]:.4f}" if len(r) > 1 else ''))
open('field_tests/results/s4e_scalar_masses.txt', 'w').write('\n'.join(Ls)+'\n'); print('\n'.join(Ls[-2:]))
