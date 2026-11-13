"""D25: the kick as a Nieh-Yan instanton with its exponent FIXED by the derived Nieh-Yan period. AI-assisted.
Base theory: F = (4/pi) sqrt(3/2) M_P = 1.559 M_P (Nieh-Yan index), canonical angle a~ = sqrt(3/2) a at the reference
dilaton, so the angle's period is Delta a = 2 pi F / sqrt(3/2) = 8.00 (the 7 Nov "Delta beta = 8"). An instanton term
e^{-A T_o} (T_o the base-frame field, Im T_o = angle) has period 2 pi / A in the angle -> A = 2 pi / 8 = pi/4.
In the mirrored model (sugra_mirror.py, T = 1/T_o) the kick term e^{-a mk / T} = e^{-a mk T_o}, so a*mk = pi/4 is fixed.
Its size is then exp(-(pi/4) Re T_o) at the kick: S = (pi/4) x_o, set by where inflation ends, not by a free delta.
Here delta = 1 (natural prefactor) and the cliff position m2 is scanned; MATTER rate equation as chain_d22.py."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "inflation")); sys.path.insert(0, HERE)
import sugra_mirror as M, sugra_mirror_radiation as R, chain_d22 as C
A = math.pi / 4
print(f"Nieh-Yan period in the angle: {2 * math.pi * (4 / math.pi) * math.sqrt(1.5) / math.sqrt(1.5):.3f} -> instanton exponent A = {A:.4f}")


def chain(m2, n=10.0, f=0.99, delta=1.0, p0=None, Nafter=6.0, step=0.05):
    p0 = p0 if p0 is not None else (math.log(m2 / (2 * n)) / M.c - 6.3)
    kw = dict(mu=1e4, a=1.0, n=n, m2c=m2, mk=A, p0=p0)
    o = M.run(delta=0.0, mu=1e4, a=1.0, n=n, m2=m2, p0=p0, Nafter=0.0, mk=A)
    rows = R.run(delta, f, Nafter=Nafter, step=step, **kw)
    Y = 0.0; pts = []
    for dN, T, r, sh, rs in rows:
        H = math.sqrt(math.pi ** 2 * C.gs / 30 * T ** 4 / max(rs, 1e-12) / 3) / C.MP; pts.append((T, r, H))
    for (T0, r0, H0), (T1, r1, H1) in zip(pts, pts[1:]):
        T = 0.5 * (T0 + T1); H = 0.5 * (H0 + H1); r = 0.5 * (r0 + r1); k = C.GW(T) / H; Yeq = -C.KEQ * C.cA * r * H / T
        Y = Yeq + (Y - Yeq) * math.exp(-k * step)
    return o, (28 / 79) * abs(Y), max(abs(p[1]) for p in pts)


if __name__ == "__main__":
    for m2 in (0.5, 1.0, 2.0):
        o, nb, rmax = chain(m2)
        x_end = math.exp(M.c * 0) if o is None else None
        print(f"cliff m2 {m2}: N_end {o['N_end']:.1f}, n_s {o['n_s']:.4f}, r {o['r_t']:.4f} | n_B/s {nb:.2e} "
              f"(x{nb / C.TARGET:.2g} of observed), peak angle speed {rmax:.2e}", flush=True)
