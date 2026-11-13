"""D204: TWIST-M9 freeze and thaw computed (not calibrated): today's x and heterotic g_s versus heat share. AI-assisted.
Same freeze/thaw machinery as D185 (cliff_v2.freeze / thaw), with the M9 potential: lnV(x) = -2n h9/(1+h9) - ln(4(1 + x/mu)),
h9 = h(x/72)^9, h = (eta(iy)/eta(9iy))^3 (D196), x = Re T. Heterotic coupling g_s ~ g_YM (x/72)^(3/2) (Im T_het = x/72, R^2 = T_het)."""
import math, mpmath as mp, cliff_v2 as C
mp.mp.dps = 20
n = 125
def eta(y): return mp.e ** (-2 * mp.pi * y / 24) * mp.qp(mp.e ** (-2 * mp.pi * y))
def h(y):
    y = mp.mpf(y)
    if y < mp.mpf(1) / 3: return (3 * eta(1 / y) / eta(1 / (9 * y))) ** 3
    return (eta(y) / eta(9 * y)) ** 3
def lnV(p):
    x = math.exp(C.c * p)
    lh9 = 9 * float(mp.log(h(x / 72)))
    s = 1 / (1 + math.exp(-lh9)) if lh9 > -700 else 0.0      # h9/(1+h9)
    return -2 * n * s - math.log(4 * (1 + x / C.MU))
C.DL = lambda p, hh=1e-5: (lnV(p + hh) - lnV(p - hh)) / (2 * hh)   # numerical slope (cliff_v2.d uses the global DL)
gYM = math.sqrt(4 * math.pi / 25)
for f in (0.008, 0.05, 0.2, 0.35, 0.5):
    try:
        pf = C.freeze(lnV, f, p0=math.log(0.5) / C.c)
        w0, wa, p0 = C.thaw(lnV, pf); xf, xt = math.exp(C.c * pf), math.exp(C.c * p0)
        gs = gYM * (xt / 72) ** 1.5
        print(f"heat {100*f:5.1f}%: frozen x {xf:9.4g}, today x {xt:9.4g}, w0 {w0:.4f}, wa {wa:.4f}, g_s today ~ {gs:.3g}", flush=True)
    except Exception as e:
        print(f"heat {100*f:5.1f}%: solver failed ({type(e).__name__}: {e})", flush=True)
