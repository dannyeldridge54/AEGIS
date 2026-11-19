"""D1504: tau-dependent flux superpotential as tilt source (PREREG_D1504)."""
import json, sympy as sp
x, y, f, h, Vh, xi = sp.symbols('x y f h Vhat xihat', positive=True)
tau, taub = x + sp.I*y, x - sp.I*y
Kt = -sp.log(-sp.I*(tau - taub))                      # = -log(2y)
# derivatives wrt tau at fixed taubar: K_tau = -1/(tau - taub); K_tau,taub = -1/(tau-taub)^2 -> 1/(4y^2)
K_tau = -1/(tau - taub); K_ttb = sp.simplify(-1/(tau - taub)**2)
W = f - tau*h; Wb = f - taub*h
DW = -h + K_tau*W; DWb = -h + sp.conjugate(K_tau)*Wb
Kinv = sp.simplify(1/K_ttb)
VDt = sp.simplify(sp.expand(Kinv*DW*DWb))              # K^{tt} |D_tau W|^2 (times e^K outside)
eKt = 1/(2*y)
absW2 = sp.simplify(sp.expand(W*Wb))
out = {"Kinv_tautaubar": str(Kinv), "Kinv_DW2": str(sp.factor(VDt)), "absW2": str(absW2)}
# ratio of flux term to alpha'^3 plateau term: V_tau = e^{K_tau} e^{K_V} Kinv|DW|^2 ; V_xi ~ (3 xi/(4 V)) e^{K_tau} e^{K_V} |W|^2 with xi_hat = xi*y^{3/2}*2zeta(3)/(2zeta(3)) ~ xi y^{3/2}
R = sp.simplify(VDt/((3*xi*y**sp.Rational(3, 2)/(4*Vh))*absW2))
out['ratio_flux_over_alpha3'] = str(R)
Rx = sp.simplify(R.subs(x, sp.Rational(1, 2)))
out['ratio_at_x_half'] = str(Rx)
out['ratio_large_y'] = str(sp.limit(Rx*y**sp.Rational(-1, 2), y, sp.oo))   # coefficient of y^{1/2}
# numbers at the D1486 benchmark: x* = g at horizon exit (strip centre, model frame) and the implied xi(tau*)/V
import mpmath as mp
gstar = 126.0  # placeholder replaced below from D1485/D1497 data
out['note'] = 'h/f solve dropped: ratio is independent of f,h (K^{tt}|D W|^2 = |W|^2 identically); see DEVIATIONS D1'
json.dump(out, open('field_tests/results/D1504_flux_tilt.json', 'w'), indent=1); print(json.dumps(out, indent=1))
