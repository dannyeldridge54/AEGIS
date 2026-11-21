import math, json, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
MZ, aem, s2 = 91.1876, 127.95, 0.23122; mw, mg, ms = 700, 7000, 4.7e5
SM1, MS1 = np.array([41/10, -19/6, -7]), np.array([33/5, 1, -3])
SM2 = np.array([[199/50, 27/10, 44/5], [9/10, 35/6, 12], [11/10, 9/2, -26]]); MS2 = np.array([[199/25, 27/5, 88/5], [9/5, 25, 24], [11/5, 9, 14]])
cSM, cMS = np.array([17/10, 3/2, 2]), np.array([26/5, 6, 4])
def make(tb):
    sb = math.sin(math.atan(tb))
    def rhs(t, v):
        x, yt = v[:3], v[3]; mu = math.exp(t); al = 1 / x; g2 = 4 * math.pi * al
        if mu >= ms:
            b1, b2, c = MS1, MS2, cMS
            dy = yt / (16 * math.pi**2) * (6 * yt**2 - 16/3 * g2[2] - 3 * g2[1] - 13/15 * g2[0])
        else:
            b1, b2, c = SM1.copy(), SM2.copy(), cSM
            if mu >= mw: b1 = b1 + [0, 4/3, 0]; b2[1, 1] += 64/3
            if mu >= mg: b1 = b1 + [0, 0, 2]; b2[2, 2] += 48
            dy = yt / (16 * math.pi**2) * (4.5 * yt**2 - 8 * g2[2] - 2.25 * g2[1] - 17/20 * g2[0])
        dx = -b1 / (2 * math.pi) - b2 @ al / (8 * math.pi**2) + c * yt**2 / (32 * math.pi**3)
        return np.append(dx, dy)
    def run(a3, mu1):
        v = np.array([0.6 * (1 - s2) * aem, s2 * aem, 1 / a3, 0.97])
        pts = [math.log(MZ)] + [math.log(m) for m in (mw, mg, ms) if m < mu1] + [math.log(mu1)]
        for t0, t1 in zip(pts, pts[1:]):
            v = solve_ivp(rhs, (t0, t1), v, rtol=1e-10, atol=1e-12).y[:, -1]
            if abs(t1 - math.log(ms)) < 1e-9: v[3] = v[3] / sb
        return v
    def m12(a3):
        lo, hi = 1e12, 1e18
        for _ in range(50):
            mid = math.sqrt(lo * hi); v = run(a3, mid); lo, hi = (mid, hi) if v[0] > v[1] else (lo, mid)
        return mid, run(a3, mid)
    return m12
out = {}
for tb in (1, 2, 4):
    m12 = make(tb)
    try:
        M, v = m12(0.118)
        if not np.all(np.isfinite(v)) or v[3] > 4 * math.pi: raise ValueError('yt nonperturbative')
        au = brentq(lambda a3: (lambda r: r[1][2] - r[1][0])(m12(a3)), 0.09, 0.14, xtol=1e-6)
        out[str(tb)] = dict(M12=M, alpha_inv=float(v[0]), Delta3=float(v[2] - v[0]), yt_M12=float(v[3]), alpha_s_unif=au)
    except Exception as e:
        out[str(tb)] = dict(status='non-perturbative / no unification', error=str(e)[:80])
    print(tb, out[str(tb)])
c = out['2']['alpha_s_unif']; out['verdict'] = 'CONSISTENT' if abs(c - 0.118) <= 0.007 else 'TENSION' if abs(c - 0.118) <= 0.015 else 'FAIL'
print(out['verdict']); json.dump(out, open('field_tests/results/b11c_yukawa.json', 'w'), indent=1)
