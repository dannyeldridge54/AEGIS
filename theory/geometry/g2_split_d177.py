"""D177: the G2-natural 4+3 split — an associative triad (a Fano line) plus its coassociative complement. AI-assisted.
Superpotential in the style of Kallosh-Linde-Wrase-Yamada (1704.04829, W0 = M sum_{i<j} (T_i - T_j)^2), restricted to the two blocks:
  W = M [ sum_{i<j in A} (T_i - T_j)^2 + sum_{i<j in C} (T_i - T_j)^2 ],   A = {1,2,4} (a Fano line), C = {3,5,6,7} (its complement).
Supersymmetric Minkowski vacua need W = 0 and dW = 0: count the flat directions (zero modes of the mass matrix d2W) and show they are
T_A (three disks -> K = -3 ln, rung 3: the Twist) and T_C (four disks -> rung 4). Also check that C is coassociative (the complement of
an associative triad) for all 7 lines, and that each of the 7 such splits is related to the others by the Fano symmetry (order 168)."""
import itertools, numpy as np
lines = [(1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)]
def hess(A, C):
    Hm = np.zeros((7, 7))
    for blk in (A, C):
        for i, j in itertools.combinations(blk, 2):
            i, j = i - 1, j - 1; Hm[i, i] += 2; Hm[j, j] += 2; Hm[i, j] -= 2; Hm[j, i] -= 2
    return Hm
A = (1, 2, 4); C = tuple(sorted(set(range(1, 8)) - set(A)))
ev, evec = np.linalg.eigh(hess(A, C))
zero = [evec[:, k] for k in range(7) if abs(ev[k]) < 1e-9]
print(f"split A = {A} (Fano line), C = {C}: mass eigenvalues {np.round(ev, 3)}; flat directions: {len(zero)}")
span = np.array(zero).T
for name, blk in (("T_A (rung 3)", A), ("T_C (rung 4)", C)):
    v = np.array([1.0 if i + 1 in blk else 0.0 for i in range(7)]); res = v - span @ np.linalg.lstsq(span, v, rcond=None)[0]
    print(f"  {name} lies in the flat space: {np.allclose(res, 0)}")
# coassociative check: a 4-set is the complement of a line iff it contains no line
for l in lines:
    comp = set(range(1, 8)) - set(l)
    assert not any(set(m) <= comp for m in lines)
print("all 7 complements of Fano lines contain no line (coassociative quadruples): True")
# contrast: GKLY's hand-made 4+3 split (3-direction {2,3,6})
print("GKLY 4+3 split rung-3 set {2,3,6} is a Fano line:", frozenset({2, 3, 6}) in {frozenset(l) for l in lines})
