"""D1364 merge (DEVIATIONS D2): five per-w rows -> D1364_p3_mix.json in the original format."""
import json, math, sys
sys.path.insert(0, '.')
from tools.serapis_calc.shapes import E, E1hat
RHO = complex(0.5, math.sqrt(3)/2); Y10 = complex(0.5, 10.0)
k = (E(Y10) - E(RHO))/(E1hat(Y10) - E1hat(RHO))
rows = [json.load(open(f'field_tests/results/D1364_rows/w_{w}.json')) for w in (1.0, 0.75, 0.5, 0.25, 0.0)]
json.dump(dict(k=k, rows=rows), open('field_tests/results/D1364_p3_mix.json', 'w'), indent=1); print(json.dumps(rows, indent=1))
