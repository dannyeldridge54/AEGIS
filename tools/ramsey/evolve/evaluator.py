"""OpenEvolve evaluator for R(3,10) front L (D2021). Score: higher is better.
Stage 1 (cascade): valid edge list on 40 vertices, triangle-free. Stage 2: exact independence number alpha (bitset branch-and-bound).
combined_score = 10 - alpha (+ small degree-balance bonus); alpha <= 9 means a (3,10,40)-graph: written to WITNESS.txt for verify.py, never claimed."""
import importlib.util, time, json, os
def _load(path):
    spec = importlib.util.spec_from_file_location('prog', path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def _graph(edges, n=40):
    adj = [0] * n
    for u, v in edges:
        u, v = int(u), int(v)
        if not (0 <= u < n and 0 <= v < n) or u == v: raise ValueError('bad edge')
        adj[u] |= 1 << v; adj[v] |= 1 << u
    return adj
def _triangles(adj): return sum(bin(adj[u] & adj[v]).count('1') for u in range(len(adj)) for v in range(u) if adj[u] >> v & 1) // 3
def _alpha(adj, cap=12, deadline=20.0):
    best = [0]; t0 = time.time()
    def rec(size, cand):
        if best[0] >= cap or time.time() - t0 > deadline: return
        if size + bin(cand).count('1') <= best[0]: return
        if not cand: best[0] = size; return
        v = (cand & -cand).bit_length() - 1
        rec(size + 1, cand & ~adj[v] & ~(1 << v)); rec(size, cand & ~(1 << v))
    rec(0, (1 << len(adj)) - 1); return best[0]
def evaluate_stage1(program_path):
    try:
        edges = _load(program_path).run(); adj = _graph(edges); tri = _triangles(adj)
        return {'combined_score': -float(tri) if tri else 0.5, 'triangles': float(tri)}
    except Exception as e:
        return {'combined_score': -1000.0, 'error': str(e)[:200]}
def evaluate(program_path):
    s1 = evaluate_stage1(program_path)
    if s1.get('triangles', 1) != 0: return s1
    adj = _graph(_load(program_path).run()); a = _alpha(adj); degs = [bin(x).count('1') for x in adj]
    score = 10.0 - a + 0.01 * (min(degs) >= 5) - 0.001 * (max(degs) - min(degs))
    if a <= 9:
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'WITNESS.txt'), 'a').write(json.dumps({'t': time.time(), 'edges': _load(program_path).run()}) + '\n')
    return {'combined_score': score, 'alpha': float(a), 'min_degree': float(min(degs)), 'max_degree': float(max(degs))}
