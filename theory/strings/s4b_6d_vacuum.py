"""S4b(b) (locked PREREG_S4b_6d_tadpole): 6D Dudas-Mourad-type vacuum. Equations and general-D solution from
Basile-Thomee 2209.10553 (fetched): action R - 4/(D-2)(dphi)^2 - 2 aE e^{gamma phi} (Eq. 3.1), gauge B = -gamma phi/2,
ODEs (3.2), solutions (3.9)-(3.11), gamma = 4 sqrt(D-1)/(D-2) (1+2 delta). In this normalisation the orientifold-type
tadpole has gamma_o = (D+2)/(D-2) (Eq. 3.17) = the exponent found in D1014 before canonical rescaling."""
import sympy as sp, numpy as np, math
from scipy.integrate import solve_ivp
D = 6; gam = sp.Rational(D + 2, D - 2); aE = 1
gc = 4*sp.sqrt(D - 1)/(D - 2); dl = sp.nsimplify((gam/gc - 1)/2)
y = sp.symbols('y', positive=True); xi = sp.sqrt(sp.Rational(2*(D - 1), D - 2))*y; w = sp.sqrt(-dl*(dl + 1))
A = -sp.Rational(1, 2*(D - 1))*sp.log(sp.cos(w*xi)**(1/dl)*sp.sin(w*xi)**(-1/(dl + 1)))
P = sp.Rational(D - 2, 4)/sp.sqrt(D - 1)*sp.log(sp.cos(w*xi)**(1/dl)*sp.sin(w*xi)**(1/(dl + 1)))
Ap, App, Pp, Ppp = sp.diff(A, y), sp.diff(A, y, 2), sp.diff(P, y), sp.diff(P, y, 2)
e1 = (D-2)*App + sp.Rational(D-2, 2)*gam*Pp*Ap + sp.Rational((D-1)*(D-2), 2)*Ap**2 + sp.Rational(2, D-2)*Pp**2 + aE
e2 = sp.Rational((D-1)*(D-2), 2)*Ap**2 - sp.Rational(2, D-2)*Pp**2 + aE
e3 = sp.Rational(8, D-2)*Ppp + sp.Rational(8, D-2)*((D-1)*Ap + gam/2*Pp)*Pp - 2*gam*aE
L = [f"D = {D}: gamma_o = {gam}, gamma_c = {sp.nsimplify(gc)} = {float(gc):.6f}, delta = {float(dl):.6f} (subcritical: -1/2 < delta < 0 -> trigonometric branch)"]
yend = float(sp.pi/2/(w*sp.sqrt(sp.Rational(2*(D-1), D-2))))
L.append(f"interval: y in (0, {yend:.6f}) (sin -> 0 at y = 0, cos -> 0 at y_end)")
ys = np.linspace(0.02*yend, 0.98*yend, 400); f = [sp.lambdify(y, e, 'mpmath') for e in (e1, e2, e3)]
import mpmath as mp; mp.mp.dps = 40
res = [max(abs(float(fi(mp.mpf(v)))) for v in ys) for fi in f]
L.append(f"Route A (analytic Eq. 3.11 in ODEs 3.2, 40-digit arithmetic): max residuals eq1 {res[0]:.1e}, eq2 {res[1]:.1e}, eq3 {res[2]:.1e}")
Af, Apf, Pf, Ppf = [sp.lambdify(y, e, 'mpmath') for e in (A, Ap, P, Pp)]
def rhs(t, s):
    a, ap, p, pp = s; g = float(gam)
    app = -(g*(D-2)/2*pp*ap + (D-1)*(D-2)/2*ap**2 + 2/(D-2)*pp**2 + aE)/(D-2)
    ppp = -(((D-1)*ap + g/2*pp)*pp) + 2*g*aE*(D-2)/8
    return [ap, app, pp, ppp]
y0 = 0.3*yend; s0 = [float(Af(y0)), float(Apf(y0)), float(Pf(y0)), float(Ppf(y0))]
sol = solve_ivp(rhs, [y0, 0.9*yend], s0, method='DOP853', rtol=1e-13, atol=1e-15, dense_output=True)
yb = np.linspace(y0, 0.9*yend, 300); S = sol.sol(yb)
dA = max(abs(S[0][i] - float(Af(v))) for i, v in enumerate(yb)); dP = max(abs(S[2][i] - float(Pf(v))) for i, v in enumerate(yb))
con = max(abs((D-1)*(D-2)/2*S[1][i]**2 - 2/(D-2)*S[3][i]**2 + aE) for i in range(len(yb)))
L.append(f"Route B (numerical from y0 = 0.3 y_end): max |dA| {dA:.1e}, |dphi| {dP:.1e}, constraint {con:.1e}")
ok = max(res) < 1e-20 and dA <= 1e-8 and dP <= 1e-8 and con <= 1e-8
L.append(f"e^phi (phi0 = 0): y = 0.05 y_end: {math.exp(float(Pf(0.05*yend))):.3e}; y = 0.95 y_end: {math.exp(float(Pf(0.95*yend))):.3e}")
L.append("S4b(b) " + ("two routes agree: 6D vacuum CONFIRMED" if ok else "routes DISAGREE"))
open('field_tests/results/s4b_6d_vacuum.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
