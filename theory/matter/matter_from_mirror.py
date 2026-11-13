"""D21b: matter made by the mirrored model's actual angle-speed history (sugra_mirror_radiation.py), through the same
Boltzmann equation as MATTER (boltzmann_leptogenesis.py): dY/dN = -(Gamma_W/H)(Y - Y_eq), Y_eq = -KEQ mu_A/T,
mu_A/T = c_A r H / T (r = angle speed / (H M_P)), H from the model itself (not assumed radiation), n_B/s = (28/79)|Y|.
Exploratory, not a locked test. AI-assisted."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "inflation"))
import sugra_mirror_radiation as R
from scipy.integrate import solve_ivp
MP = 2.435e18; v = 174.0; gs = 106.75
cA = math.sqrt(3 / 8); KEQ = 45 / (2 * math.pi ** 2 * gs) * 0.5227; TARGET = 8.7e-11
MASSES = [0.0, 0.0086e-9, 0.0502e-9]
GW = lambda T: 3 * T ** 3 * sum(m * m for m in MASSES) / (4 * math.pi ** 3 * v ** 4)


def history(delta, f=0.99, Nafter=6.0, step=0.05):
    V, G, Mm = R.M.make(1.0, delta, 1.0, 10.0, 100.0)
    rows = R.run(delta, f, Nafter=Nafter, step=step)
    return rows


def nbs(delta, f=0.99):
    rows = history(delta, f)
    # need H: recompute from T and radiation share: rho_r = (pi^2 g/30) T^4, 3 H^2 M_P^2 = rho_r / share
    pts = []
    for dN, T, r, sh, rs in rows:
        rho_r = math.pi ** 2 * gs / 30 * T ** 4
        H = math.sqrt(rho_r / max(rs, 1e-12) / 3) / MP
        pts.append((dN, T, r, H))
    Y = 0.0
    for (n0, T0, r0, H0), (n1, T1, r1, H1) in zip(pts, pts[1:]):
        dn = n1 - n0; T = 0.5 * (T0 + T1); H = 0.5 * (H0 + H1); r = 0.5 * (r0 + r1)
        k = GW(T) / H; Yeq = -KEQ * cA * r * H / T
        Y = Yeq + (Y - Yeq) * math.exp(-k * dn)          # exact step for the linear relaxation
    return (28 / 79) * abs(Y), pts


if __name__ == "__main__":
    for d in (0.003, 0.01, 0.03):
        nb, pts = nbs(d)
        print(f"delta {d}: n_B/s = {nb:.2e}  (target 8.7e-11; ratio {nb / TARGET:.2f})")
    nb1, _ = nbs(0.01)
    print(f"-> delta needed ~ {0.01 * TARGET / nb1:.4f} (n_B/s is linear in delta for small delta)")
