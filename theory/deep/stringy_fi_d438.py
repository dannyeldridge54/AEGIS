"""D438 (locked PREREG_D438_STRINGY_FI): deep step 3 — bounded (Π-stability) FI term at small volume. AI-assisted.
Toy: magnetised D7 on T²×T² with 2-cycle volumes x (rolling, the Twist) and x₂ (fixed); brane with fluxes (n₁, n₂) vs constituent (m₁, m₂).
Central charge Z ∝ −(n₁ − i x)(n₂ − i x₂) (large-volume form, B = 0). FI of the relative U(1): ζ = φ_a − φ_b, grade φ = arg Z / π:
ζ(x) = (1/π)[atan(x/m₁) − atan(x/n₁)] + c, c = constant from the x₂ factor. For x ≫ √(m₁n₁) this → (n₁ − m₁)/(π x) + c: the supergravity
1/x form (D436). |ζ| is bounded by construction at small x (→ c). Parameters: m₁ = 10, n₁ = 400 (peak of the x-term at √(m₁n₁) ≈ 63);
c fixed so the first root (where the rolling field from small x first meets ζ = 0) is x_E = 29.6. Compare |ζ| (in M_s² units) with the
supergravity extrapolation of D436 (ξ ≈ −76 M_P² at the CMB point)."""
import math
from scipy.optimize import brentq
m1, n1, xE = 10.0, 400.0, 29.6
f = lambda x: (math.atan(x / m1) - math.atan(x / n1)) / math.pi
c = -f(xE); z = lambda x: f(x) + c
x2root = brentq(z, math.sqrt(m1 * n1) + 1e-6, 1e6)
print(f"c = {c:+.4f};  roots: x_E1 = {brentq(z, 1e-6, math.sqrt(m1*n1)):.3f} (capture), x_E2 = {x2root:.1f}")
for x in (1.3e-4, 8.8e-3, 1.0, 3.1, 20.0, 29.0, 29.6, 30.0, 63.0, 1e3):
    print(f"x {x:9.4g}:  ζ = {z(x):+.4e} M_s²   (supergravity-like large-x term (n1−m1)/(πx) = {(n1-m1)/(math.pi*x):.3e})")
print(f"max |ζ| for x < x_E: {max(abs(z(10**(k/100))) for k in range(-500, int(100*math.log10(xE)))):.3f} M_s² → screening |φ|² ≤ that × M_s² (sub-Planckian if M_s ≲ M_P)")
