import math, json
x = 0.279; TD3 = 1.34e9; lo, hi = 1.54e9, 2.09e9
out = {}
# C2: T(Gamma) ∝ sqrt(Gamma); T_vis = (G_vis/G_tot)^(1/4) * T(G_tot)
for Nh in (0, 12, 248, 496):
    gv = x**2; gt = gv + Nh / 12; Tv = (gv / gt) ** 0.25 * math.sqrt(gt) * TD3; Ttot = math.sqrt(gt) * TD3
    out['C2_Nh%d' % Nh] = dict(T_vis=Tv, T_total_equiv=Ttot, in_target=lo <= Tv <= hi, hidden_energy_share=1 - gv / gt)
# C1: gaugino suppression (m12/m_phi)^2
for m12 in (660, 1850): out['C1_m%d' % m12] = dict(Gamma_ratio=(m12 / 4.9e12) ** 2)
# C3: amplitude needed a = T_target/TD3 (T ∝ amplitude); theta*(dfvis/Re f) = a - x
out['C3_amplitude_needed'] = [lo / TD3, hi / TD3]; out['C3_extra_amplitude_needed'] = [lo / TD3 - x, hi / TD3 - x]
json.dump(out, open('field_tests/results/d2009_tr_channels.json', 'w'), indent=1); print(json.dumps(out, indent=1))
