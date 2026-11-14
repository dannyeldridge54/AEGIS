"""D419 (locked PREREG_D419_ROUTE_A): Route A — a tiny holomorphic deformation of the Twist superpotential that keeps K = −3 ln(T + T̄).
F(T) = (T + ε) / √(1 + T/μ) · cliff(T)   [i.e. W ⊃ S·ε·cliff/√(1+T/μ) added to W ⊃ S·F; precedent: arXiv:2505.03608's ε₁ term]
V ∝ |F|²/(4x²) → lnV_ε = lnV_0 + 2 ln(1 + ε/x) (real T). On the plateau (x ~ 10⁻⁴) the term tilts V; after the cliff (x ≳ 0.01) it is negligible.
Outputs at fixed N* = 57.2 (D391: instant 55.7 + kination 1.5; recomputed instant N* reported): n_s, r, α_s = −dn_s/dN, B1, B2, ε needed for
n_s = 0.9736 (crown D410 THAW_FREE), and the cross-sector factors (1 + ε/x)² at the end of inflation and at x_E = 29.6 (Λ). AI-assisted."""
import math, sys, os
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.join(ROOT, "theory", "inflation")); sys.argv = sys.argv[:1]
import cliff_v2 as C
lnV0, Fc = C.version("exp", 4 / math.pi); DL0 = C.DL; c = C.c
NSTAR = 57.2
def model(eps_w):
    xof = lambda p: math.exp(c * p)
    lnV = lambda p: lnV0(p) + 2 * math.log(1 + eps_w / xof(p))
    DL = lambda p: DL0(p) - 2 * c * eps_w / (xof(p) + eps_w)
    e1 = lambda p: 0.5 * DL(p) ** 2
    eta = lambda p: (DL(p + 1e-5) - DL(p - 1e-5)) / 2e-5 + DL(p) ** 2
    lo = math.log(max(2 * abs(eps_w), 1e-12)) / c if eps_w < 0 else -25
    ps = np.linspace(max(lo, -25) + 1e-3, 2, 6000); ev = [e1(p) for p in ps]
    i = next(k for k in range(len(ps)) if ev[k] >= 1 and ps[k] > -8); pend = brentq(lambda p: e1(p) - 1, ps[i - 1], ps[i])
    Nof = lambda p: quad(lambda q: -1 / DL(q) if DL(q) < 0 else 1e9, p, pend, limit=400)[0]
    def at(N):
        p = brentq(lambda q: Nof(q) - N, max(lo, -25) + 1e-3, pend - 1e-6); return 1 - 6 * e1(p) + 2 * eta(p), 16 * e1(p), p
    ns, r, p = at(NSTAR); a = -(at(NSTAR + 0.25)[0] - at(NSTAR - 0.25)[0]) / 0.5
    return dict(ns=ns, r=r, a=a, B1=r - 3 * (1 - ns) ** 2, B2=a + 0.5 * (1 - ns) ** 2, xstar=math.exp(c * p), xend=math.exp(c * pend),
                fend=(1 + eps_w / math.exp(c * pend)) ** 2, fLam=(1 + eps_w / 29.6) ** 2)
if __name__ == "__main__":
    print(" ε            n_s       r          α_s         B1          B2         x*        x_end     (1+ε/x)²_end  (1+ε/x_E)²")
    for e in (0.0, 1e-6, 3e-6, 1e-5, 2e-5, 3e-5, -1e-6, -3e-6, -1e-5, -2e-5):
        try:
            m = model(e)
            print(f"{e:+.1e}   {m['ns']:.5f}  {m['r']:.6f}  {m['a']:+.3e}  {m['B1']:+.2e}  {m['B2']:+.2e}  {m['xstar']:.2e}  {m['xend']:.2e}  {m['fend']:.6f}      {m['fLam']:.9f}", flush=True)
        except Exception as ex:
            print(f"{e:+.1e}   failed: {type(ex).__name__}")
    try:
        f = lambda e: model(e)["ns"] - 0.9736
        es = [x for x in (0.0, 1e-6, 3e-6, 1e-5, 2e-5, 3e-5, -1e-6, -3e-6, -1e-5, -2e-5)]
        vals = []
        for e in es:
            try: vals.append((e, f(e)))
            except Exception: pass
        vals.sort(); root = None
        for (e1_, f1), (e2_, f2) in zip(vals, vals[1:]):
            if f1 * f2 < 0: root = brentq(f, e1_, e2_, xtol=1e-9); break
        if root is None: print("ε for n_s = 0.9736: not bracketed in the scan")
        else:
            m = model(root); print(f"ε for n_s = 0.9736: {root:+.3e} → r = {m['r']:.5f}, α_s = {m['a']:+.3e}, B1 = {m['B1']:+.2e}, B2 = {m['B2']:+.2e}, Λ factor {m['fLam']:.9f}")
    except Exception as ex:
        print("root search failed:", ex)
