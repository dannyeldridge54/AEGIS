"""Consistency pass, model v5 (13 Nov afternoon): everything recomputed with the final form in one run.
K = -3 ln(T + Tbar - S Sbar (1 + (T+Tbar)/2mu) + zeta (S Sbar)^2), W = sqrt3 m S T exp(-n(1 - e^{-pi T/4})), mu = 1, n = 125, zeta = 3e4,
heat share 0.8%. AI-assisted."""
import math, mpmath as mp
import cliff_v2 as C
import kahler_sqrt_d127 as Q        # angle mass, old vs new V
import s_mass_d127 as SM            # S mass, full two-field potential
lnV, _ = C.version("exp", 4 / math.pi)
x = mp.mpf("0.37")
print("V_new == V_old for real T:", all(mp.almosteq(Q.V_old(mp.mpf(v), 0), Q.V_new(mp.mpf(v), 0)) for v in ("1e-4", "0.01", "1", "89")))
inf = C.inflation(lnV)
print(f"inflation (instant-reheating N*): N* {inf['N']:.1f}, n_s {inf['ns']:.4f}, r {inf['r']:.4f}; with kination dN ~ +1.9 (D84) n_s ~0.965")
pf = C.freeze(lnV, 0.008); w0, wa, p0 = C.thaw(lnV, pf)
print(f"tail at 0.8% heat: frozen x {math.exp(C.c*pf):.1f}, today x {math.exp(C.c*p0):.1f}, w0 {w0:.4f}, wa {wa:.4f}")
xs = math.exp(C.c * inf["pstar"]); xt = math.exp(C.c * p0)
for lab, xv in (("CMB point", xs), ("today", xt)):
    X = mp.mpf(xv); d2 = mp.diff(lambda y: Q.V_new(X, y), 0, 2)
    my = float(d2 / (3 / (4 * X * X)) / (Q.V_new(X, 0) / 3))
    K, W = SM.setup(True); s = mp.mpf("1e-6")
    v0, kss = SM.V(K, W, X, mp.mpf(0)); vp, _ = SM.V(K, W, X, s); vm, _ = SM.V(K, W, X, -s)
    ms = float((vp - 2 * v0 + vm) / (s * s) / (2 * kss) / (v0 / 3))
    print(f"{lab} (x {xv:.3g}): m_y^2/H^2 {my:+.3f}, m_S^2/H^2 {ms:.4g}  (both must be > 0; S >> 1)")
