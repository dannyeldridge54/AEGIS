"""D1654 / Janus genesis G6b (PREREG_D1654_G6B_CHANNELS_NEFF)."""
import json
gV, gV0 = 106.75, 3.909
def scen(f, gD, gD0=2.0):
    xiR = (f * gV / gD) ** 0.25
    xi0 = xiR * (gD / gD0) ** (1 / 3) / (gV / gV0) ** (1 / 3)
    dn = gD0 / 1.75 * 2.75 ** (4 / 3) * xi0 ** 4
    zA = (3.044 + dn - 2.86) / 0.13; zL = (3.044 + dn - 2.990) / 0.070; zmax = max(zA, zL)
    return dict(f=f, xi_R=xiR, xi_today=xi0, dneff=dn, pull_ACT=zA, pull_2603=zL,
                reading='CONSISTENT' if zmax <= 2 else ('TENSION' if zmax <= 3 else 'EXCLUDED'), SO_sigmas=dn / 0.055)
S = dict(S1_democratic=scen(5.5 / 106.75, 5.5), S2_gauge=scen(1 / 12, 5.5), S3_gauge_higgs=scen(1 / 16, 5.5), S4_dark_QCD=scen(9 / 12, 21.5))
dn_max = 2.990 + 2 * 0.070 - 3.044
f_max = {k: dn_max / v['dneff'] * v['f'] for k, v in S.items()}
out = dict(D='D1654', scenarios=S, dneff_max_2sigma_2603=dn_max, f_max_2sigma=f_max,
           D1646_caseB_rescored=S['S1_democratic']['reading'])
json.dump(out, open('field_tests/results/D1654_G6b_channels.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
