#!/usr/bin/env python3
"""D2082 report item (locked): inequivalent completed visible pairs across the whole chi grid (the same model appears at many chi points).
It also confirms the CSU fillers are SUSY at the control point. Scored counts are unchanged."""
import itertools, sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seed_v3 as s
from fractions import Fraction as Fr
fill = [w for N, w in s.CSU if w in s.PROBES]
print('CSU fillers SUSY at (1,3,2):', all(s.zprod(w, (Fr(1), Fr(3), Fr(2)))[1] == 0 and s.zprod(w, (Fr(1), Fr(3), Fr(2)))[0] > 0 for w in fill))
tot = {}; per = {}
for chi in itertools.product(s.GRID, repeat=3):
    r = s.run_chi(chi)
    for k in r['completed_keys']: tot.setdefault(k, set()).add(chi)
print('inequivalent completed visible pairs (A, B, N_A) across grid:', len(tot), '| seen at >1 chi:', sum(len(v) > 1 for v in tot.values()))
