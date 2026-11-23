import math, json
hbar = 6.582119569e-25; mP = 2.435e18; a = 1/128
def tau(m, ms, fa): lam = fa/mP; G = 3*a*lam**2*m**5/(128*math.pi**2*ms**4); return hbar/G
def fa_min(m, ms, tmax):   # tau ∝ fa^-2  -> closed form
    lam2 = hbar*128*math.pi**2*ms**4/(3*a*m**5*tmax); return math.sqrt(lam2)*mP
R = {'grid': [], 'fa_min': {}}
for ms in (5e3, 10e3, 30e3, 60e3, 130e3, 160e3):
    for m in (670., 693., 1000.):
        k = f'{int(ms/1e3)}TeV_{int(m)}GeV'
        f01, f1 = fa_min(m, ms, 0.1), fa_min(m, ms, 1.0)
        R['fa_min'][k] = dict(m_soft_TeV=ms/1e3, m_chi_GeV=m, fa_min_tau_0p1s=f01, fa_min_tau_1s=f1,
                              fa_min_tau_0p1s_band=[f01/math.sqrt(5), f01*math.sqrt(5)], inside_axion_window_upper_5e12=f01 <= 5e12)
        for e in [9 + 0.25*i for i in range(25)]:
            R['grid'].append(dict(m_soft_TeV=ms/1e3, m_chi_GeV=m, log10_fa=e, tau_s=tau(m, ms, 10**e)))
w = R['fa_min']['130TeV_693GeV']; w2 = R['fa_min']['160TeV_693GeV']
R['headline'] = dict(minisplit_130TeV=dict(fa_min_0p1s=w['fa_min_tau_0p1s'], band=w['fa_min_tau_0p1s_band']),
                     minisplit_160TeV=dict(fa_min_0p1s=w2['fa_min_tau_0p1s'], band=w2['fa_min_tau_0p1s_band']),
                     their_upper_edge=5e12)
json.dump(R, open('field_tests/results/d2186_baer_rpv_wino.json', 'w'), indent=1)
for k, v in R['fa_min'].items(): print(k, f"{v['fa_min_tau_0p1s']:.2e}", f"{v['fa_min_tau_1s']:.2e}", v['inside_axion_window_upper_5e12'])
