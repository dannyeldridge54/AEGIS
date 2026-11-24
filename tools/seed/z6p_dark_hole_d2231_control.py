import os, sys, json, itertools, collections, numpy as np
HERE = '/home/claude/aegis/tools/seed'; sys.path.insert(0, HERE); os.environ['RHO'] = '1/2'
src = open(os.path.join(HERE, 'z6p_scan_d2230.py')).read().split('def oddv(')[0]
g = dict(__file__=os.path.join(HERE, 'z6p_scan_d2230.py'), __name__='c'); exec(src, g)
FR, BULKS, img, O6 = g['FR'], g['BULKS'], g['img'], g['O6']; Z = g['Z']
from fractions import Fraction as Fr
H = Fr(1, 2)
W = {'a': (1, -1, 1, 0, 0, 1), 'b': (1, 1, 2, -1, 1, 1), 'c': (1, -1, -1, 2, 1, 0), 'd': (1, 1, 1, -2, 0, 1), 'e': (1, 1, 1, -2, 0, 1)}
SIG = {'a': (H, 0, H, 0), 'b': (H, 0, 0, 0), 'c': (H, 0, 0, H), 'd': (0, 0, H, 0), 'e': (H, 0, 0, 0)}
TAU = {'a': (0, 1, 1), 'b': (1, 1, 0), 'c': (1, 1, 1), 'd': (0, 1, 1), 'e': (0, 1, 0)}
C = {k: np.array(Z.cycle(W[k], SIG[k], TAU[k]), dtype=float) for k in W}
base = sum(N * (C[k] + np.array(img(list(C[k])))) for k, N in (('a', 3), ('b', 2), ('c', 1), ('d', 1)))
R = tuple(int(round(x)) for x in 4 * np.array(O6) - base)
blocks = [(tuple(h), tuple(int(round(v)) for v in (np.array(h) + np.array(img(h))))) for b in BULKS for h in FR[b]]
vecs = set(v for _, v in blocks); one = {tuple(N * np.array(v)) for v in vecs for N in range(1, 7)}
e = tuple(int(round(x)) for x in C['e'] + np.array(img(list(C['e']))))
print('published e in blocks:', e in vecs, ' residual found as one-stack sum:', R in one, ' R == e:', R == e)
