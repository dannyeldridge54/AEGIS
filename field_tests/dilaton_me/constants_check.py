"""Constants check (EXPLORATORY tool, not a verdict): for an early electron-mass shift Delta0 = m_e/m_e0 - 1 held until a
light field thaws at z_t, after which a QUADRATICALLY coupled field oscillates with phi^2 ~ a^-3 (hyperlight scalar, as
arXiv 2502.04432), the shift seen later is Delta(z) = Delta0 ((1+z)/(1+z_t))^3 (envelope). Checks:
  quasar (methanol, z ~ 0.89):  |Delta(0.89)| < 1.5e-7   (Kanekar et al. 2015)
  atomic clocks today:          |d ln m_e/dt| ~ Delta(0) * 2 m_phi < 1e-16 /yr, with m_phi ~ H(z_t) (thaw when H = m)
  no galactic clustering:       m_phi < 1e-28 eV (Jeans length > ~15 Mpc), so no local density enhancement
  BBN:                          Y_p shift = 0.74 * Delta0 * Y_p (Nakashima et al. 2008, arXiv 0803.0247: ~7.4% per 10% m_e)
Also the flagship dilaton coupled linearly (phi_history.json) for contrast.
    python constants_check.py [Delta0]   -> constants_check.json"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D0 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0078
H0, Om, Or = 67.2, 0.315, 9.1e-5
h_eV = H0 / 3.0857e19 * 6.582e-16                 # H0 in eV
yr = 3.156e7 / 6.582e-16                          # 1 yr in 1/eV
H = lambda z: h_eV * np.sqrt(Om * (1 + z) ** 3 + Or * (1 + z) ** 4 + 1 - Om)
rows = []
for zt in (50, 70, 100, 150, 200, 300, 500, 800):
    m = H(zt)
    d089 = D0 * (1.89 / (1 + zt)) ** 3
    d0 = D0 * (1 / (1 + zt)) ** 3
    drift = d0 * 2 * m * yr
    rows.append({"z_thaw": zt, "m_phi_eV": float(f"{m:.2e}"), "Delta(z=0.89)": float(f"{d089:.2e}"), "quasar_ok": bool(d089 < 1.5e-7),
                 "drift_per_yr": float(f"{drift:.2e}"), "clock_ok": bool(drift < 1e-16), "no_clustering": bool(m < 1e-28)})
    print(rows[-1])
out = {"note": "EXPLORATORY tool; envelope estimates", "Delta0": D0, "BBN_dYp_over_Yp": round(0.74 * D0, 5),
       "BBN_dYp_abs": round(0.74 * D0 * 0.245, 5), "Planck_sigma_YHe": 0.012, "thaw_table": rows,
       "allowed_z_thaw": [r["z_thaw"] for r in rows if r["quasar_ok"] and r["clock_ok"] and r["no_clustering"]]}
ph = json.load(open(os.path.join(HERE, "phi_history.json")))
out["flagship_dilaton_linear"] = {"Delta(z=0.89)": ph["implied_dlnme_z0.89"], "drift_per_yr": ph["implied_dlnme_dt_per_yr"],
                                  "quasar_ok": False, "clock_ok": False}
json.dump(out, open(os.path.join(HERE, "constants_check.json"), "w"), indent=1)
print("allowed z_thaw:", out["allowed_z_thaw"], "| BBN dYp:", out["BBN_dYp_abs"])
