"""D185: can a larger heat share put today's field value inside the weakly coupled heterotic window (6.4 < x < 10.1, D164)? AI-assisted.
Freeze/thaw on the reshaped cliff for higher heat shares; report frozen and today's x, w0, wa, and the heterotic coupling g_s ~ g_YM R^3
with R^2 = x/8 (D164)."""
import math, cliff_v2 as C
lnV, _ = C.version("exp", 4 / math.pi)
gYM = math.sqrt(4 * math.pi / 25)
for f in (0.02, 0.05, 0.07, 0.1, 0.15, 0.25):
    pf = C.freeze(lnV, f); w0, wa, p0 = C.thaw(lnV, pf); xf, xt = math.exp(C.c * pf), math.exp(C.c * p0)
    gs = gYM * (xt / 8) ** 1.5
    print(f"heat {100*f:5.1f}%: frozen x {xf:6.2f}, today x {xt:6.2f}, w0 {w0:.4f}, wa {wa:.4f}, heterotic g_s today ~ {gs:.2f} {'(weak)' if gs < 1 else '(strong)'}", flush=True)
