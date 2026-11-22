#!/usr/bin/env python3
"""Seed engine v1 (D2079): tiniest seed, then rings spinning outward; hard filters -> 2-number fit -> joint held-out goalposts.
Run: python3 seed_v1.py  (prints a line per ring and writes seed_v1_results.json)"""
import itertools, json, math, os
import numpy as np
from fractions import Fraction as Fr
inv2, invY, as0, das, MSMIN, TOL = 29.59, 98.37, 0.1180, 0.0009, 4e15, 0.05
b3, b2, bY = -3.0, 1.0, 11.0
RINGS = [(1, [1]), (2, [0.5, 1, 2]), (3, [1/3, 0.5, 1, 2, 3]), (4, [0.25, 1/3, 0.5, 1, 2, 3, 4]), (6, [0.2, 0.25, 1/3, 0.5, 1, 2, 3, 4, 5])]
FORKS = list(itertools.product([Fr(1), Fr(1, 2)], [Fr(1), Fr(1, 2)], [Fr(1), Fr(1, 3)], [1, -1]))
def stacks(b1, bb2, rho, eps, na2, nb1, nd2):
    nc1 = (bb2/(2*b1))*(na2 + 3*rho*nd2)
    if nc1.denominator != 1: return None
    if 3*Fr(na2)/(rho*b1) + 2*Fr(nb1)/bb2 + Fr(nd2)/b1 > 16: return None
    return {'a': [(1/b1, 0), (na2, eps*bb2), (1/rho, Fr(1, 2))], 'b': [(nb1, -eps*b1), (1/bb2, 0), (1, 3*rho/2)],
            'c': [(nc1, 3*rho*eps*b1), (1/bb2, 0), (0, 1)], 'd': [(1/b1, 0), (nd2, -bb2*eps/rho), (1, 3*rho/2)]}, int(nc1)
def ring(nmax, grid, forks):
    G = np.array(list(itertools.product(grid, repeat=3)))           # all radii triples at once (vectorised lens spin)
    tot = phys = g2 = joint = near = win = 0; earned = set(); examples = []
    for f in forks:
        for na2, nb1, nd2 in itertools.product(range(-nmax, nmax + 1), repeat=3):
            r = stacks(*f, na2, nb1, nd2)
            if r is None: continue
            S, nc1 = r; tot += len(G); V = {}; ok = np.ones(len(G), bool)
            for k, st in S.items():
                v = np.ones(len(G)); ang = np.zeros(len(G))
                for i, (n, m) in enumerate(st):
                    n, m = float(n), float(m); v *= np.sqrt(n*n + (m*G[:, i])**2); ang += np.arctan2(m*G[:, i], n)
                V[k] = v; dev = np.abs((ang + math.pi) % (2*math.pi) - math.pi); ok &= (dev <= TOL) & (v > 0)   # SUSY filter
            if not ok.any(): continue
            VY = V['a']/6 + V['c']/2 + V['d']/2; det = V['b']*bY/(2*math.pi) - VY*b2/(2*math.pi)
            K = (inv2*bY/(2*math.pi) - invY*b2/(2*math.pi))/det; L = (V['b']*invY - VY*inv2)/det
            P = ok & (K > 0) & (L > 0) & (L < 38.8); phys += P.sum()
            inv3 = K*V['a'] + b3/(2*math.pi)*L; P &= inv3 > 0
            al = np.where(P, 1/np.where(inv3 > 0, inv3, 1), np.nan); Ms = 91.19*np.exp(np.where(P, L, 0))
            G2 = P & (Ms >= MSMIN); g2 += G2.sum()
            near += (P & (np.abs(al - as0) <= 0.02)).sum(); win += (P & (np.abs(al - as0) <= 2*das)).sum()
            J = G2 & (np.abs(al - as0) <= 2*das); joint += J.sum()
            if J.any():
                earned.add(f)
                for idx in np.where(J)[0][:max(0, 3 - len(examples))]:
                    examples.append({'fork': [str(x) for x in f], 'n': [na2, nb1, nd2, nc1], 'chi': [round(float(x), 3) for x in G[idx]],
                                     'alpha_s': round(float(al[idx]), 4), 'Ms_GeV': '%.2e' % Ms[idx]})
    chance = (g2/max(phys, 1))*(win/max(near, 1)) if near else 0.0; frac = joint/max(phys, 1)
    verdict = 'SIGNAL' if (joint >= 5 and frac >= 3*chance and chance > 0) else 'NULL'
    return dict(nmax=nmax, grid=len(grid), configs=int(tot), physical=int(phys), pass_G2=int(g2), joint=int(joint), joint_frac=frac,
                chance=chance, ratio=(frac/chance if chance else None), verdict=verdict, earned=[[str(x) for x in f] for f in earned], examples=examples), earned
if __name__ == '__main__':
    out = []; forks = FORKS
    for i, (nmax, grid) in enumerate(RINGS):
        res, earned = ring(nmax, grid, forks); res['ring'] = 'R%d' % i; res['forks_spun'] = len(forks); out.append(res)
        print('R%d |n|<=%d grid %d forks %2d: configs %9d physical(SUSY+fit) %7d  G2 %7d  JOINT %5d  frac %.2e  chance %.2e  ratio %s  -> %s'
              % (i, nmax, len(grid), len(forks), res['configs'], res['physical'], res['pass_G2'], res['joint'], res['joint_frac'], res['chance'],
                 ('%.2f' % res['ratio']) if res['ratio'] else '-', res['verdict']), flush=True)
        for e in res['examples']: print('     example:', e)
        if i >= 1: forks = sorted(earned, key=str) if earned else FORKS                      # spin outward only where it paid
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed_v1_results.json'), 'w'), indent=1)
