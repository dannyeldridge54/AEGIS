"""D2165: massless U(1) combinations of the published Z6-II model (Stueckelberg kernel)."""
import os, sys, json, sympy as sp
sys.path.insert(0, os.path.dirname(__file__)); import z6p as Z
S = {'a': (3, [0, 0, 1, -1, 0, 1, -1, 0, 0, 1, -1, 0]), 'b': (2, [3, 0, 3, 0, -3, 0, -3, 0, 0, 0, 0, 0]),
     'c': (1, [1, 1, 0, 0, 0, 0, 3, -3, 0, 0, -3, 3]), 'd': (1, [0, 0, 3, -3, 0, -1, 1, 0, 0, -1, 1, 0]),
     'e': (1, [0, 0, 3, -3, 3, 0, 0, 3, -3, 0, 0, -3])}
names = list(S)
cols = [[S[k][0]*(x - y) for x, y in zip(S[k][1], Z.image_ABa(S[k][1]))] for k in names]
M = sp.Matrix(cols).T           # 12 x 5
ker = M.nullspace()
out = {'rank': M.rank(), 'massless_dim': len(ker), 'basis': [[str(v) for v in b] for b in ker]}
# chiral spectrum charges to identify hypercharge: try Y = sum x_a Q_a giving SM values on the a-b (Q_L) sector etc.
ch = Z.chiral(S, Z.image_ABa, Z.O6_ABa)
out['chiral'] = {f'{k[0]}{k[1]}': (str(v)) for k, v in ch.items() if v not in (0, 0.0)}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', '..', 'field_tests', 'results', 'd2165_stueckelberg.json'), 'w'), indent=1)
