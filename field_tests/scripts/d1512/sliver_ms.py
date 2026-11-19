"""D1512: exact-MS check of physical-frame DILMIX (0.1, 1.8e-6) (PREREG_D1512)."""
import json, sys, os, tempfile, time
sys.path.insert(0, '.')
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.shapes import E
al, C, lam = 0.1, 1.8e-6, 1 / 9930.9
P.E_paper = lambda x, y: E(complex(x, y), 1.5)
orig = P._egrid
def _eg(model, lam_, ymax, npts):
    ph, x = orig(model, lam_, ymax, npts); Pp = al*x/(1 + x) + (1 - al)*(1 - 1/(1 + x)**2); return ph, Pp/(1 - Pp)
P._egrid = _eg
_b = P.build
def _build(model='serapis_e', C=1.15e-6, lam=1.0, ymax=2e5, npts=8000):
    mm, V, dV, p0 = _b(model, C, lam, ymax, npts); ph, _ = P._egrid(model, lam, ymax, npts); lo, hi = 10, len(ph) - 5
    for _ in range(16):
        mid = (lo + hi)//2; ne = P.Background(V, dV, ph[mid]).Nend
        if ne is None or ne > 140: hi = mid
        else: lo = mid
        if ne is not None and 100 <= ne <= 200: return mm, V, dV, ph[mid]
    return mm, V, dV, ph[lo]
P.build = _build
os.environ['AEGIS_CACHE'] = tempfile.mkdtemp(); P._EGRID.clear(); t = time.time()
r = P.predict('serapis_e', C=C * lam, TR=8.94e8, lam=lam)
row = dict(alpha=al, C=C, lam=lam, ns=float(r['ns']), r=float(r['r']), alpha_s=float(r['alpha_s']), Nstar=float(r['Nstar']), seconds=round(time.time() - t, 1),
           sr_ns=0.9719704911347419, sr_r=0.0005462294458971985)
row['d_ns'] = row['ns'] - row['sr_ns']; row['d_r_rel'] = row['r'] / row['sr_r'] - 1
row['agree'] = abs(row['d_ns']) <= 5e-4 and abs(row['d_r_rel']) <= 0.02
row['in_band'] = bool(0.969 <= row['ns'] <= 0.975 and 4.55e-4 <= row['r'] <= 5.7e-4)
print(json.dumps(row), flush=True); json.dump(row, open('/tmp/claude-0/-home-claude/e1153314-178b-5884-8c19-291220701fba/scratchpad/D1512_sliver_ms.json', 'w'), indent=1)
