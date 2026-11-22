# EVOLVE-BLOCK-START
"""R(3,10) front L: construct a triangle-free graph on 40 vertices with no independent set of size 10.
Return a list of edges (u, v) with 0 <= u < v < 40. Known: no circulant, no Cayley graph on any group of order 40,
no 2-block circulant works (D2000, D2018, D2019); every vertex needs degree 5..9 (D2003). Best known family members reach alpha = 10."""
import random
def construct(seed=0, n=40, iters=20000):
    rng = random.Random(seed)
    adj = [set() for _ in range(n)]
    def triangle_free_add(u, v): return not (adj[u] & adj[v])
    # greedy random triangle-free process, then local improvement on degree balance
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]; rng.shuffle(pairs)
    for u, v in pairs:
        if len(adj[u]) < 9 and len(adj[v]) < 9 and triangle_free_add(u, v): adj[u].add(v); adj[v].add(u)
    return [(u, v) for u in range(n) for v in adj[u] if u < v]
# EVOLVE-BLOCK-END
def run(): return construct()
