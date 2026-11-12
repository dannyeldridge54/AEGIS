"""Development 7: does the Twist's curved field space pump the angle to the speed matter formation needs?
Angle (beta, coordinate) + dilaton (sigma, canonical) with the hyperbolic kinetic term
  L = 1/2 sigma'^2 + 1/2 F^2 e^{lam sigma / M_P} beta'^2,   lam = -2 sqrt(2/3)  (fixed by the theory),
in a radiation background (potentials negligible this early: both are set at the dark-energy scale).
Equations (cosmic time):  sigma'' + 3H sigma' - (lam/2M_P) F^2 e^{lam sigma/M_P} beta'^2 = 0
                          d/dt (a^3 e^{lam sigma/M_P} beta') = 0   (the angle's momentum is conserved)
The spin coupling acts on beta' (Mercuri: -(3/4) d beta J_A), normalised so that at sigma = 0 the speed that matters is
phidot = F beta' with c_A = sqrt(3/8); the requirement is r = F beta' / (H M_P) ~ 1.3e-3 at T_F = 2.1e13 GeV.
AI-assisted; hypothesis-stage numerics."""
import math
import numpy as np
from scipy.integrate import solve_ivp
MP = 2.435e18; lam = -2 * math.sqrt(2 / 3); gs = 106.75; MPL = 1.221e19
H_of_T = lambda T: 1.66 * math.sqrt(gs) * T * T / MPL
TRH, TF, need = 1e15, 2.1e13, 1.3e-3
# variables in units of M_P and H(T_RH); time variable N = ln a ; radiation: H = H_RH e^{-2N}
def rhs(N, y):
    s, ds, chi_dot = y                           # sigma/M_P, d sigma/dN, F beta' /(H M_P) at sigma=0 normalisation
    # with H dot/H = -2 per efold: sigma'' in N: s'' + (3 - 2) s' - (lam/2) e^{lam s} q^2 = 0, q = F beta' /(H M_P)
    # angle: d/dN(a^3 e^{lam s} q H) = 0  ->  q' = -q (3 - 2) - lam s' q = -q - lam ds q
    q = chi_dot
    dds = -ds + 0.5 * lam * math.exp(lam * s) * q * q
    dq = -q - lam * ds * q
    return [ds, dds, dq]
NF = math.log(TRH / TF)                          # efolds from T_RH to T_F (a ~ 1/T)
print(f"efolds from 1e15 to 2.1e13 GeV: {NF:.2f}; needed r at T_F = {need:.1e}")
for rs0, q0 in ((0.0, 0.06), (0.5, 0.06), (1.0, 0.012), (1.0, 0.03), (-1.0, 0.06), (2.0, 0.006)):
    sol = solve_ivp(rhs, [0, NF], [0.0, rs0, q0], rtol=1e-10, atol=1e-14)
    s, ds, q = sol.y[:, -1]
    r = q * math.exp(lam * s / 2) * 0 + q            # q is defined at sigma=0 normalisation of F beta'
    print(f"start: dilaton speed {rs0:+.1f}, angle speed {q0:.3f} -> at T_F: angle r = {q:.2e} "
          f"({'enough' if q >= need else 'short'}), dilaton moved {s:+.2f} M_P")
