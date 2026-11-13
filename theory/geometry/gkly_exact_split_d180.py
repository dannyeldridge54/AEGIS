"""D180: does GKLY's EXACT octonion superpotential (arXiv:2008.01494 eq. 4.7, signs fixed by the octonions) contain the
associative/coassociative split? W = sum_r c_r (T^{r+2} - T^{r+4})(T^{r+5} - T^{r+6}), r = 0..6, indices mod 7 in 1..7; their
splits remove codewords (terms). Test every subset of the 7 exact terms, with unit coefficients and with random coefficients,
for flat directions exactly {T_A, T_C} (A a Fano line, C its complement) and every kept term vanishing there. AI-assisted."""
import itertools, numpy as np
from scipy.linalg import null_space
m = lambda k: (k - 1) % 7 + 1
terms = [((m(r + 2), m(r + 4)), (m(r + 5), m(r + 6))) for r in range(7)]
lines = [(1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)]
def vec(p):
    v = np.zeros(7); v[p[0] - 1] = 1; v[p[1] - 1] = -1; return v
rng = np.random.default_rng(1)
print("GKLY terms:", terms)
for coeff_mode in ("unit", "random"):
    found = []
    for k in range(1, 8):
        for sub in itertools.combinations(range(7), k):
            cs = np.ones(7) if coeff_mode == "unit" else rng.uniform(0.5, 2.0, 7)
            Hm = sum(cs[r] * (np.outer(vec(terms[r][0]), vec(terms[r][1])) + np.outer(vec(terms[r][1]), vec(terms[r][0]))) for r in sub)
            N = null_space(Hm, rcond=1e-8)
            for A in lines:
                tA = np.array([1.0 if i + 1 in A else 0 for i in range(7)]); tC = 1 - tA
                ok = all(abs(vec(terms[r][0]) @ tA) < 1e-12 or abs(vec(terms[r][1]) @ tA) < 1e-12 for r in sub)
                if ok and N.shape[1] == 2:
                    P = N @ N.T
                    if np.allclose(P @ tA, tA) and np.allclose(P @ tC, tC): found.append((A, sub))
    print(f"{coeff_mode} coefficients: subsets of GKLY's exact terms giving exactly the split T_A + T_C: {len(found)}", found[:7])
# full W: flat directions
Hm = sum(np.outer(vec(a), vec(b)) + np.outer(vec(b), vec(a)) for a, b in terms); print("full W_O flat directions:", null_space(Hm, rcond=1e-8).shape[1])
