"""Development 76b: past the cliff the twist angle y is tachyonic at y = 0; where is its valley, and does the tail's
dark-energy slope change along it? V(x, y) = |F(x + i y)|^2 / (4 x^2), mu = 1, n = 125, m2 = 1. AI-assisted."""
import math
import mpmath as mp
mp.mp.dps = 30
MU, N, M2 = 1, 125, 1
c = math.sqrt(2 / 3)
F = lambda T: T / mp.sqrt(1 + T / MU) * mp.exp(-N * T / (T + M2))
V = lambda x, y: abs(F(mp.mpc(x, y))) ** 2 / (4 * x * x)
rows = []
for x in (0.03, 0.1, 0.3, 1, 3, 10, 30, 100):
    x = mp.mpf(x)
    ys = [mp.mpf(10) ** (k / 8) for k in range(-24, 33)]
    vals = [V(x, y) for y in ys]; i = min(range(len(ys)), key=lambda k: vals[k])
    y0 = mp.findroot(lambda y: mp.diff(lambda t: V(x, t), y), ys[i]) if 0 < i < len(ys) - 1 else ys[i]
    rows.append((x, y0, V(x, y0) / V(x, 0)))
    print(f"x {float(x):7.2f}: valley at y = {float(y0):9.3f} (y/x {float(y0 / x):7.2f}), V_valley/V(y=0) = {float(V(x, y0) / V(x, 0)):.3e}")
print("\nslope of ln V vs canonical distance along the valley (y = 0 line gives sqrt(2/3) x correction):")
for (x1, y1, _), (x2, y2, _) in zip(rows, rows[1:]):
    # field-space distance with metric 3/(4x^2)(dx^2 + dy^2) -> ds = sqrt(3/2) sqrt(dx^2 + dy^2) / x (midpoint)
    xm = (x1 + x2) / 2; ds = mp.sqrt(1.5) * mp.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / xm
    s_valley = abs(mp.log(V(x2, y2)) - mp.log(V(x1, y1))) / ds
    s_zero = abs(mp.log(V(x2, 0)) - mp.log(V(x1, 0))) / (mp.sqrt(1.5) * abs(x2 - x1) / xm)
    print(f"  x {float(x1):6.2f}-{float(x2):6.2f}: valley slope {float(s_valley):.3f}, y=0 slope {float(s_zero):.3f} (sqrt(2/3) = 0.816)")
