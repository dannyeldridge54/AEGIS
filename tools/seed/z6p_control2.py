"""D2146 control 2: regenerate all 5 published branes (Appendix D.1 wrapping + Table 13 sigma, tau) and check SUSY at rho = 1/2."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import z6p as Z
from fractions import Fraction as Fr
H = Fr(1, 2)
W = {'a': (1, -1, 1, 0, 0, 1), 'b': (1, 1, 2, -1, 1, 1), 'c': (1, -1, -1, 2, 1, 0), 'd': (1, 1, 1, -2, 0, 1), 'e': (1, 1, 1, -2, 0, 1)}   # DEV-1: Appendix D.1 m1 sign typo
SIG = {'a': (H, 0, H, 0), 'b': (H, 0, 0, 0), 'c': (H, 0, 0, H), 'd': (0, 0, H, 0), 'e': (H, 0, 0, 0)}
TAU = {'a': (0, 1, 1), 'b': (1, 1, 0), 'c': (1, 1, 1), 'd': (0, 1, 1), 'e': (0, 1, 0)}
PUB = {'a': [0, 0, 1, -1, 0, 1, -1, 0, 0, 1, -1, 0], 'b': [3, 0, 3, 0, -3, 0, -3, 0, 0, 0, 0, 0], 'c': [1, 1, 0, 0, 0, 0, 3, -3, 0, 0, -3, 3],
       'd': [0, 0, 3, -3, 0, -1, 1, 0, 0, -1, 1, 0], 'e': [0, 0, 3, -3, 3, 0, 0, 3, -3, 0, 0, -3]}
res = {}
for k in W:
    c = Z.cycle(W[k], SIG[k], TAU[k]); res[k] = dict(generated=c, published=PUB[k], match=c == PUB[k], susy=bool(Z.susy_ABa(c, H)))
res['PASS'] = all(v['match'] and v['susy'] for v in res.values() if isinstance(v, dict))
print(json.dumps(res, indent=1)); json.dump(res, open(os.path.join(os.path.dirname(__file__), 'z6p_control2_dev1.json'), 'w'), indent=1)
