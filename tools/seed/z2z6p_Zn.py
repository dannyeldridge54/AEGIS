#!/usr/bin/env python3
"""D2120: discrete Z_n from the P2 GS matrix of the Table-27 PS model."""
import itertools
from fractions import Fraction as Fr
C = [[0,0,0,0,2],[0,0,0,0,0],[0,0,0,-2,0],[2,0,-2,-3,-1],[0,0,0,2,-2],[0,0,0,0,-2],[0,0,0,0,0],[0,0,0,2,0],[-2,2,0,3,1],[0,0,0,-2,2],
     [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,2,-1,-1,0],[-2,0,-2,2,0]]   # c-values (P2 == paper, D2119 R1-9)
N = [4, 2, 2, 2, 2]
chiral = {'ab': (1,-1,0,0,0), "ab'": (1,1,0,0,0), 'ac': (-1,0,1,0,0), "ac'": (-1,0,-1,0,0), 'bc': (0,1,-1,0,0), 'bd': (0,1,0,-1,0),
          "bd'": (0,-1,0,-1,0), "be'": (0,-1,0,0,-1), 'cd': (0,0,-1,1,0), "cd'": (0,0,1,1,0), "ce'": (0,0,1,0,1)}
for dbl in (False, True):
    M = [[N[x]*C[r][x]*(2 if dbl else 1) for x in range(5)] for r in range(15)]
    print('== doubling' if dbl else '== raw c (integer as given)')
    for n in range(2, 13):
        sols = [k for k in itertools.product(range(n), repeat=5) if any(k) and all(sum(k[x]*M[r][x] for x in range(5)) % n == 0 for r in range(15))]
        # keep only generators not reducible to a smaller Z_m (gcd with n)
        prim = [k for k in sols if __import__('math').gcd(n, *k) == 1]
        if prim:
            k = prim[0]; q = {s: sum(a*b for a, b in zip(k, Q)) % n for s, Q in chiral.items()}
            yuk = (q['ac'] + q['bc'] + q['ab']) % n
            print(' Z_%d: %d primitive generators, e.g. k=%s | chiral charges %s | Yukawa(ac,bc,ab) charge %d' % (n, len(prim), k, q, yuk))
