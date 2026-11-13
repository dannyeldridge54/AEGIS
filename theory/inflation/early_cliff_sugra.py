"""Backlog O step 1 (exploratory): can the supergravity model's own knobs (n, m2) put the cliff early enough to raise n_s?
Real direction of the mirrored model: V(p) = |F0(x)|^2 / (4 x^2), x = exp(c p), F0 = x/sqrt(1+x/mu) exp(-n x/(x+m2)).
For x << m2:  V ~ (1/4) exp(-(2n/m2) x) = (1/4) exp(-exp(c (p - p_s))), p_s = ln(m2/2n)/c  -> m2 and n only SHIFT p
unless the saturation x ~ m2 lies inside the last ~60 e-folds. Slow roll on the exact V(p) (p canonical along the real
axis, as in the model code), V scale from A_s, N* self-consistent (instant reheating). AI-assisted."""
import math
from scipy.integrate import quad
from scipy.optimize import brentq

c = math.sqrt(2 / 3); AS = 2.1e-9; G = 106.75; H0c = 67.4 / 299792.458; KSTAR = 0.05


def model(n, m2, mu=1e4):
    lnV = lambda p: (-2 * n * math.exp(c * p) / (math.exp(c * p) + m2)) - math.log(4 * (1 + math.exp(c * p) / mu))
    def d1(p):
        x = math.exp(c * p); return c * x * (-2 * n * m2 / (x + m2) ** 2 - 1 / (mu + x))
    d2 = lambda p, h=1e-5: (d1(p + h) - d1(p - h)) / (2 * h)
    eps = lambda p: 0.5 * d1(p) ** 2
    eta = lambda p: d2(p) + d1(p) ** 2                      # V''/V
    # inflation runs toward larger p; end where eps = 1 (first crossing from the plateau)
    grid = [-30 + 0.01 * i for i in range(6000)]
    pend = next(p for p in grid if eps(p) >= 1)
    Nback = lambda p: quad(lambda q: 1 / math.sqrt(2 * eps(q)), p, pend, limit=200)[0]
    def at(N):
        return brentq(lambda p: Nback(p) - N, pend - 25, pend - 1e-6)
    N = 55.0
    for _ in range(60):
        p = at(N); e = eps(p); Vs = 24 * math.pi ** 2 * AS * e; rho_end = 1.5 * Vs * math.exp(lnV(pend) - lnV(p))
        Nn = 66.89 - math.log(KSTAR / H0c) + 0.25 * math.log(Vs ** 2 / rho_end) - math.log(G) / 12
        if abs(Nn - N) < 1e-6:
            break
        N = Nn
    p = at(N); e = eps(p)
    return {"n": n, "m2": m2, "N*": round(N, 2), "n_s": round(1 - 6 * e + 2 * eta(p), 5), "r": round(16 * e, 5),
            "x_end/m2": math.exp(c * pend) / m2}


if __name__ == "__main__":
    print(f"Inflation can end on the cliff only if n > 2 sqrt(2)/c = {2 * math.sqrt(2) / c:.3f}")
    for n, m2 in ((125, 1.0), (125, 100.0), (10, 1.0), (6, 1.0), (4.5, 1.0), (4.0, 1.0), (3.7, 1.0), (3.55, 1.0), (3.5, 1.0), (3.47, 1.0), (3.0, 1.0)):
        try:
            o = model(n, m2)
        except StopIteration:
            print(f"n {n:>5}, m2 {m2:>5}: inflation never ends on the cliff (slope stays below sqrt 2)"); continue
        print(f"n {n:>5}, m2 {m2:>5}: N* {o['N*']}, n_s {o['n_s']}, r {o['r']}, x_end/m2 {o['x_end/m2']:.2e}", flush=True)
