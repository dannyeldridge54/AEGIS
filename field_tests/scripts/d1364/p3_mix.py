"""D1364 (locked PREREG_D1364_p3_mix.md): s=1/s=2 shape mix through the full SERAPIS-E pipeline."""
import json, math, os, sys, tempfile, time
sys.path.insert(0, '.')
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.shapes import E, E1hat
RHO = complex(0.5, math.sqrt(3)/2); Y10 = complex(0.5, 10.0)
k = (E(Y10) - E(RHO))/(E1hat(Y10) - E1hat(RHO))
out = dict(k=k, rows=[])
WS = [float(a) for a in sys.argv[1:]] or [1.0, 0.75, 0.5, 0.25, 0.0]
os.makedirs('field_tests/results/D1364_rows', exist_ok=True)
for w in WS:
    os.environ['AEGIS_CACHE'] = tempfile.mkdtemp(); P._EGRID.clear()
    P.E_paper = (lambda w_: (lambda x, y: (1 - w_)*k*E1hat(complex(x, y)) + w_*E(complex(x, y))))(w)
    t = time.time(); r = P.predict('serapis_e', C=1.25e-6, TR=8.94e8)
    row = dict(w=w, ns=float(r["ns"]), r=float(r["r"]), alpha_s=float(r["alpha_s"]), Nstar=float(r["Nstar"]), seconds=round(time.time() - t, 1),
               in_band=bool(0.969 <= r['ns'] <= 0.975 and 4.55e-4 <= r['r'] <= 5.7e-4))
    out['rows'].append(row); print(json.dumps(row), flush=True)
    json.dump(row, open(f'field_tests/results/D1364_rows/w_{w}.json', 'w'))
if not sys.argv[1:]: json.dump(out, open('field_tests/results/D1364_p3_mix.json', 'w'), indent=1)
