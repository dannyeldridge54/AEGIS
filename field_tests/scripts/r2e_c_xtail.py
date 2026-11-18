import sys, math, numpy as np
sys.path.insert(0, 'tools/janus_astro'); sys.path.insert(0, 'field_tests/scripts')
from r2c_b_alls import run
from r2e_b_gstar import omega
from r2e_a_alpha import XS
XE = sorted(XS + list(np.geomspace(3e4, 1e5, 9)[1:])); ref = {2800.0: 0.1048, 3000.0: 0.1195}
r = run(list(ref), XE, [40]); lx = np.log(XE); out = []
for M in ref:
    R = np.array([r[(M, x, 40)][0] for x in XE])
    Rf = lambda x, R=R: float(np.interp(math.log(min(max(x, 3.0), 1e5)), lx, R))
    om = omega(M, Rf)[0]; d = om/ref[M] - 1
    wlow = (1e-3*math.sqrt(1e5/4))**3*4/(3*math.sqrt(math.pi))
    out.append(f"M={M/1e3:.1f}: R_eff(3e4)={np.interp(math.log(3e4), lx, R):.3f} R_eff(1e5)={R[-1]:.3f} Oh2={om:.4f} vs R2e-b {ref[M]} (rel {d:+.4f}) -> {'MATTERS' if abs(d) > 0.01 else 'small'}; Maxwell weight v<1e-3 at x=1e5 ~{wlow:.3%}")
slope = math.log(0.1195/0.1048)/math.log(3.0/2.8)
out.append(f"Omega ~ M^{slope:.2f}; implied M_th shift ~ -(dOmega/Omega)/{slope:.2f}")
open('field_tests/results/r2e_c_xtail.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
