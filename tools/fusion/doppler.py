"""N5: exact free-gas (Solbrig) Doppler broadening of a pointwise 0 K cross section (piecewise-linear in E)."""
import numpy as np
KB = 8.617333262e-5
def broaden(E0, s0, awr, T, Eout, nsub=400, width=5.0):
    alpha = awr / (KB * T); sa = np.sqrt(alpha); x0 = np.sqrt(E0); out = np.empty_like(Eout, dtype=float)
    for i, E in enumerate(Eout):
        y = np.sqrt(E); lo, hi = max(0.0, y - width / sa), y + width / sa
        xs = np.union1d(np.linspace(lo, hi, nsub), x0[(x0 > lo) & (x0 < hi)])
        sx = np.interp(xs * xs, E0, s0, left=0.0, right=0.0)
        lo_m = xs * xs < E0[0]   # audit R99: 1/v extension below the lowest grid point (was zero)
        if lo_m.any(): sx[lo_m] = s0[0] * np.sqrt(E0[0] / np.maximum(xs[lo_m] ** 2, 1e-30))
        k = np.exp(-alpha * (xs - y) ** 2) - np.exp(-alpha * (xs + y) ** 2)
        out[i] = np.sqrt(alpha / np.pi) / (y * y) * np.trapezoid(xs * xs * sx * k, xs)
    return out
