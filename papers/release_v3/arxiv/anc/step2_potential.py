"""Plan step 2: can geometry produce V = Lambda^4 [1 - cos(phi/F)]^3?

(1) What is special about n = 3: expand (1 - cos x)^n in harmonics and near its minimum.
(2) Instanton-type series V = sum_k a_k cos(k x): which conditions give a flat (x^6) bottom like n = 3?
(3) A generic (dilute-gas) series a_k ~ (-r)^k: does it ever have a flat bottom?
(4) The chiral (QCD-like) axion potential from an anomaly: its shape near the minimum.
Run: python step2_potential.py
"""
import numpy as np
import sympy as sp

x, r, z = sp.symbols("x r z", real=True)

print("(1) harmonics and small-x behaviour of (1 - cos x)^n")
for n in (1, 2, 3):
    v = sp.expand(sp.fu((1 - sp.cos(x)) ** n))
    harm = sp.expand(sp.expand_trig(v).rewrite(sp.exp).rewrite(sp.cos))
    print(f"    n={n}: {sp.simplify(sp.fu(v))}   series: {sp.series((1 - sp.cos(x)) ** n, x, 0, 8).removeO()}")
a = {1: sp.Rational(-15, 4), 2: sp.Rational(3, 2), 3: sp.Rational(-1, 4)}
print("    n=3 harmonic amplitudes a1, a2, a3 =", a[1], a[2], a[3])
print("    sum k^2 a_k =", sum(k ** 2 * a[k] for k in a), "  sum k^4 a_k =", sum(k ** 4 * a[k] for k in a),
      "  -> both vanish: no x^2 and no x^4 term, so V ~ x^6/8 (flat bottom)")

print("\n(2) a series sum_k a_k cos(kx) has V - V(0) = -sum a_k (k x)^2/2 + sum a_k (k x)^4/24 - ...")
print("    flat bottom like n=3 needs TWO exact cancellations: sum k^2 a_k = 0 and sum k^4 a_k = 0")

print("\n(3) dilute instanton gas a_k = (-r)^k / k (and a_k = (-r)^k): curvature at the minimum")
for name, ak in (("a_k=(-r)^k", lambda k: (-r) ** k), ("a_k=(-r)^k/k", lambda k: (-r) ** k / k)):
    m2 = -sum(k ** 2 * ak(k) for k in range(1, 60))           # coefficient of x^2/2 near x = 0 (or x = pi)
    for rv in (0.1, 0.3, 0.5, 0.8):
        print(f"    {name}: r={rv}: x^2 coefficient = {float(m2.subs(r, rv)):+.4f} (never zero for 0<r<1)")
xs = np.linspace(-np.pi, np.pi, 4001)
for rv in (0.3, 0.6):
    V = sum(-(-rv) ** k * np.cos(k * xs) for k in range(1, 80))
    V -= V.min()
    x0 = xs[np.argmin(V)]
    curv = sum((-rv) ** k * k ** 2 * np.cos(k * x0) for k in range(1, 80))      # V''(x0) for V = -sum (-r)^k cos kx
    print(f"    geometric series r={rv}: minimum at x={x0:+.3f}, V''(min) = {curv:.3f} > 0: a mass term, "
          f"so it behaves like n = 1")

print("\n(4) chiral axion potential (anomaly + confining sector), z = mass ratio:")
Vch = -sp.sqrt(1 - 4 * z / (1 + z) ** 2 * sp.sin(x / 2) ** 2)
ser = sp.series(Vch, x, 0, 6).removeO()
print("    V ~", sp.simplify(ser), " -> x^2 term present: n = 1 behaviour near the minimum")
