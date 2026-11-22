#!/usr/bin/env python3
"""D1997 powered calibration of confirmed false alarms (PREREG_D1997_calib10x.md)."""
import json, math, os, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def work(seeds):
    import loom_rt5 as R
    cal = json.load(open('field_tests/results/d1987_calibration.json'))['start']; n = c = ret = 0
    for sd in seeds:
        o = R.engine(7.0, sd, events=False, calib=True, pbt=False, live_cfg=(cal['k'], cal['h']), vclock=True, dt=R.VDT)
        c += o['confirmed_cal']; ret += o['retracted']; n += int((o['tt'] >= 2.0).sum())
    return n, c, ret
if __name__ == '__main__':
    with Pool(2) as p: res = p.map(work, [list(range(1, 51, 2)), list(range(2, 51, 2))])
    n = sum(r[0] for r in res); c = sum(r[1] for r in res); ret = sum(r[2] for r in res); N = n * 7; lam = 1e-6 * N
    pge = 1 - sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(c))   # P(K >= c)
    up = next(x / 1e3 for x in range(1, 200000) if sum(math.exp(-x / 1e3) * (x / 1e3) ** i / math.factorial(i) for i in range(c + 1)) <= 0.05) / N
    out = dict(prereg='PREREG_D1997_calib10x.md', layer_pulses=N, confirmed=c, retracted=ret, rate=c / N, upper95=up, expected_at_bar=lam, p_ge=pge, verdict='PASS' if pge >= 0.05 else 'FAIL')
    json.dump(out, open('field_tests/results/d1997_calib10x.json', 'w'), indent=1); print(out)
