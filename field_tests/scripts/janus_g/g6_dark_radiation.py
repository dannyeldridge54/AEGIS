"""D1646 / Janus genesis G6: Delta N_eff after democratic gravitational reheating (PREREG_D1646_G6_DARK_RADIATION)."""
import json, sys
sys.path.insert(0, '.')
from tools.genesis.genesis import mirror_dneff
gsV_R, gsV_0 = 106.75, 3.909
def xi_today(gsD_R, gsD_0): return (gsD_R / gsD_0) ** (1 / 3) / (gsV_R / gsV_0) ** (1 / 3)
def dneff_boson(gD0, xi): return gD0 / (7 / 4) * (11 / 4) ** (4 / 3) * xi ** 4
A = dict(xi=1.0, dneff=mirror_dneff(1.0))
xiB = xi_today(3.5 + 2.0, 2.0); B = dict(xi=xiB, dneff=dneff_boson(2.0, xiB))
xi_max = (0.3 / mirror_dneff(1.0)) ** 0.25; Cc = dict(xi_max=xi_max, branching_max=xi_max ** 4)
for c in (A, B): c['viable'] = c['dneff'] < 0.3; c['dYp'] = 0.0130 * c['dneff']
out = dict(D='D1646', A_full_mirror=A, B_minimal_ADM=B, C_asym_branching=Cc,
           verdict_C5=('a cold dark side needs no special branching once the dark sector is minimal' if B['viable'] else f"needs Gamma_D/Gamma_V <= {Cc['branching_max']:.3g}"))
json.dump(out, open('field_tests/results/D1646_G6_dark_radiation.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
