import json, mpmath as mp
src = open('field_tests/scripts/d1506/phys_ns.py').read().split('out = {')[0]
G = {}; exec(src, G)
# replace E32 by the pure y^{3/2} zero mode and E_rho by 0: x = lambda*2zeta(3)*y^{3/2}
z3 = 2*mp.zeta(3)
G['E32'] = lambda y, x=None: z3*y**mp.mpf(1.5)
G['Er'] = mp.mpf(0)
p = G['point'](0.375, 1.5e-6, 1.0); print('pure-y^1.5, lambda=1:', json.dumps(p), flush=True)
