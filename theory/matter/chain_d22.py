"""D22: the full chain in the plateau -> cliff -> tail arrangement (sugra_mirror.py with mu = 1e4 so the tail starts
after the cliff, m2 = 1, kick switching on at the cliff scale mk = m2/(2n)), with radiation (instant preheating f) and
the MATTER Boltzmann equation on the model's own angle-speed history (as matter_from_mirror.py). Exploratory. AI-assisted."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "inflation"))
import sugra_mirror as M, sugra_mirror_radiation as R
MP = 2.435e18; v = 174.0; gs = 106.75; cA = math.sqrt(3 / 8); KEQ = 45 / (2 * math.pi ** 2 * gs) * 0.5227; TARGET = 8.7e-11
MASSES = [0.0, 0.0086e-9, 0.0502e-9]
GW = lambda T: 3 * T ** 3 * sum(m * m for m in MASSES) / (4 * math.pi ** 3 * v ** 4)


def chain(delta, n=10.0, f=0.99, p0=-10.0, Nafter=6.0, step=0.05):
    kw = dict(mu=1e4, a=1.0, n=n, m2c=1.0, mk=1.0 / (2 * n), p0=p0)
    rows = R.run(delta, f, Nafter=Nafter, step=step, **kw)
    Y = 0.0; pts = []
    for dN, T, r, sh, rs in rows:
        H = math.sqrt(math.pi ** 2 * gs / 30 * T ** 4 / max(rs, 1e-12) / 3) / MP
        pts.append((dN, T, r, H, sh))
    for (n0, T0, r0, H0, _), (n1, T1, r1, H1, _) in zip(pts, pts[1:]):
        T = 0.5 * (T0 + T1); H = 0.5 * (H0 + H1); r = 0.5 * (r0 + r1); k = GW(T) / H; Yeq = -KEQ * cA * r * H / T
        Y = Yeq + (Y - Yeq) * math.exp(-k * (n1 - n0))
    return (28 / 79) * abs(Y), pts


if __name__ == "__main__":
    for n in (10.0,):
        o = M.run(delta=0.0, mu=1e4, m2=1.0, n=n, p0=-10.0, Nafter=0.0, mk=1.0 / (2 * n))
        print(f"n {n}: inflation N_end {o['N_end']:.1f}, n_s {o['n_s']:.4f}, r {o['r_t']:.4f}")
        for d in (1e-3, 1e-2):
            nb, pts = chain(d, n)
            peak = max(p[4] for p in pts); rT = [(round(p[1], -11), round(p[2], 4)) for p in pts[::20]]
            print(f"  delta {d}: n_B/s {nb:.2e} (x{nb / TARGET:.2f} of observed); peak angle share {peak:.1e}; (T, r) {rT[:6]}")
