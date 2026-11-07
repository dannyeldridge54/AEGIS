"""Running-F test (7 Nov 2026; AI-assisted, not pre-registered): can the GKY dilaton make ONE BI axion serve both roles?
    python dilaton_running_F.py   -> dilaton_running_F.json
The axion's canonical decay constant is F = F_P/|phi| with F_P = (4/pi) sqrt(3/2) = 1.559 (Nieh-Yan, |phi| = 1).
The early width the data want (stored edelockP_F6..F12 scan) is F ~ 0.12-0.17, i.e. |phi| ~ 9-13 at equality, while
the late value needs |phi| ~ 1 today. Here the dilaton evolves in the N = 1 supergravity potential of the GKY Kahler
potential with superpotential W = W0 exp(b Phi) (b = 0 is the simplest, constant W): for phi < -1,
V ~ A (-phi-1) exp(-(6-2b) phi)/phi^2. Matter is blind to the dilaton (Einstein frame). Units: M_Pl = 1, H0 = 1.
For each b, A is set so that |phi| = 1.5 today; the output is |phi| and the implied F at z = 3500."""
import json
import math

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

FP, OR, OM, OL = 4 / math.pi * math.sqrt(1.5), 9.0e-5, 0.3, 0.7
S = math.sqrt(2 / 3)


def v(chi, b):
    p = math.exp(S * chi)                                # |phi|
    return (p - 1) * math.exp((6 - 2 * b) * p) / p ** 2


def dv(chi, b):
    p = math.exp(S * chi)
    k = 6 - 2 * b
    f = (p - 1) * math.exp(k * p) / p ** 2
    dfdp = math.exp(k * p) / p ** 2 + (p - 1) * (k * math.exp(k * p) / p ** 2 - 2 * math.exp(k * p) / p ** 3)
    return dfdp * S * p


def run(lnA, b, chi0=None):
    A = math.exp(lnA)
    N0 = math.log(1e-9)
    if chi0 is None:
        chi0 = math.log(60.0) / S                        # start high; the tracker is an attractor

    def rhs(N, y):
        c, cp = y
        a = math.exp(N)
        rr, rm = 3 * OR / a ** 4, 3 * OM / a ** 3
        V = A * v(c, b)
        H2 = (rr + rm + 3 * OL + V) / (3 - cp * cp / 2)
        eps = cp * cp / 2 + (rm + 4 * rr / 3) / (2 * H2)
        return [cp, -(3 - eps) * cp - A * dv(c, b) / H2]

    stop = lambda N, y: math.exp(S * y[0]) - 1.2       # stop before the negative well (|phi| < 1)
    stop.terminal = True
    sol = solve_ivp(rhs, (N0, 0.0), [chi0, 0.0], method="LSODA", rtol=1e-8, atol=1e-10, dense_output=True, events=stop)
    ph = lambda z: math.exp(S * sol.sol(max(-math.log(1 + z), N0))[0]) if -math.log(1 + z) <= sol.t[-1] else float("nan")
    return sol, ph


def result(b):
    """Distance the dilaton moves between z = 3500 and today on the tracking branch (amplitude small enough that it
    tracks the background instead of overshooting and freezing). Needed: |phi| ~ 9-13 at z = 3500 down to ~1 today,
    i.e. a move of ~8-12."""
    moves = []
    for x in np.arange(-400.0, 1.0, 5.0):
        sol, ph = run(x, b)
        if sol.status != 0:
            continue
        a, z0 = ph(3500.0), ph(0.0)
        if ph(1e6) < 59.0 and z0 > 5.0:                  # moving and still on the large-|phi| tracker today
            moves.append(a - z0)
    if not moves:
        return {"b": b, "note": "no tracking solution found"}
    d = float(np.median(moves))
    return {"b": b, "exponent_6_minus_2b": 6 - 2 * b, "tracker_move_z3500_to_today": round(d, 2),
            "analytic_ln(rho_eq/rho_0)/exponent": round(math.log(3501 ** 3 * OM / (OM + OL)) / (6 - 2 * b), 2),
            "abs_phi_at_z3500_if_1_today": round(1 + d, 2), "F_early_implied": round(FP / (1 + d), 3),
            "in_data_window_0.12_to_0.17": 0.12 <= FP / (1 + d) <= 0.17}


def main():
    rows = [result(b) for b in (0.0, 1.0, 1.5, 1.7, 1.8, 1.9)]
    out = {"target": "F_early 0.12-0.17 (best 0.136-0.153, stored F-scan) <=> |phi| 9-13 at z = 3500",
           "rows": rows,
           "reading": ("b = 0 (constant W, the simplest supergravity potential) is the derived case; any b != 0 is a new "
                       "free parameter, not a derivation. Larger amplitudes overshoot and freeze the dilaton (no running "
                       "at all). The tracker estimate ignores the regime near |phi| ~ 1-3, where the potential changes "
                       "shape (V = 0 at |phi| = 1, negative below), so it is an order-of-magnitude check.")}
    json.dump(out, open("dilaton_running_F.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
