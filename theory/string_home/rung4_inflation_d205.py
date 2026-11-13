"""D205: inflation on rung 4 (heterotic M-theory's matter-neutral direction, D184), same plateau shape as the Twist. AI-assisted.
E-model plateau V = (1 - e^{-k phi})^2 (same exponential approach as the Twist; its end is set by the cliff, here by eps = 1), k = sqrt(2/(3 alpha)):
rung 3 (alpha = 1) k = sqrt(2/3) as a check; rung 4 (alpha = 4/3) k = sqrt(1/2). End at eps = 1, then N* back."""
import mpmath as mp
mp.mp.dps = 30
def run(k, label):
    f = lambda p: 2 * mp.log(1 - mp.e ** (-k * p))
    d1 = lambda p: mp.diff(f, p); d2 = lambda p: mp.diff(f, p, 2); eps = lambda p: d1(p) ** 2 / 2
    pend = mp.findroot(lambda p: eps(p) - 1, 1)
    out = []; N, q, dq = mp.mpf(0), pend, mp.mpf("0.002")
    for Ns in (55.7, 57):
        while N < Ns: N += dq / abs(d1(q)); q += dq
        out.append(f"N*={Ns}: n_s={float(1 + 2 * d2(q) - d1(q) ** 2):.4f}, r={float(8 * d1(q) ** 2):.4f}")
    print(label, "; ".join(out))
run(mp.sqrt(mp.mpf(2) / 3), "rung 3 (check vs the Twist's 0.964-0.965, r 0.0036):")
run(mp.sqrt(mp.mpf(1) / 2), "rung 4:")
