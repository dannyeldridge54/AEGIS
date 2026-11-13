"""Development 64 (exploratory): can the base theory give the small dark-matter coupling beta ~ 0.03? AI-assisted.
Code convention (AxiCLASS coupled build): rho_cdm a^3 ~ m_DM(phi) ~ exp(beta phi), phi canonical (reduced Planck).
With x = exp(sqrt(2/3) phi): m ~ x^q, q = beta / sqrt(2/3).
No-scale supergravity, K = -3 ln(T+Tbar) + |Q|^2 / (T+Tbar)^n (modular weight n), W ⊃ M Q Q:
physical mass m = e^{K/2} M / K_QQbar ~ (2x)^{-3/2} (2x)^{n} -> q = n - 3/2."""
import math
c = math.sqrt(2 / 3)
print("fitted beta 0.030-0.034  ->  q =", round(0.030 / c, 4), "-", round(0.034 / c, 4), "  (needs modular weight n = 1.537-1.542)")
for n in (0, 0.5, 1, 1.5, 2, 3):
    q = n - 1.5; print(f"modular weight n = {n}: q = {q:+.2f}, beta = {q * c:+.3f}")
print("data: beta > ~0.1 not computable (CLASS fails) and disfavoured; fits give 0.030-0.034")
