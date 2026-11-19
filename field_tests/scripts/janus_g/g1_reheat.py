"""D1637 / Janus genesis G1: inflaton mass at rho and gravitational-decay T_R for the final SERAPIS equation (PREREG_D1637_G1_REHEAT)."""
import json, math, sys
sys.path.insert(0, '.')
import mpmath as mp
from tools.serapis_calc import p3s
from tools.serapis_calc.nstar import MP, AS
C, D, TR0, G = 8e-7, 10, 8.94e8, 106.75
o0 = p3s.point(C=C, D=D, TR=TR0)
b = math.sqrt(D - 2) / 2
phis = math.log(o0['y_star']) / b
Vs_over_Vinf = float(p3s.V(mp.mpf(phis), C, D))
Vstar = 1.5 * math.pi ** 2 * AS * o0['r'] * MP ** 4
Vinf = Vstar / Vs_over_Vinf                                   # GeV^4
phr = mp.log(p3s.YRHO) / b
V0 = float(p3s.V(phr, C, D)); V1 = float(mp.diff(lambda p: p3s.V(p, C, D), phr, 1)); V2 = float(mp.diff(lambda p: p3s.V(p, C, D), phr, 2))
m = math.sqrt(V2 * Vinf / MP ** 2)                            # canonical phi in units of M_P
def TR_of(kap):
    Gam = kap * m ** 3 / MP ** 2
    return (90 / (math.pi ** 2 * G)) ** 0.25 * math.sqrt(Gam * MP)
band = {'kappa_1_over_8pi': TR_of(1 / (8 * math.pi)), 'kappa_1': TR_of(1.0)}
lo, hi = band['kappa_1_over_8pi'] / 10, band['kappa_1'] * 10
verdict = 'CONSISTENT' if lo <= TR0 <= hi else 'TENSION'
shifts = {}
for k, T in band.items():
    o = p3s.point(C=C, D=D, TR=T)
    shifts[k] = {'TR': T, 'Nstar': o['Nstar'], 'ns': float(o['ns']), 'r': float(o['r']),
                 'dN': o['Nstar'] - o0['Nstar'], 'dns': float(o['ns']) - float(o0['ns']), 'dns_over_SO': (float(o['ns']) - float(o0['ns'])) / 0.002}
out = {'D': 'D1637', 'C': C, 'Dim': D, 'TR_assumed': TR0, 'base': {'ns': float(o0['ns']), 'r': float(o0['r']), 'Nstar': o0['Nstar'], 'y_star': o0['y_star']},
       'V_star_over_Vinf': Vs_over_Vinf, 'Vinf_GeV4': Vinf, 'Vinf_quarter_GeV': Vinf ** 0.25,
       'at_rho': {'V_over_Vinf': V0, 'Vp': V1, 'Vpp_over_Vinf_MP2': V2}, 'm_GeV': m, 'm_over_H_star': m / math.sqrt(Vstar / (3 * MP ** 2)),
       'TR_band': band, 'pass_window': [lo, hi], 'ratio_assumed_to_kappa1': TR0 / band['kappa_1'], 'verdict': verdict, 'shifts': shifts}
json.dump(out, open('field_tests/results/D1637_G1_reheat.json', 'w'), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
