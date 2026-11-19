"""D1478: pulls of SERAPIS points against 2609.35964v1 Table III (read from the paper, PDF)."""
import json
MODELS = {"rho_A1": (0.974393, -9.9796e-4), "tau_i_NA12": (0.97462, -8.5430e-4)}
ROWS = [  # (dataset, model, n_s, sig, alpha_s, sig)
 ("P-ACT-LB", "LCDM+alpha_s", 0.9741, 0.0033, 0.0062, 0.0053),
 ("CMB-PAS+DESI DR2", "LCDM+alpha_s", 0.9737, 0.0027, 0.0062, 0.0049),
 ("CMB-PAS+DESI DR2", "w0waCDM+alpha_s", 0.9702, 0.0029, 0.0054, 0.0049),
 ("CMB-PAS+DESI DR2", "LCDM+alpha_s+Neff", 0.9790, 0.0062, 0.0102, 0.0063),
 ("CMB-PAS+DESI DR2", "LCDM+alpha_s+Neff+mnu", 0.9758, 0.0064, 0.0080, 0.0064)]
out = {"source": "arXiv:2609.35964v1 Table III", "rows": []}
for d, m, ns, sn, a, sa in ROWS:
    r = {"data": d, "model": m}
    for k, (mns, ma) in MODELS.items():
        r[k] = {"pull_ns": round((mns - ns) / sn, 3), "pull_as": round((ma - a) / sa, 3)}
    out["rows"].append(r)
allp = [abs(v) for r in out["rows"] for k in MODELS for v in r[k].values()]
out["max_abs_pull"] = max(allp); out["verdict"] = "PASS" if max(allp) < 2 else "FAIL"
json.dump(out, open("field_tests/results/D1478_lit_pulls.json", "w"), indent=1)
for r in out["rows"]: print(r)
print(out["max_abs_pull"], out["verdict"])
