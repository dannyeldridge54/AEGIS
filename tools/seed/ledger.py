#!/usr/bin/env python3
"""Budget ledger (Danny 07:51-07:53): the root charge (set by the O-planes) is split node by node; every node's brane half and
mirror-image half are shown; the hidden rings close the budget; the 'synapses' are intersection numbers (= chiral particles).
Bookkeeping display on the D2083 unified PS model (chi = (1,3,2)); no scored claim."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seed_v3 as s
from fractions import Fraction as Fr
chi = (Fr(1), Fr(3), Fr(2))
VIS = [('a: U(4) colour+lepton', 8, (-1, -1, 0, -1, -1, -1)), ('b: U(2)_L weak', 4, (-1, 0, -3, -1, 1, 0)), ('c: U(2)_R', 4, (0, -1, -3, -1, -1, -1))]
S = [w for w in s.ALL if s.zprod(w, chi)[1] == 0 and s.zprod(w, chi)[0] > 0]
def first_completion(R, par, i=0, acc=()):
    if i == len(S): return acc if (all(r == 0 for r in R) and par == (0, 0, 0, 0)) else None
    X, P = s.X(S[i]), s.parity(S[i]); W = lambda x: x[0] - chi[1]*chi[2]*x[1] - chi[0]*chi[2]*x[2] - chi[0]*chi[1]*x[3]; c = 0
    while 2*c*W(X) <= W(R):
        r = first_completion(tuple(a - 2*c*b for a, b in zip(R, X)), tuple((p + c*q) % 2 for p, q in zip(par, P)), i + 1, acc + (((2*c, S[i]),) if c else ()))
        if r is not None: return r
        c += 1
    return None
fmt = lambda v: '(' + ', '.join('%5s' % str(x) for x in v) + ')'
print('ROOT budget (O-plane charge, the space itself):          ', fmt(s.TGT))
R = s.TGT
for name, N, w in VIS:
    share = tuple(N*x for x in s.X(w)); half = tuple(x/2 for x in share)
    print('  node %-24s N=%d  share %s  = brane %s + mirror %s' % (name, N, fmt(share), fmt(half), fmt(half)))
    R = tuple(r - x for r, x in zip(R, share))
print('  left for the hidden rings:                              ', fmt(R))
H = first_completion(R, s.kcheck([(N, w) for _, N, w in VIS]))
for N, w in H:
    share = tuple(N*x for x in s.X(w)); R = tuple(r - x for r, x in zip(R, share))
    print('  hidden ring N=%-2d wrap %s  share %s' % (N, s.tor(w) and tuple(str(x) for pair in s.tor(w) for x in pair), fmt(share)))
print('  remainder after all nodes:                              ', fmt(R), '<- must be zero (conservation)')
print('\nSYNAPSES (intersection numbers = chiral particles living where two nodes meet):')
nodes = VIS + [('hidden%d' % k, N, w) for k, (N, w) in enumerate(H)]
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        I, Ip = s.inter(nodes[i][2], nodes[j][2]), s.inter(nodes[i][2], nodes[j][2], True)
        if I or Ip: print('  %-24s <-> %-24s  direct %3s   via mirror %3s' % (nodes[i][0], nodes[j][0], I, Ip))
