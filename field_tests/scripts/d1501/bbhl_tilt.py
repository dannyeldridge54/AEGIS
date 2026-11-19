"""D1501: exact BBHL alpha'^3 potential shape in u = xi/V (PREREG_D1501)."""
import json, sympy as sp
u, d, ur = sp.symbols('u delta u_rho', positive=True)
G = 3*u*(u**2 + 7*u + 1)/((1 - u)*(2 + u)**4)          # Eq. 3.8 with e^K = (2V+xi)^-2, V scaled out
eK = 1/(2 + u)**2
out = {}
out['G_series_u'] = str(sp.series(G, u, 0, 4).removeO())
out['G_trunc_eq39'] = str(sp.Rational(3, 16)*u)        # leading term = 3u/16 (Eq. 3.9 with e^K0 = 1/4)
# relative correction to the leading term: G / (3u/16)
rel = sp.series(sp.simplify(G/(sp.Rational(3, 16)*u)), u, 0, 3).removeO()
out['G_over_leading'] = str(sp.expand(rel))
# e^K alone relative to vacuum: ratio (2+u_r)^2/(2+u)^2 = 1/(1+x)^2 with x = (u-u_r)/(2+u_r): form B
x = sp.symbols('x', positive=True)
out['eK_ratio_in_x'] = str(sp.simplify(((2 + ur)**2/(2 + u)**2).subs(u, ur + x*(2 + ur))))
# first-order tilt coefficient: G(u)/G(u_r) = 1 + kappa1*delta + ...; kappa1 = G'(u_r)/G(u_r); at small u_r leading 1/u_r (power law) + const
k1 = sp.series(sp.diff(G, u)/G, u, 0, 2).removeO()
out['dlnG_du_series'] = str(sp.expand(k1))
print(json.dumps(out, indent=1))
json.dump(out, open('field_tests/results/D1501_bbhl_tilt.json', 'w'), indent=1)
