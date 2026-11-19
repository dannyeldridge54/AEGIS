"""D1665 / Janus genesis G15 (PREREG_D1665_G15_KAPPA)."""
import json, math
n, Ng = 1.0, 12
dg = 2 / math.sqrt(n); k1 = Ng * dg ** 2 / (128 * math.pi)
y = 3.7; X2 = 2 * y; KXX = n / X2 ** 2; k2 = Ng * 1.0 / (128 * math.pi * KXX * y ** 2)
g1 = json.load(open('field_tests/results/D1637_G1_reheat.json')); m, MP, gs = g1['m_GeV'], 2.435e18, 106.75
TR = (90 / (math.pi ** 2 * gs)) ** 0.25 * math.sqrt(k1 * m ** 3 / MP)
lo, hi = 1 / (8 * math.pi), 1.0
out = dict(D='D1665', n=n, d_g=dg, kappa_gg=k1, kappa_crosscheck=k2, crosscheck_ok=abs(k1 / k2 - 1) < 1e-12, m_GeV=m, T_R_GeV=TR,
           band=[lo, hi], reading='INSIDE' if lo <= k1 <= hi else 'OUTSIDE', TR_band_D1637=[g1['TR_band']['kappa_1_over_8pi'], g1['TR_band']['kappa_1']],
           Gamma_GeV=k1 * m ** 3 / MP ** 2, H_end_GeV=math.sqrt(g1['Vinf_GeV4'] / 3) / MP)
json.dump(out, open('field_tests/results/D1665_G15_kappa.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
