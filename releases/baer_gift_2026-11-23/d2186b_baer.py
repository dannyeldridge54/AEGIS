import math, json, csv
hbar = 6.582119569e-25; mP = 2.435e18; mt = 173.0
def fa_min(m, ms, tmax, alpha, eps=1.0):
    lam2 = hbar*128*math.pi**2*ms**4/(3*alpha*eps**2*m**5*tmax); return math.sqrt(lam2)*mP
rows = []; R = {}
for case, alpha, epsf in (('A_UDD_baryonic', 1/128, lambda ms: mt/ms), ('B_LQD_LLE_leptonic', 1/30, lambda ms: 1.0)):
    for ms in (5e3, 10e3, 30e3, 60e3, 130e3, 160e3):
        for m in (670., 693., 1000.):
            f = fa_min(m, ms, 0.1, alpha, epsf(ms)); lo, hi = f/math.sqrt(10), f*math.sqrt(10)
            rows.append([case, ms/1e3, m, f'{f:.3e}', f'{lo:.3e}', f'{hi:.3e}', 'yes' if hi <= 5e12 else ('partly' if lo <= 5e12 else 'no')])
            R[f'{case}_{int(ms/1e3)}_{int(m)}'] = dict(fa_min=f, band=[lo, hi])
json.dump(R, open('field_tests/results/d2186b_baer_rpv_wino.json', 'w'), indent=1)
with open('field_tests/results/d2186b_baer_rpv_wino.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['operator_case', 'm_soft_TeV', 'm_wino_GeV', 'fa_min_GeV_tau_le_0.1s', 'band_low', 'band_high', 'inside_fa_le_5e12_window']); w.writerows(rows)
for r in rows:
    if r[2] == 693.0: print(r)
