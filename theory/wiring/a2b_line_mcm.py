import sys, math; sys.path.insert(0, '.')
from tools.janus_astro import jfactor as J
Jein = J.J_route_B(J.normalise(J.einasto(20.0, 0.17), 0.39, 8.5), 8.5)
cases = {'McMillan17 NFW': (19.60, 0.385, 8.21), 'MWPotential2014 NFW': (16.0, 0.286, 8.0)}
out = [f"J (HESS Einasto benchmark) = {Jein:.4e} (module units)"]
for k, (rs, rho, r0) in cases.items():
    Jm = J.J_route_B(J.normalise(J.nfw(rs), rho, r0), r0); sc = math.sqrt(Jein/Jm)
    for lab, f0 in (('LO', 0.355), ('NLO', 0.391)):
        fm = f0*sc
        out.append(f"{k} {lab}: J ratio model/HESS = {Jm/Jein:.3f}; f_max = {fm:.3f} (one-loop {fm*math.sqrt(3):.2f}-{fm*2:.2f}) -> {'PASS' if fm >= 0.26 else 'FAIL'} vs 0.26")
open('field_tests/results/a2b_line_mcm.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
