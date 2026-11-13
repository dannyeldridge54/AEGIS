"""D28: Development 27's candidate fix. The angle term (eq. 5, base frame) shares the hidden sector of the cliff, so it
carries the cliff factor |exp(-nT/(T+m2))|^2 too. Realistic cliff n = 125. Otherwise as full_chain_sugra.py. AI-assisted.
RESULT (12 Nov, 21:25 CT): FAILS. Matter forms after the cliff, where the shared factor suppresses the kick by ~e^-250:
n_B/s = 4e-11 to 4e-9 of observed for eps 1e-4 to 1e-2; the observed amount would need eps ~ 1e6 (unphysical)."""
import cmath, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import full_chain_sugra as S
S.N = 125.0


def make(eps, gamma):
    def V(p, y):
        x = math.exp(S.c * p); T = complex(x, y)
        cliff = cmath.exp(-S.N * T / (T + S.M2))
        F0 = T / cmath.sqrt(1 + T / S.MU) * cliff
        To = 1 / T; xo, yo = To.real, To.imag
        return abs(F0) ** 2 / (4 * x * x) + abs(cliff) ** 2 * eps * math.exp(-S.A * xo) * math.cos(S.A * yo + gamma) / (2 * xo * xo)
    def G(p, y, h=1e-6):
        v = V(p, y)
        return (V(p + h, y) - V(p - h, y)) / (2 * h) / v, (V(p, y + h) - V(p, y - h)) / (2 * h) / v
    return V, G


S.make = make
if __name__ == "__main__":
    for eps in (1e-4, 1e-3, 1e-2):
        o = S.run(eps, p0=-13.0, Nafter=5.0)
        m32 = S.m_inf * S.MP * math.sqrt(eps / (8 * S.A))
        print(f"eps {eps:.0e} (m_3/2 ~ {m32:.1e} GeV): N_end {o['N_end']:.1f} n_s {o['n_s']:.4f} r {o['r_t']:.4f} | "
              f"n_B/s {o['nBs']:.2e} (x{o['nBs'] / S.C.TARGET:.2g}) | peak angle share {o['peak_angle_share']:.1e}", flush=True)
