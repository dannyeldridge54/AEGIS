"""Development 78 (exploratory): the slope the frozen field really sees today, including the cliff factor. AI-assisted.
tail_freeze.py (Backlog L) found where the field freezes (x_f) but took the slope today as c x/(x + mu), keeping only the
mu factor. The full tail V = m^2 exp(-2n x/(x+m2)) / (4 (1 + x/mu)) has
    -d ln V / d phi = c x [ 2 n m2/(x + m2)^2 + 1/(x + mu) ],
and the first term (the cliff's leftover slope) is not small unless x_f >> 2n m2. Here: x_f from tail_freeze.run for
heat shares f in the derived range (D42: 0.04-0.4%), the full slope, the angle's mass there (D76), and w0, wa for a
thawing field with that slope (background, exponential approximation, CPL fit over z < 2 as effective_w.py)."""
import math, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, "theory/darkenergy")
from tail_freeze import run
c = math.sqrt(2 / 3); n, m2, mu = 125.0, 1.0, 1.0
Om, Or = 0.31, 9.1e-5; ODE = 1 - Om - Or


def thaw(lam):
    def go(V0):
        def rhs(N, y):
            p, v = y; a = math.exp(N); V = V0 * math.exp(-lam * p)
            H2 = (Om * a ** -3 + Or * a ** -4 + V / 3) / (1 - v * v / 6)
            eps = (1.5 * Om * a ** -3 + 2 * Or * a ** -4 + 0.5 * v * v * H2) / H2
            return [v, -(3 - eps) * v + lam * V / H2]
        return solve_ivp(rhs, [math.log(1e-4), 0], [0, 0], rtol=1e-9, atol=1e-12, dense_output=True)
    def ode(V0):
        s = go(V0); p, v = s.y[:, -1]; V = V0 * math.exp(-lam * p); H2 = (Om + Or + V / 3) / (1 - v * v / 6)
        return (v * v * H2 / 6 + V / 3) / H2 - ODE
    V0 = brentq(ode, 1e-2, 1e3); s = go(V0); a = np.linspace(1 / 3, 1, 300); w = []
    for N in np.log(a):
        p, v = s.sol(N); A = math.exp(N); V = V0 * math.exp(-lam * p)
        H2 = (Om * A ** -3 + Or * A ** -4 + V / 3) / (1 - v * v / 6); K = v * v * H2 / 6; w.append((K - V / 3) / (K + V / 3))
    return np.linalg.lstsq(np.vstack([np.ones(300), 1 - a]).T, np.array(w), rcond=None)[0]


w0r, war = thaw(c)
print(f"reference, slope sqrt(2/3) (PURE-TWIST): w0 {w0r:.3f}, wa {war:.3f}")
for f in (4e-4, 1.3e-3, 4e-3, 1.47e-2):
    xf = run(mu, n=n, m2=m2, f=f)[0]
    slope = c * xf * (2 * n * m2 / (xf + m2) ** 2 + 1 / (xf + mu))
    my = 2 - 8 * n * xf ** 2 / (xf + 1) ** 3
    try:
        w0, wa = thaw(slope); wtxt = f"w0 {w0:.3f}, wa {wa:.3f}"
    except ValueError:
        wtxt = "no thawing solution with Omega_DE 0.69"
    print(f"heat share {f * 100:.2f}%: frozen at x = {xf:.0f}; old slope {c * xf / (xf + mu) / c:.3f}, full slope "
          f"{slope / c:.2f} x sqrt(2/3) = {slope:.2f}; angle m_y^2/H^2 {my:+.2f}; {wtxt}")
