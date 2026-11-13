"""D179 (corrected): every term may enter with either sign (the octonion structure constants fix signs; here we allow both and ask
whether ANY signed choice gives the associative/coassociative split). 7 options per quadruple (unused, or 3 pairings x 2 signs).
Counts must now be equal for all 7 lines (Fano symmetry) — that is the check on the code. AI-assisted."""
import itertools, numpy as np
from scipy.linalg import null_space
lines = [(1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)]
quads = [tuple(sorted(set(range(1, 8)) - set(l))) for l in lines]
def pairings(q):
    a, b, c, d = q; return [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]
def vec(p):
    v = np.zeros(7); v[p[0] - 1] = 1; v[p[1] - 1] = -1; return v
TERMS = [[None] + [(s * np.outer(vec(p[0]), vec(p[1])) + s * np.outer(vec(p[1]), vec(p[0])), vec(p[0]), vec(p[1]))
          for p in pairings(q) for s in (1, -1)] for q in quads]
tgt = []
for A in lines:
    C = set(range(1, 8)) - set(A)
    tgt.append((np.array([1.0 if i + 1 in A else 0 for i in range(7)]), np.array([1.0 if i + 1 in C else 0 for i in range(7)])))
counts = [0] * 7; minterms = [9] * 7
for choice in itertools.product(range(7), repeat=7):
    used = [TERMS[i][c] for i, c in enumerate(choice) if c]
    if len(used) < 4: continue
    Hm = sum(t[0] for t in used)
    # flat directions of each candidate split must be killed by every term (W = dW = 0 there): cheap test first
    for li, (tA, tC) in enumerate(tgt):
        if all(abs(u @ tA) < 1e-12 or abs(w @ tA) < 1e-12 for _, u, w in used) and all(abs(u @ tC) < 1e-12 or abs(w @ tC) < 1e-12 for _, u, w in used):
            N = null_space(Hm, rcond=1e-8)
            if N.shape[1] == 2:
                P = N @ N.T
                if np.allclose(P @ tA, tA) and np.allclose(P @ tC, tC):
                    counts[li] += 1; minterms[li] = min(minterms[li], len(used))
for li in range(7):
    print(f"line {lines[li]}: {counts[li]} signed superpotentials give exactly the flat directions T_A, T_C (fewest terms {minterms[li]})")
