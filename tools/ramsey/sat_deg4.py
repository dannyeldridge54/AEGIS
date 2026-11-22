#!/usr/bin/env python3
"""D2002 independent check by SAT (PySAT, CaDiCaL): does a (3,K)-graph on 40 vertices with a degree-4 vertex exist (dual neighbourhood = C35(1,7,11,16))?
Independent of glue4.c: H and its independent sets are rebuilt here in pure Python; constraints are clauses, not search."""
import sys, itertools, time
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
K = int(sys.argv[1]) if len(sys.argv) > 1 else 10
n = 35; S = (1, 7, 11, 16); adj = [set() for _ in range(n)]
for v in range(n):
    for d in S: adj[v].add((v + d) % n); adj[v].add((v - d) % n)
indep = {6: [], 7: [], 8: []}
def rec(cur, cand):
    if len(cur) in indep: indep[len(cur)].append(tuple(cur))
    for i, v in enumerate(cand): rec(cur + [v], [u for u in cand[i + 1:] if u not in adj[v]])
rec([], list(range(n)))
print({k: len(v) for k, v in indep.items()}, flush=True)
pool = IDPool(); x = lambda a, h: pool.id(('x', a, h)); clauses = []
for h in range(n):
    for a, b in itertools.combinations(range(4), 2): clauses.append([-x(a, h), -x(b, h)])       # disjoint (H is 8-regular, degrees <= 9)
for a in range(4):
    for h in range(n):
        for g in adj[h]:
            if g > h: clauses.append([-x(a, h), -x(a, g)])                                           # A_a independent (triangle-free)
    lits = [x(a, h) for h in range(n)]
    for enc in (CardEnc.atleast(lits, 3, vpool=pool, encoding=EncType.seqcounter), CardEnc.atmost(lits, 8, vpool=pool, encoding=EncType.seqcounter)): clauses += enc.clauses
for j, I_list in indep.items():
    maxmiss = K - 1 - j
    if maxmiss >= 4: continue
    for I in I_list:
        for T in itertools.combinations(range(4), maxmiss + 1):   # no (maxmiss+1) of the A's may all miss I
            clauses.append([x(a, h) for a in T for h in I])
print('vars', pool.top, 'clauses', len(clauses), flush=True)
t = time.time()
with Solver(name='cadical153', bootstrap_with=clauses) as s:
    r = s.solve(); print('K', K, 'SAT' if r else 'UNSAT', 'in %.1fs' % (time.time() - t))
    if r:
        m = set(l for l in s.get_model() if l > 0); A = [[h for h in range(n) if x(a, h) in m] for a in range(4)]; print('A =', A)
