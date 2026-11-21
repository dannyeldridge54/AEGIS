"""PREREG_R2_WINO_MAGD7"""
import json, math
import numpy as np
M = [0.66, 1.0, 1.85]; ft = [0.14, 0.26, 0.67]; fth = [0.05, 0.12, 0.41]; fmax = [0.16, 0.24, 0.44]
out = {}
for ainv, TR in ((24.3, 4.30e8), (40.0, 2.61e8)):
    f = [th + (t - th) * TR / 3.2e8 for t, th in zip(ft, fth)]
    ok = [a <= b for a, b in zip(f, fmax)]
    lm = np.log(M); g = np.array(f) - np.array(fmax)   # margin; upper edge where g crosses 0 going up
    edge = None
    for i in range(2):
        if g[i] <= 0 < g[i + 1]: edge = float(math.exp(lm[i] + (lm[i + 1] - lm[i]) * (-g[i]) / (g[i + 1] - g[i])))
    out[f'alpha_inv={ainv}'] = dict(T_R=TR, f_total=dict(zip(map(str, M), f)), pass_=dict(zip(map(str, M), ok)), upper_edge_TeV=edge,
                                    window='empty at the collider edge' if not ok[0] else f'0.67 – {edge:.2f} TeV' if edge else '0.67 – ≥1.85 TeV')
print(json.dumps(out, indent=1))
