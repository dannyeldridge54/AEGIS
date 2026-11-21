"""RW3 — PREREG_RW3_PLATEAU. AI-assisted."""
import json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools", "weave_cm"))
import weave_reverse as wr

out = {}
# R1
a, s = 2 * math.pi, 38.6
m_single = wr.saxion_mass_over_H0(a, s, 0.685, "single", k=3)
m_swiss = wr.saxion_mass_over_H0(a, s, 0.685, "swiss", V=1e5, tv=20.15)
out["R1"] = {"m_over_H0_K3ln": m_single, "m_over_H0_swiss_V1e5": m_swiss,
             "verdict": "CAN" if min(m_single, m_swiss) <= 3 else "FAIL",
             "minimum_exists_for_a_sigma_gt_1": False,
             "note": "dV/dsigma = c e^{-a s}(1 - a s) < 0 for a s > 1: monotonic, no minimum (runaway)"}
# R2
tilts = {"sqrt2": math.sqrt(2), "2": 2.0, "2sqrt2": 2 * math.sqrt(2)}
mech = {}
for k in (1, 3):
    for n in (1, 2):
        mech[f"K=-{k}ln,1/tau^{n}"] = wr.beta_single(n, k)
for m in (0.5, 1, 1.5, 2):
    mech[f"fibre,tau1^-{m}"] = wr.beta_fibre(m)
out["R2"] = {name: {"beta": b, "matches": [t for t, v in tilts.items() if abs(b / v - 1) <= 0.05]} for name, b in mech.items()}

# R3
Om, Orad = 0.31, 9e-5


def run(beta, xi):
    # y = [phi, dphi/dN]; V = VL(1 - x), x = xi e^{-beta (phi - 0)}, phi starts at 0
    def H2(N, phi, dphi, VL):
        aa = math.exp(N)
        rho = 3 * Om * aa**-3 + 3 * Orad * aa**-4 + VL * (1 - xi * math.exp(-beta * phi))
        return rho / (3 - dphi**2 / 2)

    def rhs(N, y, VL):
        phi, dphi = y
        h2 = H2(N, phi, dphi, VL)
        aa = math.exp(N)
        V = VL * (1 - xi * math.exp(-beta * phi)); Vp = VL * beta * xi * math.exp(-beta * phi)
        # dlnH/dN = -(rho+p)/(2H^2) with rho+p = rho_m + 4/3 rho_r + dphi^2 H^2
        eps = (3 * Om * aa**-3 + 4 * Orad * aa**-4 + dphi**2 * h2) / (2 * h2)
        return [dphi, -(3 - eps) * dphi - Vp / h2]

    def H_today(VL):
        sol = solve_ivp(rhs, [math.log(1e-3), 0], [0.0, 0.0], args=(VL,), rtol=1e-9, atol=1e-12, dense_output=True)
        phi, dphi = sol.y[:, -1]
        return math.sqrt(H2(0, phi, dphi, VL)), sol
    # shoot VL: H(1) = 1
    lo, hi = 1e-3, 1e3
    for _ in range(50):
        mid = math.sqrt(lo * hi)
        if H_today(mid)[0] > 1: hi = mid
        else: lo = mid
    VL = math.sqrt(lo * hi)
    _, sol = H_today(VL)
    phi0 = sol.y[0, -1]
    viable = (1 - xi * math.exp(-beta * phi0)) > 0
    Ns = np.linspace(math.log(1 / 3), 0, 60)
    w = []
    for N in Ns:
        phi, dphi = sol.sol(N)
        h2 = H2(N, phi, dphi, VL)
        K = dphi**2 * h2 / 2; V = VL * (1 - xi * math.exp(-beta * phi))
        w.append((K - V) / (K + V))
    aa = np.exp(Ns); A = np.vstack([np.ones_like(aa), 1 - aa]).T
    w0fit, wa = np.linalg.lstsq(A, np.array(w), rcond=None)[0]
    return viable, w[-1], float(w0fit), float(wa)


xis = np.logspace(-3, math.log10(0.999), 300)
R3 = {}
for name, beta in {"2sqrt2": 2 * math.sqrt(2), "fibre_1/sqrt3": 1 / math.sqrt(3), "K3ln_sqrt(2/3)": math.sqrt(2 / 3)}.items():
    rows = []
    for xi in xis:
        try:
            v, w0, w0f, wa = run(beta, xi)
        except Exception as e:  # record, do not hide
            rows.append({"xi": float(xi), "error": str(e)}); continue
        rows.append({"xi": float(xi), "viable": bool(v), "w0": float(w0), "w0_fit": w0f, "wa": wa})
    R3[name] = rows
gate_pts = [r for r in R3["2sqrt2"] if r.get("viable") and abs(r["w0"] + 0.79) <= 0.03 and abs(r["wa"] + 0.36) <= 0.15]
out["R3_gate"] = {"pass": bool(gate_pts), "points": gate_pts[:5]}
summ = {}
for name in ("fibre_1/sqrt3", "K3ln_sqrt(2/3)", "2sqrt2"):
    vr = [r for r in R3[name] if r.get("viable")]
    inreg = [r for r in vr if -0.82 <= r["w0"] <= -0.76]
    summ[name] = {"n_viable": len(vr), "w0_min_viable": min(r["w0"] for r in vr) if vr else None,
                  "in_region": inreg[:6], "VIABLE": bool(inreg)}
out["R3"] = summ if out["R3_gate"]["pass"] else {"INVALID": "validation gate failed", "summary": summ}
# R5
m32 = 2.5e5; MP = wr.MP_GEV; H0 = wr.H0_GEV
rhoL_GeV4 = 7.1e-121 * MP**4
out["R5"] = {"Vsub_over_rhoL": m32**4 / rhoL_GeV4, "m_over_H0": (m32**2 / MP) / H0,
             "m32_for_Vsub_eq_rhoL_eV": rhoL_GeV4**0.25 * 1e9}
nat_ok = out["R5"]["m_over_H0"] <= 3
host = any(v["VIABLE"] for k, v in summ.items() if k != "2sqrt2") or any(v["matches"] for v in out["R2"].values())
out["decision"] = "HOSTED" if (host and nat_ok and out["R3_gate"]["pass"]) else "OPEN"
p = os.path.join(os.path.dirname(__file__), "..", "..", "field_tests", "results", "rw3_plateau.json")
json.dump({"summary": out, "R3_rows": R3}, open(p, "w"), indent=1)
print(json.dumps(out, indent=1))
