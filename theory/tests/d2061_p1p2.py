import math, itertools
from fractions import Fraction as F
s, ReS = 20.15, math.sqrt(3)/2
for W in (1, 2, 3, 4, 6, 12): print('P1 W=%2d alpha_G^-1 = %.2f %s' % (W, W*s + 9*ReS, 'ok' if abs(W*s + 9*ReS - 27.94) <= 0.5 else 'FAIL'))
sets = {'Madrid (1/6,-1/2,1/2)': [F(1,6), F(-1,2), F(1,2)], 'SU5-like (-1/3,1/2)': [F(-1,3), F(1,2)], '4-stack (1/6,1/2,1/2,-1/2)': [F(1,6), F(1,2), F(1,2), F(-1,2)]}
for name, cs in sets.items():
    steps = sorted({c*c*m*m for c in cs for m in range(1, 4)})
    hit = [str(x) for x in steps if x in (F(1,12), F(1,6))]
    print('P2 %-28s single-stack steps %s -> exact 1/12 or 1/6: %s' % (name, [str(x) for x in steps], hit or 'none'))
    pair = sorted({abs(ca*cb*ma*mb) for ca, cb in itertools.combinations(cs, 2) for ma in range(1, 4) for mb in range(1, 4)})
    print('    cross terms |c_a c_b m_a m_b|:', [str(x) for x in pair][:12], '| contains 1/12:', F(1,12) in pair, '1/6:', F(1,6) in pair)
