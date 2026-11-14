"""D400 (locked PREREG_D400_DESI_ALPHA): one-loop α drift for a DESI-fitting quintessence modulus with K ⊃ −k ln(X + X̄). AI-assisted.
Coefficient (kl_coeff.py, locality weights Z ∝ e^{K/3}): 16π² d(1/g_a²)/d ln x = −(k/3) b_a (MSSM b = 33/5, 1, −3);
d ln α_em/d ln x = (k/3) × 6.97e-3; canonical field: d ln x/dφ = √(2/k) (M_P = 1) → ζ ≡ d ln α_em/dφ.
Field speed from w(z) (CPL), canonical so w clipped at −1: (dφ/dN)² = 3 Ω_DE(z) (1 + w(z)).
Outputs: Δα/α at z = 1.15 (ESPRESSO), α̇/α today [1/yr] (clocks), η ≈ 10⁻³ ζ² (MICROSCOPE, Martins et al. 2204.02930)."""
import math
from scipy.integrate import quad
Om, H0yr = 0.31, 67.4 / 977.8 / 1e9            # H0 in 1/yr (977.8 Gyr per (km/s/Mpc)^-1)
base = 6.968458e-3                               # d ln α_em / d ln x at k = 3 (kl_coeff.py)
fits = {"PantheonPlus": (-0.833, -0.65), "DESY5": (-0.749, -0.88), "Union3": (-0.664, -1.10)}   # arXiv:2511.22512 CPL
def w(z, w0, wa): return max(w0 + wa * z / (1 + z), -1.0)
def ODE(z, w0, wa):
    rde = (1 - Om) * math.exp(3 * quad(lambda zz: (1 + w(zz, w0, wa)) / (1 + zz), 0, z)[0])
    return rde / (rde + Om * (1 + z) ** 3)
def dphi(z1, w0, wa):   # ∫ |dφ/dN| dN from z1 to 0, dN = dz/(1+z)
    return quad(lambda z: math.sqrt(3 * ODE(z, w0, wa) * (1 + w(z, w0, wa))) / (1 + z), 0, z1)[0]
if __name__ == "__main__":
    print("bounds: ESPRESSO Δα/α(1.15) = (1.3 ± 1.4)e-6; clocks α̇/α = (1.8 ± 2.5)e-19 /yr; MICROSCOPE η = (−0.1 ± 1.3)e-14")
    print("fit           k   ζ=dlnα/dφ   Δφ(z<1.15)  Δα/α(1.15)  [σ]      α̇/α [1/yr]  [σ]        η          [σ]")
    for name, (w0, wa) in fits.items():
        for k in (1, 2, 3):
            zeta = (k / 3) * base * math.sqrt(2 / k)
            D = dphi(1.15, w0, wa); da = zeta * D
            phidot = math.sqrt(3 * (1 - Om) * (1 + w0)) * H0yr; adot = zeta * phidot
            eta = 1e-3 * zeta ** 2
            print(f"{name:12s} {k}   {zeta:.3e}   {D:.3f}       {da:.2e}  {da/1.4e-6:6.0f}   {adot:.2e}  {adot/2.5e-19:9.2e}  {eta:.2e}  {eta/1.3e-14:9.2e}")
