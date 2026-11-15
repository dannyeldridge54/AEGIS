"""D428 (locked PREREG_D428_PART7B): second pass Part 7 — bridge B4 for the BASELINE birefringence axion (separate light axion, D414).
Field θ (Ω_a ≪ 1, no backreaction) in flat ΛCDM (Ω_m 0.31, Ω_r 9.1e-5): θ'' + (3 + dlnH/dN) θ' + (m/H)² sin θ = 0, N = ln a, start frozen at
θ_i = 1 at a = 1e-6. Rotation of light emitted at z: Δθ(z) = θ(0) − θ(z). Output ρ_β = |Δθ(z_re)|/|Δθ(1089)| for z_re ∈ {7, 10}. AI-assisted."""
import math
from scipy.integrate import solve_ivp
Om, Or = 0.31, 9.1e-5; OL = 1 - Om - Or
H2 = lambda a: Om / a**3 + Or / a**4 + OL
dlnH = lambda a: -0.5 * (3 * Om / a**3 + 4 * Or / a**4) / H2(a)
def run(mr):
    rhs = lambda N, y: [y[1], -(3 + dlnH(math.exp(N))) * y[1] - mr**2 / H2(math.exp(N)) * math.sin(y[0])]
    s = solve_ivp(rhs, [math.log(1e-6), 0.0], [1.0, 0.0], rtol=1e-10, atol=1e-12, dense_output=True, method="DOP853", max_step=0.01)
    th = lambda z: s.sol(-math.log(1 + z))[0]
    d = lambda z: th(0) - th(z)
    return d(1089), d(10), d(7)
print(" m/H0   Δθ_rec     Δθ(z=10)   Δθ(z=7)    ρ_β(10)   ρ_β(7)")
for mr in (2, 5, 10, 20, 50, 100, 300):
    r, a10, a7 = run(mr)
    print(f"{mr:5d}  {r:+.4f}   {a10:+.4f}   {a7:+.4f}   {abs(a10/r):.3f}    {abs(a7/r):.3f}", flush=True)
