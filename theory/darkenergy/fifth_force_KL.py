"""Development 90: does the QCD scale (so the proton mass) depend on Re T? Kaplunovsky-Louis answer. AI-assisted.
Physical gauge coupling (Kaplunovsky & Louis 1994): 1/g^2 = Re f + (b/16pi^2) ln(M_P^2/mu^2) + (c/16pi^2) K
  - sum_r T(r)/(8 pi^2) ln det Z_r,   c = sum_r T(r) - T(G).
QCD in the MSSM: T(G) = 3, sum_r T(r) = 6 (12 chiral triplets x 1/2), b = 3. K = -3 ln(2x); matter metric Z = (2x)^(-n)
(modular weight n: n = 1 is the sequestered / D3 form). f_QCD independent of T.
Lambda_QCD = M_P exp(-8 pi^2 / (b g^2)) -> d ln Lambda / d ln(2x) = -(8 pi^2/b) * d(1/g^2)/d ln(2x)."""
import math
TG, TR, b = 3, 6, 3; c = TR - TG; kap = math.sqrt(2 / 3)
def dlnL(n):
    d_invg2 = (c * (-3) + 2 * TR * n) / (16 * math.pi ** 2)       # d(1/g^2)/d ln(2x): K term + Z term
    return -(8 * math.pi ** 2 / b) * d_invg2
for n in (0, 0.5, 0.75, 1.0, 1.5):
    p = dlnL(n); yuk = -1.5 + 1.5 * n                                 # Y_phys ~ e^{K/2} / sqrt(Z^3) ~ (2x)^(-3/2 + 3n/2)
    beta_p = abs(p) * kap; beta_q = 0.05 * abs(yuk) * kap             # proton ~ Lambda; ~5% of nucleon mass from quark masses
    print(f"weight n {n}: Lambda_QCD ~ x^{p:+.3f}, Yukawa ~ x^{yuk:+.3f}; beta from Lambda {beta_p:.3f}, from quark masses ~{beta_q:.3f}"
          f" (Cassini 3.4e-3)")
