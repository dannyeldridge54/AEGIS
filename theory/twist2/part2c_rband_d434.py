"""D434 (locked PREREG_D434_PART2C): third pass Part 2 — the Route A prediction band: r and α_s over the ε window that keeps n_s within
0.9736 ± 0.003 (D419 model, N* = 57.2). AI-assisted."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import routeA_d419 as RA
from scipy.optimize import brentq
f = lambda e, t: RA.model(e)["ns"] - t
for t in (0.9706, 0.9736, 0.9766):
    e = brentq(lambda x: f(x, t), 1e-8, 9e-7, xtol=1e-11); m = RA.model(e)
    print(f"n_s {t:.4f}: ε = {e:.3e}  r = {m['r']:.5f}  α_s = {m['a']:+.3e}  B1 = {m['B1']:+.2e}  r_Starobinsky(same n_s) = {3*(1-t)**2:.5f}")
