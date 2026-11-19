"""D1555 — Janus L2: second-order n_t and n_t + r/8 for both vacua (PREREG_D1555)."""
import json
from mpmath import mp, mpf, euler, log, findroot
mp.dps = 30
C = euler + log(2) - 2
d = json.load(open("field_tests/results/D1480_pivot.json"))
out = {"D": "D1555", "C": float(C)}
for key in ("rho_A1", "tau_i_NA12"):
    ns, r = mpf(d[key]["k005"]["ns"]), mpf(d[key]["k005"]["r"])
    nt_obs = -(r/8)*(2 - r/8 - ns); dev = nt_obs + r/8
    f = lambda e1, e2: [-2*e1 - e2 - 2*e1**2 - (2*C+3)*e1*e2 - (ns-1), 16*e1*(1 + C*e2) - r]
    e1, e2 = findroot(f, (r/16, 1-ns))
    nt_eps = -2*e1 - 2*e1**2 - 2*(C+1)*e1*e2
    out[key] = {"ns": float(ns), "r": float(r), "eps1": float(e1), "eps2": float(e2),
                "nt_obs": float(nt_obs), "nt_eps": float(nt_eps), "cross_diff": float(nt_obs - nt_eps),
                "dev": float(dev), "dev_over_nt": float(dev/nt_obs), "first_order_nt": float(-r/8),
                "cross_check": "PASS" if abs(nt_obs - nt_eps) <= 1e-7 else "FAIL"}
out["rho_minus_taui_nt"] = out["rho_A1"]["nt_obs"] - out["tau_i_NA12"]["nt_obs"]
out["rho_minus_taui_dev"] = out["rho_A1"]["dev"] - out["tau_i_NA12"]["dev"]
json.dump(out, open("field_tests/results/D1555_tensor_tilt.json", "w"), indent=1)
print(json.dumps(out, indent=1))
