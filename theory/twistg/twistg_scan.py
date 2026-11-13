"""PREREG_TWISTG scan (locked f789009). TWIST-G: W = sqrt3 m S T^(1+gamma); along real T, S = 0: ln V = 2 gamma ln u - ln(1 + u/2) - 2n(1 - e^{-pi u/8})
(+ const), u = T + Tbar = e^{sqrt(2/3) phi}. Slow roll as D195/D196 (end found by scanning down the tail). AI-assisted."""
import mpmath as mp
mp.mp.dps = 30
n = 125; k = mp.sqrt(mp.mpf(2) / 3)
def run(g):
    f = lambda p: 2 * g * k * p - mp.log(1 + mp.e ** (k * p) / 2) - 2 * n * (1 - mp.e ** (-mp.pi * mp.e ** (k * p) / 8))
    d1 = lambda p: mp.diff(f, p); d2 = lambda p: mp.diff(f, p, 2); eps = lambda p: d1(p) ** 2 / 2
    p = mp.mpf(6)
    while eps(p) < 1: p -= mp.mpf("0.02")
    while eps(p) > 1: p -= mp.mpf("0.02")
    pend = mp.findroot(lambda q: eps(q) - 1, (p, p + mp.mpf("0.02")), solver="anderson")
    out, N, q, dq = [], mp.mpf(0), pend, mp.mpf("-0.002")
    for Ns in (55.7, 57):
        while N < Ns: N += -dq / abs(d1(q)); q += dq
        out.append((Ns, float(1 + 2 * d2(q) - d1(q) ** 2), float(8 * d1(q) ** 2)))
    tail = -d1(mp.log(178) / k)             # |dlnV/dphi| at x = 89 (u = 178)
    return out, float(tail)
tcc = float(k)
for g in (0, 0.002, 0.005, 0.0085, 0.012, 0.02):
    out, lam = run(mp.mpf(g))
    print(f"gamma {g:6}: " + "; ".join(f"N*={a}: n_s={b:.4f} r={c:.4f}" for a, b, c in out)
          + f"; tail slope at x=89 {lam:.4f} (TCC {tcc:.4f}{' VIOLATED' if lam < tcc - 1e-6 else ''})", flush=True)
