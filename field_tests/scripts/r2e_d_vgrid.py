import sys, math, numpy as np
sys.path.insert(0, 'tools/janus_astro'); sys.path.insert(0, 'field_tests/scripts')
from r2c_b_alls import run
from r2e_b_gstar import omega
from r2e_a_alpha import XS
lx = np.log(XS); Ms = [2800.0, 3000.0]; om = {}
for n in (40, 80, 160):
    r = run(Ms, XS, [n])
    for M in Ms:
        R = np.array([r[(M, x, n)][0] for x in XS])
        om[(M, n)] = omega(M, lambda x, R=R: float(np.interp(math.log(min(max(x, 3.0), 3e4)), lx, R)))[0]
        print(f"n={n} M={M/1e3:.1f}: Oh2={om[(M, n)]:.5f}", flush=True)
Q = max(abs(om[(M, 160)]/om[(M, 40)] - 1) for M in Ms)
print(f"Q = {Q:.4%} -> {'MATTERS' if Q > 0.01 else 'RULED OUT'}; n=40 vs R2e-b: {om[(2800.0,40)]:.4f}/0.1048, {om[(3000.0,40)]:.4f}/0.1195")
