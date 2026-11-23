"""D2170: tree-level alpha_3/alpha_2 at M_s from cycle volumes of the published Z6-II stacks vs the MSSM-run requirement."""
import math, json, os
from fractions import Fraction as Fr
S = {'a': [0, 0, 1, -1], 'b': [3, 0, 3, 0], 'c': [1, 1, 0, 0], 'd': [0, 0, 3, -3], 'e': [0, 0, 3, -3]}
rho = Fr(1, 2)
V = {k: (P + Q) - Fr(2, 3)*rho*(Vv - U) for k, (P, Q, U, Vv) in S.items()}
R_der = float(V['b'] / V['a'])
a3 = 0.1180; s2w = 0.2312; aem = 1/127.95; a2 = aem/s2w
Ms, MZ = 1e16, 91.1876; t = math.log(Ms/MZ)/(2*math.pi)
inv3 = 1/a3 + 3*t; inv2 = 1/a2 - 1*t        # 1/alpha(mu) = 1/alpha(MZ) - (b/2pi) ln(mu/MZ), b3 = -3, b2 = +1
R_need = inv2/inv3                            # alpha_3/alpha_2 = (1/alpha_2)/(1/alpha_3)
out = dict(volumes={k: str(v) for k, v in V.items()}, R_derived=R_der, R_needed=R_need, inv_alpha3_Ms=inv3, inv_alpha2_Ms=inv2,
           ln_ratio=math.log(R_der/R_need))
r = abs(out['ln_ratio']); out['verdict'] = 'DERIVED' if r < math.log(1.15) else ('NEEDS THRESHOLDS' if r < math.log(3) else 'FAR OFF')
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', '..', 'field_tests', 'results', 'd2170_tree_couplings.json'), 'w'), indent=1)
