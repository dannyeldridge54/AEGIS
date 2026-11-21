"""PREREG_L7_ALPHA_STRING"""
import math, json
MZ = 91.1876; A0 = [59.01, 29.59, 8.47]
def run(MS):
    seg = [(MZ, 1e3, (41/10, -19/6, -7)), (1e3, MS, (41/10, -19/6 + 4/3, -7 + 2)), (MS, 1e20, (33/5, 1, -3))]
    def ainv(mu):
        a = list(A0)
        for lo, hi, b in seg:
            top = min(mu, hi)
            if top <= lo: break
            for i in range(3): a[i] -= b[i] / (2 * math.pi) * math.log(top / lo)
        return a
    lo, hi = math.log(1e3), math.log(1e20)
    for _ in range(200):
        mid = (lo + hi) / 2; a = ainv(math.exp(mid))
        (lo, hi) = (mid, hi) if a[0] > a[1] else (lo, mid)
    M12 = math.exp(lo); a = ainv(M12)
    return dict(M_S=MS, M12_GeV=M12, alpha12_inv=a[0], alpha3_inv=a[2], delta3=a[2] - a[0])
gs = 2 / math.sqrt(3); MP = 2.435e18
out = {'data': [run(M) for M in (2.5e5, 5e5, 7e5)]}
th = {}
for m32 in (2.5e5, 5e5, 7e5):
    L = math.log(math.sqrt(gs / 2) * MP / m32); th[str(m32)] = {N: 9 / gs + N * L / (2 * math.pi) for N in range(2, 10)}
out['theory'] = th
sel = []
for N in range(2, 10):
    if all(abs(th[str(d['M_S'])][N] - d['alpha12_inv']) <= 1.5 for d in out['data']): sel.append(N)
out['selected_N'] = sel
out['residuals'] = {N: [round(th[str(d['M_S'])][N] - d['alpha12_inv'], 2) for d in out['data']] for N in range(3, 8)}
print(json.dumps(out, indent=1, default=str))
