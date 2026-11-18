"""Waves on the AEGIS web (heuristic, labelled as such). A +1 wave enters a node and spreads along links (forward weight 1, backward 0.5, times the
link sign; killed nodes pass 10 %, frozen nodes 50 %), damped so it fades (Katz-style series x = e + α W x). The inverse wave is −1. Outputs:
 - reach: how strongly each node responds to a wave from each source;
 - conflict index: |response with all signs +| − |signed response| — large where + and − paths meet (evidence in tension);
 - hidden links: unlinked node pairs whose response patterns are most alike (candidate new links/nodes);
 - opposites: pairs that answer the same waves with opposite signs (one rises when the other falls).
Writes docs/web/waves.json."""
import json, pathlib, numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
W = json.load(open(ROOT / 'docs/web/web.json', encoding='utf-8')); ids = [n['id'] for n in W['nodes']]; ix = {k: i for i, k in enumerate(ids)}; n = len(ids)
gate = np.array([{'killed': 0.1, 'frozen': 0.5}.get(x['status'], 1.0) for x in W['nodes']])
S = np.zeros((n, n)); A = np.zeros((n, n))
for e in W['edges']:
    a, b = ix[e['s']], ix[e['t']]; S[b, a] += e['sign']*1.0; S[a, b] += e['sign']*0.5; A[b, a] += 1.0; A[a, b] += 0.5
G = np.diag(gate); rho = max(abs(np.linalg.eigvals(G @ A))); alpha = 0.85/rho
Rs = np.linalg.solve(np.eye(n) - alpha*G @ S, np.eye(n))      # column s = signed response to a +1 wave at s
Ra = np.linalg.solve(np.eye(n) - alpha*G @ A, np.eye(n))      # all-positive response
conflict = (Ra - np.abs(Rs)); np.fill_diagonal(conflict, 0); cidx = conflict.sum(1)/max(conflict.sum(), 1e-12)
adj = (A + A.T) > 0
def cos(u, v):
    d = np.linalg.norm(u)*np.linalg.norm(v); return float(u @ v/d) if d > 0 else 0.0
P = Rs.copy(); np.fill_diagonal(P, 0)
pairs = []
for i in range(n):
    for j in range(i + 1, n):
        if adj[i, j]: continue
        pairs.append((cos(P[i], P[j]), ids[i], ids[j]))
pairs.sort(reverse=True)
two_hop = lambda i, j: bool(((A + A.T) @ (A + A.T))[ix[i], ix[j]] > 0)
hidden = [dict(a=a, b=b, sim=round(s, 3), two_hop=two_hop(a, b)) for s, a, b in pairs[:15]]
opp = [dict(a=a, b=b, sim=round(s, 3)) for s, a, b in sorted(pairs)[:10] if s < 0]
reach = {ids[s]: {ids[j]: round(float(Rs[j, s]), 4) for j in range(n) if abs(Rs[j, s]) > 1e-3 and j != s} for s in range(n)}
out = dict(alpha=alpha, note='heuristic graph analysis, not physics; real recompute follows for top targets', conflict=sorted(((ids[i], round(float(cidx[i]), 4)) for i in range(n)), key=lambda x: -x[1])[:12],
           hidden=hidden, opposites=opp, reach=reach)
json.dump(out, open(ROOT / 'docs/web/waves.json', 'w'), indent=1, ensure_ascii=False)
print('conflict:', out['conflict'][:8]); print('hidden:', [(h['a'], h['b'], h['sim'], h['two_hop']) for h in hidden[:10]]); print('opposites:', [(o['a'], o['b'], o['sim']) for o in opp[:6]])
