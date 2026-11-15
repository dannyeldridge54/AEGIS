"""First-pass stability (Floquet) check of the Locked Twist field oscillation (ROADMAP_MATH.md step 3.5).

Potential V = Lambda^4 [1 - cos(phi/F)]^3. In units x = phi/F and time in 1/m with m^2 = Lambda^4/F^2:
  background   x'' = -V'(x),            V'(x)  = 3 (1 - cos x)^2 sin x
  ripples      d'' + (k^2 + V''(x(t))) d = 0,
               V''(x) = 6 (1 - cos x) sin^2 x + 3 (1 - cos x)^2 cos x
For a field released at rest at x0 = theta_i, integrate one oscillation period T, build the monodromy matrix for each
wavenumber k, and read the Floquet exponent mu_k = ln|largest multiplier| / T. Report the instability bands and the
largest growth per oscillation, mu_max / omega with omega = 2 pi / T.

Limits (first pass): no Hubble expansion, so the amplitude does not decay here; in the real universe it falls
after release and the resonance band sweeps. Growth only matters if mu exceeds the Hubble rate for long enough;
near release omega ~ H, so mu/omega is roughly the growth per Hubble time at that moment.

Run: python floquet_twist.py
"""
import numpy as np
from scipy.integrate import solve_ivp


def dV(x):
    return 3 * (1 - np.cos(x)) ** 2 * np.sin(x)


def d2V(x):
    return 6 * (1 - np.cos(x)) * np.sin(x) ** 2 + 3 * (1 - np.cos(x)) ** 2 * np.cos(x)


def period(x0):
    """Time for the field released at rest at x0 to cross x = 0 the second time... i.e. one full oscillation."""
    ev = lambda t, y: y[1]                              # velocity zero = turning point
    ev.terminal, ev.direction = False, 0
    sol = solve_ivp(lambda t, y: [y[1], -dV(y[0])], (0, 400), [x0, 0.0], events=ev, rtol=1e-11, atol=1e-12,
                    dense_output=True)
    turns = sol.t_events[0]
    turns = turns[turns > 1e-6]
    return 2 * turns[0], sol                            # first turning point is half a period


def floquet(x0, ks):
    T, bg = period(x0)
    out = []
    for k in ks:
        def rhs(t, y):
            x = bg.sol(t)[0]
            return [y[1], -(k * k + d2V(x)) * y[0], y[3], -(k * k + d2V(x)) * y[2]]
        s = solve_ivp(rhs, (0, T), [1, 0, 0, 1], rtol=1e-10, atol=1e-12)
        M = np.array([[s.y[0, -1], s.y[2, -1]], [s.y[1, -1], s.y[3, -1]]])
        lam = np.max(np.abs(np.linalg.eigvals(M)))
        out.append(np.log(lam) / T)
    return T, np.array(out)


if __name__ == "__main__":
    # k -> 0 is the homogeneous mode, which only drifts linearly (amplitude-dependent period), so start at 0.1.
    ks = np.linspace(0.1, 8.0, 400)
    for x0, label in ((2.41421, "silver-ratio prediction"), (2.7887, "Planck best fit (START_EDE)"), (2.0, ""),
                      (1.0, ""), (3.0, "")):
        T, mu = floquet(x0, ks)
        w = 2 * np.pi / T
        band = ks[mu > 1e-3]
        i = int(np.argmax(mu))
        bands = "none" if band.size == 0 else f"k = {band.min():.2f}-{band.max():.2f}"
        print(f"theta_i = {x0:.5f} {('(' + label + ')') if label else '':30s} omega = {w:.4f}  "
              f"unstable {bands:18s} max mu = {mu[i]:.4f} at k = {ks[i]:.2f}  mu_max/omega = {mu[i] / w:.4f}")
