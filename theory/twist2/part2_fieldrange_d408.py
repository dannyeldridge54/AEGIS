"""D408 (locked PREREG_D408_PART2): Part 2 (inflation plateau) — field excursions and swampland/TCC numbers for the Twist. AI-assisted."""
import math, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.join(ROOT, "theory", "inflation")); sys.argv = sys.argv[:1]
import cliff_v2 as C
lnV, Fc = C.version("exp", 4 / math.pi); I = C.inflation(lnV); c = math.sqrt(2 / 3)
ps, pe = I["pstar"], I["pend"]; pf = math.log(29.81) / c
print(f"p* {ps:.3f}  p_end {pe:.3f}  p_final(x=29.81) {pf:.3f}  [canonical, M_P]")
print(f"Δφ CMB exit → end of inflation: {pe-ps:.3f} M_P;  end → capture: {pf-pe:.3f} M_P;  total: {pf-ps:.3f} M_P")
eps_star = 0.5 * C.DL(ps) ** 2; print(f"ε* = {eps_star:.3e},  |V'|/V at N* = {abs(C.DL(ps)):.3e}  (dS-conjecture s1 ~ O(1))")
As = 2.1e-9; V = 24 * math.pi**2 * As * eps_star; print(f"V*^(1/4) = {V**0.25*2.435e18:.2e} GeV,  H* = {math.sqrt(V/3)*2.435e18:.2e} GeV")
print(f"TCC (Bedroya–Brandenberger–Loverde–Vafa): V^(1/4) ≲ 6e8 GeV, r ≲ 1e-30 → Twist exceeds by V^(1/4) ×{V**0.25*2.435e18/6e8:.1e}")
for lam in (1/math.sqrt(6), math.sqrt(2/3), 1.0):
    print(f"distance conjecture: tower mass drop e^(-λΔφ) over total range, λ = {lam:.3f}: {math.exp(-lam*(pf-ps)):.2e}")
