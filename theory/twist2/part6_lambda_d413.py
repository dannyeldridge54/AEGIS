"""D413 (locked PREREG_D413_PART6): Part 6 (Λ from the cliff at x_E) — sensitivity of Λ to the capture point. AI-assisted.
Uses the Twist potential V(x, y=0) from cliff_v2 ('exp', m2 = 4/π)."""
import math, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.join(ROOT, "theory", "inflation")); sys.argv = sys.argv[:1]
import cliff_v2 as C
lnV, Fc = C.version("exp", 4 / math.pi); c = math.sqrt(2 / 3)
for xE in (27.0, 28.0, 29.0, 29.6, 29.83):
    p = math.log(xE) / c; h = 1e-4
    print(f"x_E {xE:6.2f}:  d ln V / d ln x = {(lnV(p + h) - lnV(p - h)) / (2 * h) / c:+.4f}   ln V = {lnV(p):.3f}")
print("Λ change for x_E 29.6 → 29.83:", f"{math.exp(lnV(math.log(29.83)/c) - lnV(math.log(29.6)/c)) - 1:+.4%}")
