"""D1661 / Janus genesis G13 (PREREG_D1661_G13_NEFF_SCOPE)."""
import json, sys
sys.path.insert(0, '.')
from tools.genesis.genesis import mirror_dneff
k = mirror_dneff(1.0); mp = 0.93827; R = 0.1200 / 0.02237
def row(dn):
    x4 = dn / k; return dict(dneff_max=dn, xi_max=x4 ** 0.25, xi4=x4, preference_visible_to_dark=1 / x4, D1648_mDM_GeV=R * mp / x4)
out = dict(D='D1661', coeff=k, old_0p3=row(0.3), new_2603=row(2.990 + 2 * 0.070 - 3.044), new_ACT=row(2.86 + 2 * 0.13 - 3.044),
           D1649_b=dict(massless_dneff=0.2062890517311545, massless_allowed=0.2062890517311545 <= 2.990 + 2 * 0.070 - 3.044, massive='dN_eff ~ 0 (D1657/D1659) -> allowed'))
json.dump(out, open('field_tests/results/D1661_G13_neff_scope.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
