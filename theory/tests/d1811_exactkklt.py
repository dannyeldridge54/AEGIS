import math, json
gs = 2 / math.sqrt(3); MP = 2.435e18; C, w = 8e-7, 2 / 3; sig = 20.15
pre = math.sqrt(gs / 2) * MP / 375 * 4 * (2 * math.pi) ** 3 * C / w
out = {}
for N in range(5, 10):
    x = 2 * math.pi * sig / N; rows = {}
    for A in (0.05, 0.1, 0.3, 1, 3, 10, 30):
        W0 = A * math.exp(-x) * (1 + 2 * x / 3)
        ch = [c for c in range(2, 301) if 660 <= pre * W0 / c <= 694 and w * c / (4 * (2 * math.pi) ** 3 * C) >= 1e4]
        rows[str(A)] = dict(W0=W0, chi=ch)
    out[str(N)] = rows
nat = lambda N: any(out[str(N)][str(A)]['chi'] for A in (0.3, 1, 3))
passN = [N for N in range(5, 10) if nat(N)]
v = 'N7 UNIQUE' if passN == [7] else ('SHARED' if 7 in passN else 'N7 DISFAVOURED')
out['natural_pass_N'] = passN; out['verdict'] = v
for N in range(5, 10):
    print(N, {A: (round(r['W0'], 12), r['chi'][:1] + r['chi'][-1:] if r['chi'] else None) for A, r in out[str(N)].items()})
print(passN, v); json.dump(out, open('field_tests/results/d1811_exactkklt.json', 'w'), indent=1)
