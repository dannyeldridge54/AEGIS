"""JANUS tick 65: machine check of docs/JANUS_FORMULAS.md (PREREG_D1469)."""
import json, math
J = lambda f: json.load(open(f'field_tests/results/{f}.json'))
e, i = J('D1457_band_e_formula'), J('D1462_band_i_lo_formula')
fr = lambda ns, r: -2*r*(e['a'] + e['b']*(ns-0.972))
def lo(ns, r):
    q = 2*math.sqrt(2)*math.sqrt(r/2)/(1-ns); return -0.5*(1-ns)**2*q*(1+0.5*(q-1))
ft = lambda ns, r: lo(ns, r)*(i['a'] + i['b']*(ns-0.9725))
c43, c44, a42 = J('D1443_box_corners')['corners'], J('D1444_four_corners')['corners'], J('D1442_rho_second_order')['second']
rho = [('A1', 0.974393, 4.82095e-4, a42['alpha'], -9.9814e-4)]
for k, (ns, r, ex) in {'K1': (0.972710, 4.38906e-4, -9.1099e-4), 'K2': (0.974828, 4.89722e-4, -1.0144e-3), 'K3': (0.971663, 4.52911e-4, -9.4017e-4),
                       'K4': (0.973232, 4.70877e-4, -9.7704e-4), 'K5': (0.974320, 4.57135e-4, -9.4741e-4), 'K6': (0.975959, 4.76299e-4, -9.8543e-4)}.items():
    rho.append((k, ns, r, (c43 if k in c43 else c44)[k]['alpha'], ex))
na = J('D1448_tau_i_exact_plateau')['rows']
NA = [(0.97368, 4.6846e-4), (0.97415, 4.7584e-4), (0.97462, 4.8335e-4), (0.97509, 4.9100e-4), (0.97556, 4.9878e-4)]
A = []
for k, ns, r, der, ex in rho:
    A.append(dict(row=k, vac='rho', in_range=(0.969 <= ns <= 0.975 and 4.55e-4 <= r <= 5.12e-4), vs_derived=fr(ns, r)/der-1, vs_exact=fr(ns, r)/ex-1))
for (ns, r), row in zip(NA, na):
    A.append(dict(row=f"NA12 eps {row['eps_NA12']:.2e}", vac='tau_i', in_range=(0.970 <= ns <= 0.975 and 4.8e-4 <= r <= 5.7e-4),
                  vs_derived=ft(ns, r)/row['alpha']-1, vs_exact=ft(ns, r)/row['alpha_exact']-1))
partA = max(abs(x['vs_derived']) for x in A) <= 2e-3
d40, d41, d49, d67 = J('D1440_first_decider'), J('D1441_so_ns_check'), J('D1449_vac_derived'), J('D1467_beta_detect')
d52, d53, d54, d66 = J('D1452_box_derived_running'), J('D1453_band_i_derived'), J('D1454_band_e_derived'), J('D1466_beta_s')
B = [  # (card text, card low, card high, json low, json high, decimals)
 ('r significance 0.46–0.57σ', 0.46, 0.57, d40['r_official_dr1e-3']['S_lo'], d40['r_official_dr1e-3']['S_hi'], 2),
 ('SO+SPHEREx 7.7–8.0σ', 7.7, 8.0, d40['ns']['SO+SPHEREx']['sigma'], max(J('D1437_ns_sensitivity')['tension']['SO+SPHEREx'].values()), 1),
 ('SO alone 3.1–3.2σ', 3.1, 3.2, d41['tension_A1'], d41['tension_NA12'], 1),
 ('Δα_s −1.62 … −1.05e-4', -1.62e-4, -1.05e-4, d49['delta_range'][0], d49['delta_range'][1], 6),
 ('Δα_s ≤ 0.05σ SO', 0.05, 0.05, d49['max_sig_SO'], d49['max_sig_SO'], 2),
 ('band_e_audited pulls −1.39 … −1.26σ', -1.39, -1.26, d52['pull_PACTLB'][0], d52['pull_PACT'][1], 2),
 ('band_i pulls −1.39 … −1.24σ', -1.39, -1.24, d53['pull_PACTLB'][0], d53['pull_PACT'][1], 2),
 ('band_e pulls −1.40 … −1.26σ', -1.40, -1.26, d54['pull_PACTLB'][0], d54['pull_PACT'][1], 2),
 ('D1457 in-sample ≤ 0.021 %', 0.021, 0.021, e['insample_max']*100, e['insample_max']*100, 3),
 ('D1462 in ≤ 0.0071 % out ≤ 0.0103 %', 0.0071, 0.0103, i['insample_max']*100, i['oos_max']*100, 4),
 ('β_s ρ −2.860e-5, τ=i −3.126e-5', -2.860e-5, -3.126e-5, d66['rho']['beta'], d66['tau_i']['beta'], 8),
 ('β_s ≤ 0.007σ', 0.007, 0.007, max(max(v.values()) for v in d67['significance'].values()), max(max(v.values()) for v in d67['significance'].values()), 3)]
mism = []
for t, cl, ch, jl, jh, dp in B:
    tol = 0.5*10**(-dp) + 1e-15
    lo_ok = abs(round(jl, dp) - cl) <= tol or (t.startswith(('Δα_s ≤', 'β_s ≤')) and jl <= cl + tol)
    hi_ok = abs(round(jh, dp) - ch) <= tol or (t.startswith(('Δα_s ≤', 'β_s ≤')) and jh <= ch + tol)
    if not (lo_ok and hi_ok): mism.append(dict(card=t, json=[jl, jh]))
out = dict(D='D1469', partA=A, partA_pass=partA, partA_max_vs_derived=max(abs(x['vs_derived']) for x in A),
           partA_max_vs_exact=max(abs(x['vs_exact']) for x in A), partB_mismatches=mism)
out['verdict'] = 'CARD CONSISTENT' if partA and not mism else 'MISMATCHES'
json.dump(out, open('field_tests/results/D1469_card_check.json', 'w'), indent=1)
print(out['verdict'], out['partA_max_vs_derived'], out['partA_max_vs_exact']); print(json.dumps(mism, indent=1))
for x in A: print(x['row'], x['in_range'], round(x['vs_derived']*100, 4), round(x['vs_exact']*100, 4))
