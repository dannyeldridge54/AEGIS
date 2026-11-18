"""Resonance modes of the AEGIS web: eigenvectors of the signed graph Laplacian L = D − S_sym (S_sym = symmetrised signed links, |weights| on the diagonal).
Low modes = groups of nodes that move together; a sign change inside a mode marks a split. Writes docs/web/modes.json. Heuristic, not physics."""
import json, pathlib, numpy as np
R = pathlib.Path(__file__).resolve().parents[2]; W = json.load(open(R / 'docs/web/web.json', encoding='utf-8'))
ids = [n['id'] for n in W['nodes']]; ix = {k: i for i, k in enumerate(ids)}; n = len(ids); S = np.zeros((n, n))
for e in W['edges']:
    a, b = ix[e['s']], ix[e['t']]; S[a, b] += e['sign']; S[b, a] += e['sign']
Dg = np.diag(np.abs(S).sum(1)); L = Dg - S; w, v = np.linalg.eigh(L)
modes = []
for k in range(min(10, n)):
    vec = v[:, k]; top = np.argsort(-np.abs(vec))[:8]
    modes.append(dict(k=k, freq=round(float(np.sqrt(max(w[k], 0))), 4), vec=[round(float(x), 4) for x in vec],
                      top=[(ids[i], round(float(vec[i]), 3)) for i in top]))
json.dump(dict(ids=ids, modes=modes), open(R / 'docs/web/modes.json', 'w'), indent=1, ensure_ascii=False)
for m in modes[:6]: print(m['k'], m['freq'], m['top'][:5])
