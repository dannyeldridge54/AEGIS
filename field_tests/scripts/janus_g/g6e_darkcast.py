"""D1664 / Janus genesis G6e (PREREG_D1664_G6E_DARKCAST). Reads DarkCast .lmt tables as data; executes nothing from them."""
import json, math, os, re, sys
import numpy as np
LIM = sys.argv[1]
MTOP = float(sys.argv[2]) if len(sys.argv) > 2 else 5.03   # D1685: top mass argument (default = D1664)
OUT = 'field_tests/results/D1664_G6e_darkcast.json' if MTOP == 5.03 else 'field_tests/results/D1685_G17_window_12p8.json'
VIS = re.compile(r'decay\s*=\s*(\[[^\]]*\]|"[^"]*")')
def meta(base):
    for cand in (base, re.sub(r'_(br\w+|prompt|displaced|combined|mumu|cs|rb|2l|2u)$', '', base)):
        p = os.path.join(LIM, cand + '.py')
        if os.path.exists(p): return open(p).read()
    return ''
used, skipped = [], []
tables = []
for f in sorted(os.listdir(LIM)):
    if not f.endswith('.lmt'): continue
    b = f[:-4]; t = meta(b)
    dm = VIS.search(t); dec = dm.group(1) if dm else ''
    ok = ('Model("dark_photon"' in t) and dec and ('none' not in dec) and ('invisible' not in t) and not b.startswith(('ATLAS', 'CMS_CMS2016', 'CMS_CMS2018'))
    if not ok: skipped.append(b); continue
    rows = [list(map(float, l.split())) for l in open(os.path.join(LIM, f)) if l.strip() and not l.startswith('#')]
    a = np.array(rows); tables.append((b, a)); used.append(b)
masses = np.geomspace(0.02, MTOP, 400); eps = np.geomspace(1e-13, 1e-2, 2000)
d57 = json.load(open('field_tests/results/D1657_G6c_massive_dp.json'))['rows']
lm = np.log10([r['m_MeV'] / 1000 for r in d57]); le = np.log10([r['eps_min_tau_1s'] for r in d57])
def floor(m):
    x = math.log10(m)
    if x <= lm[-1]: return 10 ** np.interp(x, lm, le)
    return 10 ** (le[-1] + (le[-1] - le[-2]) / (lm[-1] - lm[-2]) * (x - lm[-1]))
def interp(a, col, m):
    ms = a[:, 0]
    if m < ms.min() or m > ms.max(): return None
    return 10 ** np.interp(math.log10(m), np.log10(ms), np.log10(a[:, col]))
rows = []
for m in masses:
    allowed = eps > floor(m)
    if m <= 0.1: allowed &= ~((eps > 1e-10) & (eps < 1e-6))
    for b, a in tables:
        if a.shape[1] >= 3:
            lo, hi = interp(a, 1, m), interp(a, 2, m)
            if lo is not None and hi is not None: allowed &= ~((eps > lo) & (eps < hi))
        else:
            lo = interp(a, 1, m)
            if lo is not None: allowed &= ~(eps > lo)
    iv, start = [], None
    for k, ok in enumerate(allowed):
        if ok and start is None: start = k
        if (not ok or k == len(eps) - 1) and start is not None:
            end = k if not ok else k + 1; iv.append((float(eps[start]), float(eps[end - 1]))); start = None
    widest = max((math.log10(h / l) for l, h in iv), default=0.0)
    rows.append(dict(m_GeV=float(m), floor=float(floor(m)), intervals=iv, widest_decades=widest))
open_m = [r['m_GeV'] for r in rows if r['widest_decades'] >= 1]
edge = min(open_m) if open_m else None
def at(mg):
    r = min(rows, key=lambda r: abs(r['m_GeV'] - mg)); return dict(m=r['m_GeV'], intervals=r['intervals'], widest=r['widest_decades'])
in15 = [r for r in rows if 1.0 <= r['m_GeV'] <= MTOP]
reading = ('CLOSED' if not open_m else ('CONFIRMED' if (edge and 0.1 <= edge <= 0.9 and all(r['widest_decades'] >= 1 for r in in15)) else 'SHARPENED'))
closed_0p3_5 = [r['m_GeV'] for r in rows if 0.3 <= r['m_GeV'] <= MTOP and r['widest_decades'] < 1]
out = dict(D='D1664', mirror_commit='db9a0f66ec99946930dc263a042ec531c9576068', used=used, skipped=skipped, lower_edge_GeV=edge,
           at_0p3=at(0.3), at_1=at(1.0), at_3=at(3.0), at_5=at(5.0), closed_masses_0p3_to_5=closed_0p3_5, reading=reading, rows=rows)
out['m_top'] = MTOP
json.dump(out, open(OUT, 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('rows', 'skipped')}, indent=1, default=str)[:3000])
