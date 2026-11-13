"""D152: a candidate string home for OUR rung-3 Twist that keeps matter neutral: heterotic string on the Z3 orbifold. AI-assisted.
Ingredients (standard results; numbers here are the checks that follow from them):
 - Overall untwisted modulus T with K = -3 ln(T + Tbar): rung 3alpha = 3, exactly the Twist's.
 - Heterotic: M_s^2 / M_P^2 ~ 1/Re S (the 4-d dilaton), NOT the volume -> moving T at fixed S leaves the string scale fixed.
 - Gauge couplings: f = S at tree level; T-dependent threshold corrections come only from N=2 sectors (Dixon-Kaplunovsky-Louis),
   and the Z3 orbifold has none -> no T in the SM gauge couplings at one loop (the modular anomaly is cancelled by the universal
   Green-Schwarz term, absorbed in the dilaton).
 - Untwisted matter has modular weight 1 per field: physical Yukawa ~ e^{K/2} / sqrt(Z_1 Z_2 Z_3) with Z = (T+Tbar)^-1 -> x^0.
 - Twisted-sector Yukawas come from worldsheet instantons ~ e^{-2 pi T/3} (instanton-type breaking, D140 part (a))."""
import math
c = math.sqrt(2 / 3); x = 88.9
print("untwisted physical Yukawa exponent: K/2 gives (2x)^(-3/2); 1/sqrt(Z1 Z2 Z3) gives (2x)^(+3/2) -> total x^0 -> beta 0")
print("string scale vs Planck: depends on S only -> beta 0 from Lambda_QCD at fixed S")
for a, lab in ((2 * math.pi / 3, "twisted Yukawa e^(-2 pi T/3)"), (math.pi / 4, "cliff instanton e^(-pi T/4)")):
    b = a * x * math.exp(-a * x) * c
    print(f"{lab}: beta {b:.1e} (MICROSCOPE 1.2e-6) PASS by 10^{math.log10(1.2e-6/b):.0f}")
print("weights check (D96 used modular weights for MSSM-in-SUGRA): untwisted n=1 x3 is the case where Yukawas are T-independent;")
print("the QCD scale is T-independent here because the threshold Delta(T) = 0 on Z3, not because of a weight choice.")
