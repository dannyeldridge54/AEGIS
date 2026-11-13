"""D179: can the octonionic building blocks themselves produce the associative/coassociative split? AI-assisted.
GKLY-style terms: for each coassociative quadruple Q (complement of a Fano line) a product (T_i - T_j)(T_k - T_l) over one of its
three pairings. Search every superpotential made of these terms (each quadruple: unused or one of its 3 pairings; 4^7 = 16,384
choices) and keep those whose supersymmetric flat directions (W = dW = 0, null space of the mass matrix) are EXACTLY {T_A, T_C} for a
Fano line A and its complement C. Compare with the all-equal (0+7) case."""
import itertools, numpy as np
lines = [(1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)]
quads = [tuple(sorted(set(range(1, 8)) - set(l))) for l in lines]
def pairings(q):
    a, b, c, d = q; return [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]
def vec(p):
    v = np.zeros(7); v[p[0] - 1] = 1; v[p[1] - 1] = -1; return v
def analyse(choice):
    Hm = np.zeros((7, 7)); terms = []
    for q, ch in zip(quads, choice):
        if ch is None: continue
        u, w = (vec(x) for x in pairings(q)[ch]); Hm += np.outer(u, w) + np.outer(w, u); terms.append((u, w))
    from scipy.linalg import null_space
    null = null_space(Hm, rcond=1e-8)
    return Hm, terms, null
target = {}
for li, A in enumerate(lines):
    C = tuple(sorted(set(range(1, 8)) - set(A)))
    tA = np.array([1.0 if i + 1 in A else 0 for i in range(7)]); tC = np.array([1.0 if i + 1 in C else 0 for i in range(7)])
    target[li] = (A, C, tA, tC)
hits = {li: [] for li in target}; all_equal = 0
for choice in itertools.product([None, 0, 1, 2], repeat=7):
    if all(c is None for c in choice): continue
    Hm, terms, null = analyse(choice)
    if null.shape[1] == 1 and np.allclose(np.abs(null[:, 0]), 1 / np.sqrt(7)): all_equal += 1
    if null.shape[1] != 2: continue
    for li, (A, C, tA, tC) in target.items():
        # flat directions exactly span{tA, tC}, and every term vanishes there (W = 0 on the flat space)
        P = null @ null.T
        if np.allclose(P @ tA, tA) and np.allclose(P @ tC, tC) and all(abs(u @ tA) < 1e-9 or abs(w @ tA) < 1e-9 for u, w in terms) \
           and all(abs((u @ (tA + 2 * tC)) * (w @ (tA + 2 * tC))) < 1e-9 for u, w in terms):
            hits[li].append(sum(c is not None for c in choice))
print(f"superpotentials (built only from coassociative-quadruple terms) with the single all-equal flat direction (rung 7): {all_equal}")
for li, h in hits.items():
    print(f"line {lines[li]} + complement: {len(h)} superpotentials give exactly the two flat directions T_A, T_C"
          + (f" (using {min(h)}-{max(h)} terms)" if h else ""))
