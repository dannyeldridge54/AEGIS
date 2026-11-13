"""D19c: the scaled kick in the cliff model, stepped through kination (fields only, no radiation). AI-assisted.
Model: sugra_cliff.py, mu = 1, a = 1, n = 10, m2 = 0.01, scaled kick. Result (12 Nov): N_end ~129, n_s 0.961, r_t 0.0047;
angle speed at the end r = 0.067 (delta 0.3); m_y/H falls to ~0.04 (free roll) but r falls ~e^-2 per e-fold as the inflaton
descends (g_yy = 1.5 e^{-2 c phi} grows): r >= 0.02 only for ~1.3 e-folds after the end. Beyond ~3.5 e-folds the
fields-only run is not physical (no radiation)."""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sugra_cliff as S
from scipy.integrate import solve_ivp
c = S.c
for delta in (0.1, 0.3):
    V, G, M = S.make(1.0, delta, 1.0, 10.0, 0.01, scaled=True)
    def rhs(N, z):
        p, y, dp, dy = z; g = 1.5 * math.exp(-2 * c * p); e = 0.5 * (dp * dp + g * dy * dy); gp, gy = G(p, y)
        return [dp, dy, -c * g * dy * dy - (3 - e) * (dp + gp), 2 * c * dp * dy - (3 - e) * (dy + gy / g)]
    end = lambda N, z: 0.5 * (z[2] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[3] ** 2) - 1; end.terminal = True; end.direction = 1
    s = solve_ivp(rhs, [0, 200], [5.6, 0, 0, 0], events=end, rtol=1e-8, atol=1e-11, method="LSODA", dense_output=True)
    Ne = s.t_events[0][0]; z = s.y_events[0][0]; N = Ne
    print(f"\ndelta {delta}: N_end {Ne:.1f}")
    for k in range(14):
        z = solve_ivp(rhs, [N, N + 0.25], z, rtol=1e-7, atol=1e-10, method="LSODA").y[:, -1]; N += 0.25
        p, y, dp, dy = z; g = 1.5 * math.exp(-2 * c * p); e = 0.5 * (dp * dp + g * dy * dy)
        print(f"  N-N_end {N - Ne:4.2f} eps {e:5.3f} phi {p:+7.3f} m_y/H {math.sqrt(max(M(p, y) / g * (3 - e), 0)):9.2e} r {math.sqrt(g) * abs(dy):.3e}")
