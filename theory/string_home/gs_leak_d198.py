"""D198: does the Green-Schwarz dilaton-modulus mixing re-open the fifth force in the heterotic home? AI-assisted estimate.
Duality covariance makes each racetrack term carry eta(T) factors: A(T) = A0 eta^{-(6+2a kappa)}, B(T) = B0 eta^{-(6+2b kappa)}, W0 ~ eta^{-6}
(weight -3 each; e^{-aY} has weight a kappa, kappa ~ delta_GS/8pi^2). The two KL conditions are then consistent and give
Re Y0(T) = c - 2 kappa ln|eta|, so the duality-INVARIANT string coupling 1/g_s^2 = Re Y + (kappa/2) ln(u_het) becomes
c + (kappa/2) G(T), G = ln(u_het |eta|^4) ~ ln u_het - (pi/3) u_het/2 at large T: the physical gauge couplings move with T."""
import math
def dG(T1, T2):                      # G at large T_het (Re part), u_het = 2 T_het, ln|eta|^4 ~ -pi T_het/3
    G = lambda T: math.log(2 * T) - math.pi * T / 3
    return G(T2) - G(T1)
inv_g2 = 2.0
for label, T_today, dT in (("TWIST-M9 (T_het = x/72)", 89 / 72, 0.3), ("degree-1 (T_het = x/8)", 89 / 8, 2.5)):
    d = dG(T_today - dT, T_today)
    for delta in (1, 10, 30, 90):
        kappa = delta / (8 * math.pi ** 2)
        da = (kappa / 2) * abs(d) / inv_g2
        print(f"{label}: Delta T_het {dT} since z~1, delta_GS {delta:3}: |Delta alpha/alpha| ~ {da:.1e} (quasar bound ~1e-6)")
print("delta_GS needed for 1e-6 (M9):", 1e-6 * inv_g2 * 2 * 8 * math.pi ** 2 / abs(dG(89 / 72 - 0.3, 89 / 72)))
