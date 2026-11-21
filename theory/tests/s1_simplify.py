"""PREREG_S1_SIMPLIFY"""
import math, json
gs = 2 / math.sqrt(3); MP = 2.435e18; C = 8.0e-7; w = 2 / 3; ReT = 28.9 - 9 / gs
rows = []
for N in range(5, 11):
    W0 = math.exp(-2 * math.pi * ReT / N)
    for chi in (20, 50, 100, 200):
        V = w * chi / (4 * (2 * math.pi) ** 3 * C); m32 = math.sqrt(gs / 2) * W0 * MP / V
        rows.append(dict(N=N, chi=chi, volume=V, W0=W0, m32_GeV=m32, M2_TeV=m32 / 375 / 1e3, in_window=0.67 <= m32 / 375 / 1e3 <= 0.71))
print(json.dumps(dict(ReT=ReT, rows=rows, hits=[(r['N'], r['chi']) for r in rows if r['in_window']]), indent=1))
