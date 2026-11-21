"""PREREG_Y1_THETA"""
import numpy as np, json, cmath, math
rho = complex(0.5, math.sqrt(3) / 2)   # e^{i pi/3}
IL, IR, IH = 3, 3, 6; t = rho * IL * IR * IH
def theta(a, t, L=40):
    return sum(cmath.exp(1j * math.pi * t * (l + a) ** 2) for l in range(-L, L + 1))
out = {}
for k in range(IH):
    Y = np.array([[theta(((i / IL + j / IR + k / IH) % 1), t) for j in range(IR)] for i in range(IL)])
    s = np.linalg.svd(Y, compute_uv=False); s = np.sort(s)[::-1]
    Q = s.sum() / np.sqrt(s).sum() ** 2
    out[k] = dict(s2_s1=s[1] / s[0], s3_s1=s[2] / s[0], Koide_Q=Q)
print(json.dumps(out, indent=1))
