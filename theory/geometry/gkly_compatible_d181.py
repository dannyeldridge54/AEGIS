"""D181: which of GKLY's exact octonion terms are compatible with a Fano-line split, and what flat directions do they leave? AI-assisted.
A term (T_a - T_b)(T_c - T_d) vanishes on the split directions only if one of its pairs lies inside A (the line) or inside C (complement)."""
import itertools, numpy as np
from scipy.linalg import null_space
m = lambda k: (k - 1) % 7 + 1
terms = [((m(r + 2), m(r + 4)), (m(r + 5), m(r + 6))) for r in range(7)]
lines = [(1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)]
def vec(p):
    v = np.zeros(7); v[p[0] - 1] = 1; v[p[1] - 1] = -1; return v
for A in lines[:2]:
    C = set(range(1, 8)) - set(A)
    inside = lambda p: set(p) <= set(A) or set(p) <= C
    comp = [r for r, (p, q) in enumerate(terms) if inside(p) or inside(q)]
    Hm = sum(np.outer(vec(terms[r][0]), vec(terms[r][1])) + np.outer(vec(terms[r][1]), vec(terms[r][0])) for r in comp)
    N = null_space(Hm, rcond=1e-8)
    # describe the flat space by which T's move together: cluster coordinates by equal null-space rows
    rows = np.round(N / np.max(np.abs(N)), 6)
    groups = {}
    for i in range(7):
        groups.setdefault(tuple(rows[i]), []).append(i + 1)
    print(f"line {A}: compatible terms {[terms[r] for r in comp]} -> flat directions {N.shape[1]}; moduli moving together: {list(groups.values())}")
