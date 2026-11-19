# AEGIS string-calc stage S5 (2026-11-18, Danny "Start make toolkit"): genus-one modular integrals over the fundamental domain F
# with the Narain lattice Γ_{2,2}(T,U) — the machinery behind DKL thresholds, the universal Y (P3, D1365–D1398) and the
# genus-one D⁴R⁴ product E₂(T)E₂(U) (GRV 1001.2535 eq. 4.16). Validation-first: each function reproduces a closed form.
import math
import numpy as np


def gamma22(tau, T, U, N=5):
    """Lagrangian Γ_{2,2}(T,U) = (T₂/τ₂) Σ_A exp(−2πi T det A − πT₂/(τ₂U₂)|n₁τ + m₁ + U(n₂τ + m₂)|²), A = [[n₁,m₁],[n₂,m₂]].
    Modular invariant in τ; → 1 as τ₂ → ∞. Truncated at |entries| ≤ N (fine on F, τ₂ ≥ √3/2)."""
    r = np.arange(-N, N + 1)
    n1, m1, n2, m2 = [a.ravel().astype(float) for a in np.meshgrid(r, r, r, r, indexing='ij')]
    detA = n1*m2 - m1*n2; z = n1*tau + m1 + U*(n2*tau + m2)
    return float((T.imag/tau.imag)*np.sum(np.exp(-2j*math.pi*T*detA - math.pi*T.imag/(tau.imag*U.imag)*np.abs(z)**2)).real)


def integrate_F(f, L=6.0, n1q=48, n2q=160):
    """∫_F d²τ f(τ) over |τ₁| ≤ ½, |τ| ≥ 1, τ₂ ≤ L (Gauss–Legendre in both directions)."""
    x, wx = np.polynomial.legendre.leggauss(n1q); y, wy = np.polynomial.legendre.leggauss(n2q); tot = 0.0
    for xi, wi in zip(x, wx):
        t1 = 0.5*xi; y0 = math.sqrt(1 - t1*t1); ys = y0 + (L - y0)*(y + 1)/2; wys = wy*(L - y0)/2
        tot += 0.5*wi*sum(wj*f(complex(t1, yj)) for yj, wj in zip(ys, wys))
    return tot


def dkl(T, U, **kw):
    """Δ(T,U) = ∫_F (d²τ/τ₂)(Γ_{2,2} − 1), numerically."""
    return integrate_F(lambda t: (gamma22(t, T, U) - 1)/t.imag, **kw)


def dkl_closed(T, U):
    """Dixon–Kaplunovsky–Louis closed form: −log(T₂U₂|η(T)η(U)|⁴) − log(8π e^{1−γ_E}/(3√3))."""
    from .shapes import log_eta
    return (-math.log(T.imag*U.imag) - 4*(log_eta(T).real + log_eta(U).real)
            - math.log(8*math.pi*math.exp(1 - 0.5772156649015329)/(3*math.sqrt(3))))
