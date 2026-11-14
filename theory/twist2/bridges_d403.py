"""D403 (locked PREREG_D403_BRIDGES): Wheatstone-style null combinations for the Twist / Twist-2. AI-assisted.
B1 = r − 3(1−n_s)²   and   B2 = α_s + ½(1−n_s)²   (α = 1 plateau; reheating/N* cancels at leading order)
Bridge 2: R = (α̇/α)/[H0 √(3 Ω_DE (1+w0))] = ζ(k) for a rolling modulus with K ⊃ −k ln(X+X̄)
B3 = β² − c_γ² K1 (1+w0)   (single thawing axion: dark energy + birefringence; K1 computed here)"""
import math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "theory", "inflation")); sys.path.insert(0, HERE); sys.argv = sys.argv[:1]
from scipy.integrate import quad
from scipy.optimize import brentq
import cliff_v2 as C
lnV, Fc = C.version("exp", 4 / math.pi); I = C.inflation(lnV)
eps = lambda p: 0.5 * C.DL(p) ** 2
eta = lambda p: (C.DL(p + 1e-5) - C.DL(p - 1e-5)) / 2e-5 + C.DL(p) ** 2
Nof = lambda p: quad(lambda q: -1 / C.DL(q), p, I["pend"], limit=200)[0]
def obs(N):
    p = brentq(lambda q: Nof(q) - N, -25, I["pend"] - 1e-6); return 1 - 6 * eps(p) + 2 * eta(p), 16 * eps(p)
print("Part A: Twist inflation bridges (α_s = −dn_s/dN, central difference ΔN = 0.5)")
print("  N*     n_s       r          α_s         B1=r−3(1−n_s)²   B2=α_s+½(1−n_s)²")
for N in (55.0, 56.0, 57.0, 57.2, 58.0, 60.0):
    ns, r = obs(N); a = -(obs(N + 0.25)[0] - obs(N - 0.25)[0]) / 0.5
    print(f"  {N:5.1f}  {ns:.5f}  {r:.6f}  {a:+.3e}   {r - 3*(1-ns)**2:+.3e}        {a + 0.5*(1-ns)**2:+.3e}", flush=True)
print("Part B: single thawing axion, K1 = β(c_γ=1)² / (1+w0)  [deg²], β(c_γ=1) = 0.42°/(2π) |Δθ|")
import axion_thaw_d393 as AX
for f in (0.5, 1.0, 2.0):
    for th in (0.3, 0.5, 1.0, 1.5):
        try:
            L4 = brentq(lambda L: AX.run(f, th, L), 1e-3, 50.0, xtol=1e-12)
        except ValueError:
            print(f"  f {f:3.1f} θ_i {th:3.1f}: no flat solution"); continue
        w0, wa, ODE, dth, w1 = AX.run(f, th, L4, True); b1 = 0.42 / (2 * math.pi) * abs(dth)
        print(f"  f {f:3.1f} θ_i {th:3.1f}: w0 {w0:+.4f}  1+w0 {1+w0:.4f}  β(c=1) {b1:.5f}°  K1 {b1*b1/(1+w0):.3e} deg²", flush=True)
print("Part C: bridge-2 constants ζ(k) = 6.968e-3 (k/3) √(2/k)")
for k in (1, 2, 3): print(f"  k {k}: ζ = {6.968458e-3*(k/3)*math.sqrt(2/k):.3e}")
