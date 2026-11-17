"""S4e4 (locked PREREG_S4e4_6d_masses). Reuses setup/spectrum from s4e_scalar_masses.py without running its 10D part."""
import sympy as sp, math, re
src = open('theory/strings/s4e_scalar_masses.py').read()
exec(src.split("y = sp.symbols('y', positive=True); Ls = []")[0])
y = sp.symbols('y', positive=True)
D = 6; gam = sp.Rational(D+2, D-2); dl = sp.nsimplify((gam/(4*sp.sqrt(D-1)/(D-2)) - 1)/2); xi = sp.sqrt(sp.Rational(2*(D-1), D-2))*y; w = sp.sqrt(-dl*(dl+1))
A = -sp.Rational(1, 2*(D-1))*sp.log(sp.cos(w*xi)**(1/dl)*sp.sin(w*xi)**(-1/(dl+1))); P = sp.Rational(D-2, 4)/sp.sqrt(D-1)*sp.log(sp.cos(w*xi)**(1/dl)*sp.sin(w*xi)**(1/(dl+1)))
Uf, Jf, eBf = setup(D, gam, A, P, y); yend = float(sp.pi/2/(w*sp.sqrt(sp.Rational(2*(D-1), D-2))))
out = [f"delta = {dl} = {float(dl):.6f}, w = {float(w):.6f}, y_end = {yend:.6f}"]; R = {}
for eps in (1e-4, 1e-5):
    m2s, L = spectrum(Uf, Jf, eBf, eps*yend, (1-eps)*yend, 'D')
    r = [math.sqrt(x)*L/math.pi if x > 0 else float('nan') for x in m2s]; R[eps] = (r, L)
    out.append(f"eps {eps:g}: m^2 = {m2s}, L = {L:.6f}, m L/pi = {r}" + (f", m2/m1 = {r[1]/r[0]:.4f}" if len(r) > 1 else '') + (", TACHYON" if m2s and m2s[0] < 0 else ""))
(a, La), (b, Lb) = R[1e-4], R[1e-5]
if len(a) > 1 and len(b) > 1:
    dr = abs((b[1]/b[0])/(a[1]/a[0]) - 1); dm = max(abs(b[i]/a[i]-1) for i in (0, 1))
    out.append(f"ratio change {dr:.2e}, max m L/pi change {dm:.2e} -> {'STABLE' if dr <= 5e-3 and dm <= 1e-2 else 'UNSTABLE'}")
else: out.append("fewer than 2 modes found -> UNSTABLE/INCOMPLETE")
open('field_tests/results/s4e4_6d.txt', 'w').write('\n'.join(out)+'\n'); print('\n'.join(out))
