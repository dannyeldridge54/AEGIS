"""D1659 / Janus genesis G6d (PREREG_D1659_G6D_DP_STRIP)."""
import json, math
import numpy as np
r = json.load(open('field_tests/results/D1657_G6c_massive_dp.json'))['rows']
lm = np.log10([x['m_MeV'] for x in r]); le = np.log10([x['eps_min_tau_1s'] for x in r])
def eps_min(m):  # log-log interpolation / extrapolation of D1657's floor
    return 10 ** np.interp(math.log10(m), lm, le) if math.log10(m) <= lm[-1] else 10 ** (le[-1] + (le[-1] - le[-2]) / (lm[-1] - lm[-2]) * (math.log10(m) - lm[-1]))
def bands(m):
    b = [(1e-3, 1.0)]                       # colliders (0.01-10 GeV; also caps the window)
    if m <= 3000: b.append((1e-7, 1e-3))    # beam dumps
    if m <= 100: b.append((1e-10, 1e-6))    # SN1987A
    return b
def subtract(lo, hi, bs):
    iv = [(lo, hi)]
    for a, c in bs:
        new = []
        for x, y in iv:
            if c <= x or a >= y: new.append((x, y)); continue
            if x < a: new.append((x, a))
            if c < y: new.append((c, y))
        iv = new
    return [(x, y) for x, y in iv if y > x]
rows = []
for m in (2, 10, 50, 100, 300, 1000, 3000, 5000):
    lo = float(eps_min(m)); iv = subtract(lo, 1e-3, bands(m))
    out_iv = [dict(eps_lo=x, eps_hi=y, decades=math.log10(y / x), marginal=math.log10(y / x) < math.log10(3)) for x, y in iv]
    rows.append(dict(m_MeV=m, eps_floor=lo, bands=bands(m), open=out_iv, OPEN=any(i['decades'] >= 1 for i in out_iv)))
out = dict(D='D1659', rows=rows, allowed=any(x['OPEN'] for x in rows), open_masses=[x['m_MeV'] for x in rows if x['OPEN']])
json.dump(out, open('field_tests/results/D1659_G6d_dp_strip.json', 'w'), indent=1)
for x in rows: print(x['m_MeV'], '%.2g' % x['eps_floor'], [('%.2g' % i['eps_lo'], '%.2g' % i['eps_hi'], round(i['decades'], 2)) for i in x['open']], x['OPEN'])
print('allowed', out['allowed'], out['open_masses'])
