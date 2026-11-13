"""Tier 2 (2): does reheating carry over to TWIST-K and TWIST-L? TWIST-K has the Twist's potential and kinetic term along real T exactly,
so its trajectory and reheating are identical. For TWIST-L (V/L, b = 3, 10) compare the inflaton's speed when it crosses chi's zero
point x0 (instant preheating: produced energy ~ (g phi_dot)^{3/2} m_chi, so heat share ~ phi_dot^{3/2}). AI-assisted."""
import math, sys
from scipy.integrate import solve_ivp
sys.path.insert(0, "/home/claude/aegis/theory/inflation"); import cliff_v2 as C
lnVp, _ = C.version("exp", 4 / math.pi); c = C.c
def run(b):
    L = lambda x: 1 + b / (1 + math.log(1 + 1 / x))
    lnV = lambda p: lnVp(p) - math.log(L(math.exp(c * p)))
    dl = lambda p, h=1e-6: (lnV(p + h) - lnV(p - h)) / (2 * h)
    V = lambda p: math.exp(lnV(p)) if lnV(p) > -700 else 0.0
    def rhs(t, z):
        p, dp = z; K = 0.5 * dp * dp; return [dp, -(3 - K) * dp - dl(p) * (3 - K)]
    end = lambda t, z: 0.5 * z[1] ** 2 - 1; end.terminal = True; end.direction = 1
    s = solve_ivp(rhs, [0, 4000], [-13.0, 0], events=end, rtol=1e-9, atol=1e-12, method="LSODA")
    p, dp = s.y_events[0][0]; H2e = V(p) / (3 - 0.5 * dp * dp); f = 0.008
    lnr = math.log(f * 0.5 * H2e * dp * dp); dp *= math.sqrt(1 - f)
    def rhs2(t, z):
        p, dp, lnr = z; rr = math.exp(lnr); K = 0.5 * dp * dp; Vp = V(p); H2 = (Vp + rr) / (3 - K); e = K + (2 / 3) * rr / H2
        return [dp, -(3 - e) * dp - Vp * dl(p) / H2, -4.0]
    out = {}
    for x0 in (0.02, 0.05, 0.1):
        ev = lambda t, z, x0=x0: z[0] - math.log(x0) / c; ev.terminal = True; ev.direction = 1
        s2 = solve_ivp(rhs2, [0, 5], [p, dp, lnr], events=ev, rtol=1e-9, atol=1e-12, method="LSODA")
        if len(s2.t_events[0]):
            pp, dd, ll = s2.y_events[0][0]; Vp = V(pp); H2 = (Vp + math.exp(ll)) / (3 - 0.5 * dd * dd)
            out[x0] = abs(dd) * math.sqrt(H2) / math.sqrt(H2e)      # phi_dot in units of H at the end of inflation (b's own)
        else: out[x0] = float("nan")
    return out, math.sqrt(H2e)
base, He0 = run(0.0)
for b in (3.0, 10.0):
    o, He = run(b)
    print(f"b {b}: H_end/H_end(b=0) {He/He0:.3f}; " + ", ".join(f"x0 {k}: phi_dot ratio {o[k]*He/(base[k]*He0):.3f} -> heat share x{(o[k]*He/(base[k]*He0))**1.5:.2f}" for k in o))
# normalise each b to the observed amplitude A_s: physical V at the CMB point = (3 pi^2/2) r A_s, so the internal potential is scaled by
# c_b = V_phys(x*) / V_int(x*); heat share f ~ (g phi_dot)^{3/2} m_chi / (3 H^2 M_P^2) scales as c^{-1/4} at fixed internal shape.
import twistl_scan as TS
def scale(b):
    N, ns, r, xs = TS.obs(b)
    L = lambda x: 1 + b / (1 + math.log(1 + 1 / x)); Vint = math.exp(lnVp(math.log(xs) / c)) / L(xs)
    return r / Vint
c0 = scale(0.0)
for b in (3.0, 10.0):
    o, He = run(b); cb = scale(b)
    fr = {k: ((o[k] * He) ** 1.5 / He ** 2) / ((base[k] * He0) ** 1.5 / He0 ** 2) * (cb / c0) ** -0.25 for k in o}
    print(f"b {b} (A_s-normalised): heat share relative to the Twist " + ", ".join(f"x0 {k}: x{v:.2f}" for k, v in fr.items()))
