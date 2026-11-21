import math, json, sys
sys.path.insert(0, 'tools/weave_cm'); from weave_tools import weave_wino
gs = 2 / math.sqrt(3); MP = 2.435e18; ai = 27.94; fl = 9 / gs; C, w = 8e-7, 2 / 3
x = fl / ai; TR = x * 1.34e9
win = weave_wino({'T_R_GeV': TR}); passing = win['passing']
out = dict(x=x, T_R=TR, ReT_vis=ai - fl, wino=win, pairs=[], old_check=None)
pre = math.sqrt(gs / 2) * MP / 375 * 4 * (2 * math.pi) ** 3 * C / w
def M2(N, chi): return pre / chi * math.exp(-(2 * math.pi / N) * (ai - fl))
out['old_check'] = pre / 50 * math.exp(-(2 * math.pi / 7) * (28.9 - fl))   # should be ~700 GeV
def cross(fac):
    ms = sorted(float(m) for m in win['fraction']); g = [win['fraction'][str(m) if str(m) in win['fraction'] else m] - fac * win['limit'][str(m) if str(m) in win['limit'] else m] for m in ms]
    for (m0, g0), (m1, g1) in zip(zip(ms, g), zip(ms[1:], g[1:])):
        if g0 <= 0 < g1: return 1e3 * (m0 + (m1 - m0) * (-g0) / (g1 - g0))
    return 1e3 * ms[-1] if g[-1] <= 0 else None
lo, hi = 660.0, cross(1.0); hi2 = cross(2.0)
out['window_GeV'] = [lo, hi]; out['window_x2_GeV'] = [lo, hi2]
for N in (6, 7, 8):
    W0 = math.exp(-(2 * math.pi / N) * (ai - fl))
    chis = [c for c in range(2, 301) if lo and lo <= M2(N, c) <= hi]
    chis2 = [c for c in range(2, 301) if lo <= M2(N, c) <= hi2]
    out['pairs'].append(dict(N=N, W0=W0, M2_at_chi50=M2(N, 50), chi_range=[chis[0], chis[-1]] if chis else None, chi_range_x2=[chis2[0], chis2[-1]] if chis2 else None,
                             V_range=[w * c / (4 * (2 * math.pi) ** 3 * C) for c in (chis[0], chis[-1])] if chis else None))
ok = [p for p in out['pairs'] if p['chi_range'] and p['V_range'][0] >= 1e4]
out['verdict'] = 'CLOSES' if ok else ('STRAINED' if any(p['chi_range'] for p in out['pairs']) else 'BROKEN')
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/u20_chain.json', 'w'), indent=1)
