#!/usr/bin/env python3
"""Independent verifier for (3,K)-graphs (D1998): graph6 in -> triangle-free? independence number < K? Pure Python, two methods:
(1) exhaustive bitset search for an independent K-set; (2) maximum independent set by a separate branch-and-bound. Both must agree."""
import sys, itertools
def g6(s):
    s = s.strip(); n = ord(s[0]) - 63; bits = []
    for ch in s[1:]: v = ord(ch) - 63; bits += [(v >> (5 - i)) & 1 for i in range(6)]
    A = [0] * n; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: A[i] |= 1 << j; A[j] |= 1 << i
            k += 1
    return n, A
def triangle_free(n, A): return all(not (A[u] & A[v]) for u in range(n) for v in range(n) if (A[u] >> v) & 1)
def has_indep(cand, k, A):
    if k == 0: return True
    if bin(cand).count('1') < k: return False
    while cand:
        v = (cand & -cand).bit_length() - 1; cand &= cand - 1
        if has_indep(cand & ~A[v], k - 1, A): return True
    return False
def mis(cand, A, cur=0, best=[0]):
    if cand == 0: best[0] = max(best[0], cur); return best[0]
    if cur + bin(cand).count('1') <= best[0]: return best[0]
    v = (cand & -cand).bit_length() - 1
    mis(cand & ~A[v] & ~(1 << v), A, cur + 1, best); mis(cand & ~(1 << v), A, cur, best); return best[0]
if __name__ == '__main__':
    s = open(sys.argv[1]).read() if len(sys.argv) > 1 and not sys.argv[1].startswith(('?', '@')) and len(sys.argv[1]) > 3 and '/' in sys.argv[1] or (len(sys.argv) > 1 and sys.argv[1].endswith('.g6')) else sys.argv[1]
    K = int(sys.argv[2]); n, A = g6(s); tf = triangle_free(n, A); full = (1 << n) - 1
    ind = has_indep(full, K, A); a = mis(full, A, 0, [0])
    ok = tf and not ind and a < K
    print(dict(n=n, K=K, triangle_free=tf, has_independent_K_set=ind, independence_number=a, methods_agree=(ind == (a >= K)), VALID=ok)); sys.exit(0 if ok else 1)
