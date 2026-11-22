"""Lensing core (D1981, refactored D1982 so it can be calibrated on known-answer models). A layer's lenses are the right-singular
directions of its margin Jacobian J (rows: margins; cols: knobs). None = window (no margins, passes all); rank 0 = OPAQUE (blocks all)."""
import numpy as np
def lens(J):
    if J is None: return None
    u, s, vt = np.linalg.svd(J); r = int((s > 1e-3 * s.max()).sum()) if s.max() > 0 else 0
    return vt[:r].T
def angles(A, B):
    if A.shape[1] == 0 or B.shape[1] == 0: return np.array([90.0])
    s = np.clip(np.linalg.svd(A.T @ B, compute_uv=False), 0, 1); return np.degrees(np.arccos(s))
def klass(a): return 'PASS' if a < 15 else 'BENT' if a <= 75 else 'BLOCKED'
def analyze(Jf, K, layers=range(1, 10)):
    """Jf(L) -> Jacobian (rows x len(K)) or None. Returns lenses, transfers to the next non-window layer, chain, 9x9 coupling, hub."""
    n = len(K); layers = list(layers); Ls = {L: lens(Jf(L)) for L in layers}
    real = [L for L in layers if Ls[L] is not None]
    tr = {}
    for a, b in zip(real, real[1:]):
        ang = angles(Ls[a], Ls[b]); tr[f'{a}-{b}'] = dict(min_angle=round(float(ang.min()), 2), angles=[round(float(v), 2) for v in ang], cls=klass(ang.min()),
                                                        shared=[K[i] for i in range(n) if Ls[a].size and Ls[b].size and abs(Ls[a][i]).max() > 0.1 and abs(Ls[b][i]).max() > 0.1])
    P = np.eye(n)
    for L in layers:
        if Ls[L] is not None: P = (Ls[L] @ Ls[L].T) @ P
    m = len(layers); C = np.zeros((m, m))
    for j, a in enumerate(layers):
        for k, b in enumerate(layers):
            C[j, k] = np.nan if Ls[a] is None or Ls[b] is None else float(np.cos(np.radians(angles(Ls[a], Ls[b]).min())) ** 2)
    rows = {L: (None if Ls[L] is None else dict(r=Ls[L].shape[1], opaque=Ls[L].shape[1] == 0, dirs=[{K[i]: round(float(v[i]), 3) for i in range(n) if abs(v[i]) > 0.05} for v in Ls[L].T])) for L in layers}
    off = np.where(np.eye(m) == 1, np.nan, C); rs = np.nansum(off, axis=1); hub = layers[int(np.argmax(rs))]
    return dict(lenses=rows, transfers=tr, chain_dim=int(np.linalg.matrix_rank(P, tol=1e-6)), chain_frac=round(float(np.linalg.norm(P) ** 2 / n), 4),
                C=[[None if np.isnan(v) else round(v, 3) for v in r] for r in C], hub=hub, hub_rowsum=round(float(rs[layers.index(hub)]), 3))
def verdict(classes, chain_dim):
    nb, nbl = classes.count('BENT'), classes.count('BLOCKED')
    return 'SUPPORTED' if (nb >= 2 and chain_dim >= 1) else 'DECOUPLED' if nbl >= 5 else 'MIXED'
