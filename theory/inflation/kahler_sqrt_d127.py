"""D127: move the 1/sqrt(1 + T/mu) factor from W (where it needs a negative-power threshold) into the Kahler metric of S:
K = -3 ln(T + Tbar - S Sbar (1 + (T + Tbar)/(2 mu)) + zeta (S Sbar)^2)  =>  at S = 0, K^{S Sbar} gains 1/(1 + x/mu), so
V = m^2 |T cliff(T)|^2 / (4 x^2 (1 + x/mu))   vs the old   m^2 |T cliff(T)|^2 / (4 x^2 |1 + T/mu|).
Identical for real T (so inflation, n_s, r, the tail are unchanged); they differ only in the angle y. Compare the angle mass m_y^2/H^2.
AI-assisted."""
import mpmath as mp
mp.mp.dps = 40
MU, NN, m2 = 1, 125, 4 / mp.pi
cl = lambda T: mp.exp(-NN * (1 - mp.exp(-T / m2)))
V_old = lambda x, y: abs(mp.mpc(x, y) * cl(mp.mpc(x, y))) ** 2 / (4 * x * x * abs(1 + mp.mpc(x, y) / MU))
V_new = lambda x, y: abs(mp.mpc(x, y) * cl(mp.mpc(x, y))) ** 2 / (4 * x * x * (1 + x / MU))
if __name__ == "__main__":
    for x in (mp.mpf("1.3e-4"), mp.mpf("1e-3"), mp.mpf("0.01"), mp.mpf("0.1"), mp.mpf(1), mp.mpf(89)):
        out = []
        for lab, V in (("old", V_old), ("new", V_new)):
            d2 = mp.diff(lambda y: V(x, y), 0, 2)
            out.append(f"{lab}: m_y^2/H^2 {float(d2 / (3 / (4 * x * x)) / (V(x, 0) / 3)):+.4f}")
        print(f"x {float(x):.1e}: " + "  ".join(out) + f"   V equal at y=0: {mp.almosteq(V_old(x,0), V_new(x,0))}")
