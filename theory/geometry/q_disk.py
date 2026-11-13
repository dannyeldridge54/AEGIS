"""D139: the Twist's history drawn in the cliff's own variable q = exp(-pi T/4). AI-assisted.
Im T has period 8, so q covers the unit disk exactly once: |q| = e^{-pi x/4}, arg q = -pi y/4.
Rim |q| -> 1 is x -> 0 (the inflation plateau); the centre q -> 0 is x -> infinity (the dark-energy tail).
Field space: T (2 real) + S (2 real) = 4 real dimensions, with two angles (arg q and arg S) -> a 2-torus over a 2-d base.
Kinetic metric from K = -3 ln(T+Tbar) in q: ds^2 = 3|dq|^2 / (|q|^2 (ln|q|^2)^2) -> a hyperbolic disk with a cusp at the
centre (the pseudosphere / 'horn' geometry). Potential along the cliff: exp(-2n(1 - Re q)) -> highest on the rim, lowest at the centre."""
import math, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
marks = [("CMB scales", 1.25e-4, 0.0), ("end of inflation", 0.0125, 0.0), ("after the kick", 3.3, 0.6),
         ("frozen tail", 72.7, 1.2), ("today", 88.9, 1.2)]
OFF = {"CMB scales": (-10, 10), "end of inflation": (-30, 10), "after the kick": (6, -12), "frozen tail": (8, -14), "today": (-30, 8)}
print("stage: x, |q| = e^{-pi x/4}, arg q (deg), ln|q|")
for lab, x, y in marks:
    print(f"  {lab}: x {x:g}, |q| {math.exp(-math.pi*x/4):.6g}, arg {-45*y:.0f} deg, ln|q| {-math.pi*x/4:.3g}")
n = 125; print(f"potential ratio rim/centre e^(2n) = 10^{2*n/math.log(10):.0f}; dark-energy pressure at the centre: w0 = -0.90 (p = -0.90 rho)")
print("kinetic metric 3|dq|^2/(|q| ln|q|^2)^2: distance to the centre is infinite (cusp); to the rim infinite (plateau) — both ends are boundaries")
# figure: the q-disk with an 8-fold grid, the trajectory radius on a log-stretched scale so both ends are visible
fig, ax = plt.subplots(figsize=(6, 6), dpi=150); ax.set_aspect("equal"); ax.axis("off")
th = np.linspace(0, 2*np.pi, 400); ax.plot(np.cos(th), np.sin(th), color="#555", lw=1.2)
for k in range(8):
    a = 2*np.pi*k/8; ax.plot([0, np.cos(a)], [0, np.sin(a)], color="#bbb", lw=0.6)
R = lambda x: 1 - math.log10(1 + x/1e-4)/math.log10(1 + 100/1e-4)      # display radius: rim = plateau, centre = tail
for rr in (R(1e-3), R(1e-2), R(1e-1), R(1), R(10)):
    ax.plot(rr*np.cos(th), rr*np.sin(th), color="#ddd", lw=0.5)
xs = np.logspace(-4.1, math.log10(88.9), 300); ys = np.interp(np.log10(xs), np.log10([1e-4, 0.0125, 3.3, 72.7, 88.9]), [0, 0, 0.6, 1.2, 1.2])
ax.plot([R(x)*math.cos(-math.pi*y/4) for x, y in zip(xs, ys)], [R(x)*math.sin(-math.pi*y/4) for x, y in zip(xs, ys)], color="#c0392b", lw=2)
for lab, x, y in marks:
    px, py = R(x)*math.cos(-math.pi*y/4), R(x)*math.sin(-math.pi*y/4); ax.plot(px, py, "o", color="#222", ms=4)
    ax.annotate(lab, (px, py), textcoords="offset points", xytext=OFF[lab], fontsize=7)
ax.set_title("The Twist's history in the cliff variable q = e^(−πT/4)\nrim = inflation plateau · centre = today's dark energy · 8 spokes = the period-8 angle\n(radius log-stretched; angle path between the end and the frozen tail interpolated)", fontsize=8)
plt.savefig("/home/claude/aegis/field_tests/results/q_disk.png", bbox_inches="tight")
