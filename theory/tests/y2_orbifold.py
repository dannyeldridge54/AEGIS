"""PREREG_Y2_ORBIFOLD"""
import numpy as np, cmath, math, json
w = cmath.exp(2j * math.pi / 3)
def A(M):
    F = np.array([[cmath.exp(2j * math.pi * j * k / M) for k in range(M)] for j in range(M)]) / math.sqrt(M)
    return np.diag([cmath.exp(1j * math.pi * j * j / M) for j in range(M)]) @ F
def classes(M):
    a = A(M); s = np.linalg.matrix_power(a, 3)[0, 0]; ev, V = np.linalg.eig(a)
    ph = np.round(((np.angle(ev) - np.angle(s) / 3) / (2 * math.pi)) % 1 * 3) % 3   # class 0,1,2
    out = {}
    for c in range(3):
        idx = np.where(ph == c)[0]
        if len(idx): Q, _ = np.linalg.qr(V[:, idx]); out[c] = Q
    return out
def theta(a, t, L=30): return sum(cmath.exp(1j * math.pi * t * (l + a) ** 2) for l in range(-L, L + 1))
ML, MR = 6, 6; MH = ML + MR; tau = w; t = tau * ML * MR * MH
Y = np.zeros((ML, MR, MH), complex)
for i in range(ML):
    for j in range(MR):
        for m in range(MR):
            k = (i + j + ML * m) % MH
            Y[i, j, k] += theta((MR * i - ML * j + ML * MR * m) / (ML * MR * MH), t)
CL, CR, CH = classes(ML), classes(MR), classes(MH)
res = {}
for cl in CL:
    if CL[cl].shape[1] != 3: continue
    for cr in CR:
        if CR[cr].shape[1] != 3: continue
        ch = (-(cl + cr)) % 3
        if ch not in CH: continue
        for c in range(CH[ch].shape[1]):
            Mm = np.einsum('ijk,ia,jb,k->ab', Y, CL[cl], CR[cr], CH[ch][:, c].conj())
            s = np.sort(np.linalg.svd(Mm, compute_uv=False))[::-1]
            if s[0] < 1e-12: continue
            res[f'L{cl} R{cr} H{ch} mode{c}'] = dict(s2_s1=s[1] / s[0], s3_s1=s[2] / s[0], Q=s.sum() / np.sqrt(s).sum() ** 2)
print(json.dumps(res, indent=1))
