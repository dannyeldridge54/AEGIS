"""PREREG_TWISTC scan (locked 3cfaf39). W = sqrt3 m S (T + c); along real T, S = 0: ln V = 2 ln|1 + 2c/u| - ln(1 + u/2) - 2n(1 - e^{-pi u/8}). AI-assisted."""
import mpmath as mp
mp.mp.dps = 30
n = 125; k = mp.sqrt(mp.mpf(2) / 3)
def run(c):
    f = lambda p: 2 * mp.log(abs(1 + 2 * c / mp.e ** (k * p))) - mp.log(1 + mp.e ** (k * p) / 2) - 2 * n * (1 - mp.e ** (-mp.pi * mp.e ** (k * p) / 8))
    d1 = lambda p: mp.diff(f, p); d2 = lambda p: mp.diff(f, p, 2); eps = lambda p: d1(p) ** 2 / 2
    p = mp.mpf(6)
    while eps(p) < 1: p -= mp.mpf("0.02")
    while eps(p) > 1: p -= mp.mpf("0.02")
    pend = mp.findroot(lambda q: eps(q) - 1, (p, p + mp.mpf("0.02")), solver="anderson")
    out, N, q, dq = [], mp.mpf(0), pend, mp.mpf("-0.002")
    for Ns in (55.7, 57):
        while N < Ns:
            s = -d1(q)                      # V decreases toward the cliff: d lnV/dphi < 0 on the plateau (code fix: sign)
            if s <= 0: return None, f"plateau turns over at u = {float(mp.e ** (k * q)):.3g} (N = {float(N):.1f})"
            N += -dq / s; q += dq
        out.append((Ns, float(1 + 2 * d2(q) - d1(q) ** 2), float(8 * d1(q) ** 2), float(mp.e ** (k * q))))
    return out, None
for c in (-3e-6, -1e-6, -3e-7, -1e-7, 0, 1e-7, 3e-7, 1e-6, 3e-6):
    out, why = run(mp.mpf(c))
    if out is None: print(f"c {c:+.0e}: EXCLUDED ({why})", flush=True); continue
    print(f"c {c:+.0e}: " + "; ".join(f"N*={a}: n_s={b:.4f} r={d:.4f} (u*={e:.2e})" for a, b, d, e in out), flush=True)
