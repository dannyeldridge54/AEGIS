"""T1: the field-space pump with a self-consistent background (radiation + dilaton + angle kinetic energy).
Variables in N = ln a: s = sigma/M_P, s' = d s/dN, q = F beta'/(H M_P) (sigma = 0 normalisation, the speed the spin
coupling sees). Kinetic share Omega_k = (s'^2 + e^{lam s} q^2)/6, eps = -dlnH/dN = 2 + Omega_k (radiation 2, kination 3).
  s'' + (3 - eps) s' - (lam/2) e^{lam s} q^2 = 0 ;   q'/q = eps - 3 - lam s'.
Temperature T ~ 1/a (g* constant). AI-assisted."""
import math
import numpy as np
from scipy.integrate import solve_ivp
lam = -2 * math.sqrt(2 / 3); TRH, TF, TBBN, need = 1e15, 2.1e13, 1e-3, 1.3e-3
def rhs(N, y):
    s, ds, lq = y; q = math.exp(lq)
    Ok = (ds * ds + math.exp(lam * s) * q * q) / 6
    eps = 2 + Ok
    return [ds, -(3 - eps) * ds + 0.5 * lam * math.exp(lam * s) * q * q, eps - 3 - lam * ds]
NF, NB = math.log(TRH / TF), math.log(TRH / TBBN)
print(f"{'dilaton0':>8} {'angle0':>7} {'peak share':>10} {'angle r at T_F':>14} {'enough':>6} {'share at 1 MeV':>14} {'dilaton travel':>14}")
for ds0, q0 in ((0.5, 0.06), (1.0, 0.012), (1.0, 0.03), (1.5, 0.012), (2.0, 0.006), (2.2, 0.006)):
    if (ds0 ** 2 + q0 ** 2) / 6 >= 1:
        print(ds0, q0, "start exceeds total energy"); continue
    sol = solve_ivp(rhs, [0, NB], [0.0, ds0, math.log(q0)], rtol=1e-9, atol=1e-12, dense_output=True)
    Ns = np.linspace(0, NB, 4000); Y = sol.sol(Ns)
    Ok = (Y[1] ** 2 + np.exp(lam * Y[0]) * np.exp(Y[2]) ** 2) / 6
    yF = sol.sol(NF); rF = math.exp(yF[2])
    print(f"{ds0:8.1f} {q0:7.3f} {Ok.max():10.2f} {rF:14.2e} {'yes' if rF >= need else 'no':>6} {Ok[-1]:14.1e} {sol.sol(NB)[0]:+14.2f}")
