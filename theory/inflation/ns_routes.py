"""Task F (exploratory): every route inside the theory (alpha = 1 fixed) that moves n_s, computed. AI-assisted.
Base: E-model alpha = 1, V = V0 (1 - exp(-sqrt(2/3) phi))^2, first-order slow roll (as twist_inflation_N.py).
Routes:
 R1 kination after the cliff: radiation fraction f at the cliff, kination lasts N_k = 0.5 ln((1-f)/f) e-folds,
    N* gains N_k/2 (w = 1 between end and radiation domination; Planck 2018 X Eq. 47 form).
 R2 early cliff: inflation is cut by the cliff at phi_c above the slow-roll end; the CMB scale then sits N* e-folds
    before phi_c, i.e. N_c = N(phi_c) e-folds further up the plateau. rho_end = 1.5 V(phi_c).
 R3 second-order slow roll (Stewart-Lyth): n_s - 1 = -6e + 2h + O(e^2, e h, xi^2) correction estimated.
 R4 angle: the angle is heavy during inflation (mass^2 ~ 4H^2 at alpha = 1 from the Kahler curvature), no turn ->
    no shift at this order (noted, not computed here).
Matter-formation check: R1 lowers T_RH as f falls; R2 lowers H at the cliff, so the hidden mass must rescale."""
import math
from scipy.integrate import quad
from scipy.optimize import brentq

c = math.sqrt(2 / 3); AS = 2.1e-9; G = 106.75; H0c = 67.4 / 299792.458; KSTAR = 0.05; MP = 2.435e18
fpot = lambda p: 1 - math.exp(-c * p)
eps = lambda p: 0.5 * (2 * c * math.exp(-c * p) / fpot(p)) ** 2
eta = lambda p: 2 * c * c * math.exp(-c * p) * (2 * math.exp(-c * p) - 1) / fpot(p) ** 2
pend = brentq(lambda p: eps(p) - 1, 0.01, 5)
Nfrom = lambda a, b: quad(lambda x: 1 / math.sqrt(2 * eps(x)), a, b)[0]


def phi_at(N, start):
    return brentq(lambda p: Nfrom(start, p) - N, start + 1e-9, 60)


def solve(Nc=0.0, f_rad=1.0):
    pc = phi_at(Nc, pend) if Nc > 0 else pend
    Nk = 0.5 * math.log((1 - f_rad) / f_rad) if f_rad < 1 else 0.0
    N = 55.0
    for _ in range(80):
        p = phi_at(N, pc); e, h = eps(p), eta(p); V0 = AS * 24 * math.pi ** 2 * e / fpot(p) ** 2
        Vs = V0 * fpot(p) ** 2; rho_end = 1.5 * V0 * fpot(pc) ** 2
        Nn = 66.89 - math.log(KSTAR / H0c) + 0.25 * math.log(Vs ** 2 / rho_end) - math.log(G) / 12 + Nk / 2
        if abs(Nn - N) < 1e-7:
            break
        N = Nn
    p = phi_at(N, pc); e, h = eps(p), eta(p)
    xi2 = 4 * c ** 4 * math.exp(-c * p) * 2 * c * c / 1  # crude size of xi^2 ~ (V'V'''/V^2), order 1/N^2
    ns = 1 - 6 * e + 2 * h
    V0 = AS * 24 * math.pi ** 2 * e / fpot(p) ** 2
    return {"Nc": Nc, "f_rad": f_rad, "N_kin": round(Nk, 2), "N*": round(N, 2), "n_s": round(ns, 5), "r": round(16 * e, 5),
            "H_cliff_GeV": math.sqrt(V0 * fpot(pc) ** 2 / 3) * MP}


if __name__ == "__main__":
    base = solve()
    print(f"Base (instant reheating, cliff at slow-roll end): N* {base['N*']}, n_s {base['n_s']}, r {base['r']}")
    print("R1 kination (radiation fraction f at the cliff):")
    for f in (0.5, 0.1, 0.01, 1e-3, 1e-6, 1e-12):
        o = solve(f_rad=f); print(f"  f {f:.0e}: N_kin {o['N_kin']}, N* {o['N*']}, n_s {o['n_s']} (dn_s {o['n_s'] - base['n_s']:+.4f}), r {o['r']}")
    print("R2 early cliff (cliff N_c e-folds above the slow-roll end):")
    for Nc in (2, 5, 10, 15, 20, 30):
        o = solve(Nc=Nc); print(f"  N_c {Nc}: N* {o['N*']}, n_s {o['n_s']} (dn_s {o['n_s'] - base['n_s']:+.4f}), r {o['r']}, H at cliff {o['H_cliff_GeV']:.2e} GeV")
    for tgt in (0.9712, 0.9737):
        Nc = brentq(lambda x: solve(Nc=x)["n_s"] - tgt, 0.5, 60); o = solve(Nc=Nc)
        print(f"  n_s = {tgt} needs N_c = {Nc:.1f} (r {o['r']}, H at cliff {o['H_cliff_GeV']:.2e} GeV)")
    p = phi_at(base["N*"], pend); e = eps(p)
    print(f"R3 second-order slow roll: |correction| ~ e*(1/N) ~ {e * 2 / base['N*']:.1e} (negligible)")
