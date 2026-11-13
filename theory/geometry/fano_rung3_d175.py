"""D175: is rung 3 a Fano line? The seven imaginary octonions e1..e7 multiply along the 7 lines of the Fano plane
(standard: 124, 235, 346, 457, 561, 672, 713 — e_i e_j = e_k cyclically on each line). Seven disks <-> seven points (qubit picture,
Duff-Ferrara: E7 ⊃ SL(2)^7, seven tripartite triangles = the 7 lines) or <-> seven lines (G2 picture: the associative 3-form has one
term per line); the Fano plane is self-dual, so both pictures agree. Rung 3 = identifying three disks. Which triples are special? AI-assisted."""
from itertools import combinations
lines = [(1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)]
L = {frozenset(l) for l in lines}
def closes(t):
    # does {1, e_a, e_b, e_c} close under multiplication? e_a e_b must be +-e_c for each pair -> the triple must be a line
    return frozenset(t) in L
triples = list(combinations(range(1, 8), 3))
coll = [t for t in triples if closes(t)]
print(f"triples of 7 units: {len(triples)}; on a Fano line (closed: 1, e_a, e_b, e_c span a copy of the quaternions): {len(coll)}; "
      f"triangles (not closed): {len(triples)-len(coll)}")
print("lines:", coll)
# disks per rung: 3alpha = k identifies k disks; which k-sets are 'closed' sub-structures?
for k in range(1, 8):
    sets = list(combinations(range(1, 8), k))
    def subalg(s):
        S = set(s)
        for a, b in combinations(S, 2):
            c = next(next(iter(set(l) - {a, b})) for l in L if {a, b} <= set(l))
            if c not in S: return False
        return True
    n = sum(subalg(s) for s in sets)
    print(f"rung 3alpha = {k}: {len(sets):>2} ways to choose the disks; closed under multiplication: {n}")
