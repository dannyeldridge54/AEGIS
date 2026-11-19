"""D1505: xi/V regime check at D1486 benchmarks (PREREG_D1505)."""
import json, mpmath as mp
Er = mp.mpf('8.8927')
E = lambda y: 2*mp.zeta(3)*y**mp.mpf(1.5) + 2*mp.sqrt(mp.pi)*mp.zeta(2)/mp.gamma(mp.mpf(1.5))*y**mp.mpf(-0.5)
out = {"D": "D1505", "rows": []}
for chi, V, a_d1486 in ((100, 100, 2.0e3), (200, 1000, 9.9e3), (400, 1e4, 5.0e4)):
    c = mp.mpf(chi)/(4*(2*mp.pi)**3); lam = c/(2*V + c*Er); a = 1/lam
    yp = mp.mpf('13.96')*a**(mp.mpf(2)/3)
    R = c*E(yp)/V; x = lam*(E(yp) - Er)
    out['rows'].append(dict(chi=chi, V=V, c=float(c), a=float(a), a_D1486=a_d1486, y_phys=float(yp), xi_over_V=float(R), x_star=float(x)))
    print(out['rows'][-1])
json.dump(out, open('field_tests/results/D1505_regime.json', 'w'), indent=1)
