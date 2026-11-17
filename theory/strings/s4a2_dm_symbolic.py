"""S4a2 (locked PREREG_S4a2): symbolic check of the Dudas-Mourad 9D solution."""
import sympy as sp
y, a, p0 = sp.symbols('y alpha_E phi0', positive=True); g = sp.Rational(3, 2)
A = sp.Rational(1, 18)*sp.log(sp.sqrt(a)*y) - a*y**2/16
P = p0 + sp.Rational(2, 3)*sp.log(sp.sqrt(a)*y) + sp.Rational(3, 4)*a*y**2
Ap, App, Pp, Ppp = sp.diff(A, y), sp.diff(A, y, 2), sp.diff(P, y), sp.diff(P, y, 2)
res = [36*Ap**2 + 8*App + 4*g*Ap*Pp + Pp**2/4 + a, 36*Ap**2 - Pp**2/4 + a, Ppp + 9*Ap*Pp + g*Pp**2/2 - 2*g*a]
L = []; ok = True
for i, r in enumerate(res, 1):
    s = sp.simplify(sp.expand(r)); num = max(abs(float(s.subs({a: 1, p0: 0, y: yy}))) for yy in [0.05 + k*(2.95/49) for k in range(50)])
    ok &= (s == 0) and num <= 1e-12; L.append(f"eq{i}: symbolic residual = {s}; numeric max = {num:.1e}")
L.append('S4a Route A VALIDATED (exact) -> with Route B (S4a, 1e-10): S4a VALIDATED' if ok else 'NOT VALIDATED')
open('field_tests/results/s4a2_dm_symbolic.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
