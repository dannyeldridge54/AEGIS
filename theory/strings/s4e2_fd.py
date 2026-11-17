"""S4e2 (locked PREREG_S4e2_independent): finite-difference cross-check of S4e."""
import sys, math, numpy as np, sympy as sp; sys.path.insert(0, '.')
from scipy.integrate import cumulative_trapezoid, quad
from scipy.linalg import eigh_tridiagonal
src = open('theory/strings/s4e_scalar_masses.py').read().split("y = sp.symbols('y', positive=True); Ls = []")[0]; ns = {}; exec(compile(src, 's4e', 'exec'), ns)
setup, spectrum = ns['setup'], ns['spectrum']; y = sp.symbols('y', positive=True)
def fd(Uf, Jf, eBf, y1, y2, N):
    ys = np.concatenate([np.geomspace(y1, y1 + 1e-2*(y2-y1), 20000), np.linspace(y1 + 1e-2*(y2-y1), y2, 200000)[1:]])
    zs = cumulative_trapezoid(Jf(ys), ys, initial=0.0); zg = np.linspace(0, zs[-1], N + 2); h = zg[1] - zg[0]
    Ug = np.interp(zg[1:-1], zs, Uf(ys))
    w = eigh_tridiagonal(2/h**2 + Ug, -np.ones(N-1)/h**2, select='i', select_range=(0, 1))[0]
    return list(w), quad(eBf, y1, y2, limit=500, epsrel=1e-10)[0]
L = []
D = 10; gc = 4*sp.sqrt(D-1)/(D-2); xi = sp.sqrt(sp.Rational(2*(D-1), D-2))*y
A = -(xi**2/2 - sp.log(xi))/(2*(D-1)); P = sp.Rational(D-2, 4)/sp.sqrt(D-1)*(xi**2/2 + sp.log(xi))
Uf, Jf, eBf = setup(D, gc, A, P, y); c = float(sp.sqrt(sp.Rational(2*(D-1), D-2)))
w4, Lp = fd(Uf, Jf, eBf, 1e-4/c, 8.0/c, 4000); w8, _ = fd(Uf, Jf, eBf, 1e-4/c, 8.0/c, 8000); pr = [2.9795595536, 14.2865291117]
d_meth = [abs(w8[i]/pr[i] - 1) for i in range(2)]; d_N = [abs(w4[i]/w8[i] - 1) for i in range(2)]
L.append(f"10D critical: FD N=4000 {w4}, N=8000 {w8}; Prüfer {pr}; |FD8/Prüfer-1| {d_meth}; |N4/N8-1| {d_N}")
L.append(f"  m L/pi (FD8) = {[math.sqrt(x)*Lp/math.pi for x in w8]} (BTR context 0.97, 2.13)")
ok = max(d_meth) <= 0.005 and max(d_N) <= 0.002; L.append("V2: " + ("SOLVER VALIDATED (independent)" if ok else "NOT VALIDATED")); print('\n'.join(L), flush=True)
if ok:
    D = 6; gam = sp.Rational(D+2, D-2); dl = sp.nsimplify((gam/(4*sp.sqrt(D-1)/(D-2)) - 1)/2); xi = sp.sqrt(sp.Rational(2*(D-1), D-2))*y; w = sp.sqrt(-dl*(dl+1))
    A = -sp.Rational(1, 2*(D-1))*sp.log(sp.cos(w*xi)**(1/dl)*sp.sin(w*xi)**(-1/(dl+1))); P = sp.Rational(D-2, 4)/sp.sqrt(D-1)*sp.log(sp.cos(w*xi)**(1/dl)*sp.sin(w*xi)**(1/(dl+1)))
    Uf, Jf, eBf = setup(D, gam, A, P, y); yend = float(sp.pi/2/(w*sp.sqrt(sp.Rational(2*(D-1), D-2))))
    wf, L6 = fd(Uf, Jf, eBf, 1e-4*yend, (1-1e-4)*yend, 8000); wp, _ = spectrum(Uf, Jf, eBf, 1e-4*yend, (1-1e-4)*yend, 'D')
    agree = len(wp) >= 2 and max(abs(wf[i]/wp[i] - 1) for i in range(2)) <= 0.005
    r = [math.sqrt(x)*L6/math.pi for x in wf if x > 0]
    L.append(f"6D subcritical: FD {wf}, Prüfer {wp}, L = {L6:.6f}; m L/pi (FD) = {r}" + (f"; m2/m1 = {r[1]/r[0]:.4f}" if len(r) > 1 else '') + f"; methods agree <=0.5%: {agree}; lowest m^2 > 0: {wf[0] > 0}")
open('field_tests/results/s4e2_independent.txt', 'w').write('\n'.join(L)+'\n'); print(L[-1])
