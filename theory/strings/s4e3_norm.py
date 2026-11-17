"""S4e3 (locked PREREG_S4e3_mass_normalisation)."""
import sympy as sp, numpy as np, math
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
D = 10; y = sp.symbols('y', positive=True); gc = 4*sp.sqrt(D-1)/(D-2)
xi = sp.sqrt(sp.Rational(2*(D-1), D-2))*y
A = -(xi**2/2 - sp.log(xi))/(2*(D-1)); P = sp.Rational(D-2, 4)/sp.sqrt(D-1)*(xi**2/2 + sp.log(xi)); B = -gc*P/2
Af = sp.lambdify(y, A, 'numpy'); eBf = sp.lambdify(y, sp.exp(B), 'numpy')
c = float(sp.sqrt(sp.Rational(2*(D-1), D-2))); y1, y2 = 1e-4/c, 8.0/c
r0 = [0.9317505476938241, 2.0402669137227405]  # S4e BC D (recorded)
L = quad(eBf, y1, y2, limit=500, epsrel=1e-12)[0]
Aref = {'C0': 0.0}
mx = minimize_scalar(lambda t: -Af(t), bounds=(y1, y2), method='bounded', options={'xatol': 1e-12}); Aref['C1'] = float(Af(mx.x))
ymid = brentq(lambda t: quad(eBf, y1, t, limit=500, epsrel=1e-12)[0] - L/2, y1, y2, xtol=1e-12); Aref['C2'] = float(Af(ymid))
I = quad(lambda t: math.exp((D-2)*Af(t))*eBf(t), y1, y2, limit=500, epsrel=1e-12)[0]/L; Aref['C3'] = math.log(I)/(D-2)
out = [f"L = {L:.6f}"]; match = []
for k, a in Aref.items():
    r = [x*math.exp(-a) for x in r0]; ok = abs(r[0]-0.97) <= 0.01 and abs(r[1]-2.13) <= 0.01
    if ok: match.append(k)
    out.append(f"{k}: A_ref = {a:+.6f}, m L/pi = [{r[0]:.4f}, {r[1]:.4f}], match = {ok}")
out.append(f"needed common factor: {0.97/r0[0]:.4f}, {2.13/r0[1]:.4f} (A_ref ~ {-math.log(0.97/r0[0]):+.4f}, {-math.log(2.13/r0[1]):+.4f})")
out.append("VERDICT: " + ("CONVENTION IDENTIFIED (post-hoc, consistent): " + match[0] if len(match) == 1 else "AMBIGUOUS: " + ",".join(match) if match else "NOT EXPLAINED by these conventions"))
open('field_tests/results/s4e3_norm.txt', 'w').write('\n'.join(out)+'\n'); print('\n'.join(out))
