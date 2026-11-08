"""Score UB-P (field_tests/rules/PREREG_UB2_PREDICTIONS.md): re-solve the joined field's background at each UB-2 best
fit (cmb-fit/results/cmp_ub2B*.json) with the UB-2 code and check the five predicted ranges.
    python ub_p_score.py      (needs the CAMB build with the UB module, like the UB-2 fits)"""
import json, math, os, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CF = os.path.join(HERE, "..", "..", "cmb-fit")
sys.path.insert(0, CF)
import camb  # noqa: E402
import ub2_fit as U  # noqa: E402

rule = open(os.path.join(HERE, "..", "rules", "PREREG_UB2_PREDICTIONS.md"), encoding="utf-8").read()
rng = {}
for key, pat in (("F_at_peak", r"F during the early boost[^|]*\|\s*([-\d.]+)\s*to\s*([-\d.]+)"),
                 ("z_peak", r"z_peak \|\s*([-\d.]+)\s*to\s*([-\d.]+)"), ("f_peak", r"f_peak \|\s*([-\d.]+)\s*to\s*([-\d.]+)"),
                 ("w0", r"w0 today \|\s*([-\d.]+)\s*to\s*([-\d.]+)"), ("kappa", r"slope κ \|\s*([-\d.]+)\s*to\s*([-\d.]+)")):
    m = re.search(pat, rule)
    rng[key] = (float(m.group(1)), float(m.group(2)))


def quantities(mn):
    p = camb.set_params(H0=mn["H0"], ombh2=mn["ombh2"], omch2=mn["omch2"], mnu=0.06, num_massive_neutrinos=1, nnu=3.044,
                        As=2.1e-9, ns=0.965)
    rho, rhop, other0 = U.other_densities(p)
    par = {k: mn[k] for k in ("ub_lnL", "ub_thi", "ub_phii", "ub_kappa")}
    rf, lnA, t = U.field_history(par, "B", rho, rhop, other0)
    z = np.exp(-U.LNA) - 1
    other = np.array([rho(N) for N in U.LNA])
    f = rf / (rf + other)
    early = z >= 1500
    i = int(np.argmax(np.where(early, f, -1)))
    F = U.UB.FP * np.exp(U.UB.LAM * t["chi"] / 2)
    kin = (t["chiN"] ** 2 + F ** 2 * t["thN"] ** 2) / 2 * t["H2"] / 3
    V = rf - kin
    return {"F_at_peak": float(F[i]), "z_peak": float(z[i]), "f_peak": float(f[i]),
            "w0": float((kin[-1] - V[-1]) / (kin[-1] + V[-1])), "kappa": mn["ub_kappa"]}


rows = {}
for sn, name in (("Pantheon+", "ub2B"), ("DES-Dovekie", "ub2B_dovekie"), ("Union3", "ub2B_union3")):
    pth = os.path.join(CF, "results", f"cmp_{name}.json")
    if not os.path.exists(pth):
        rows[sn] = "NO VERDICT (fit missing)"
        continue
    q = quantities(json.load(open(pth))["minimum"])
    inside = {k: rng[k][0] <= q[k] <= rng[k][1] for k in rng}
    n = sum(inside.values())
    rows[sn] = {"values": {k: round(v, 4) for k, v in q.items()}, "inside": inside,
                "reading": "HOLDS" if n == 5 else "PARTLY" if n >= 3 else "FAILS"}
reads = [r["reading"] for r in rows.values() if isinstance(r, dict)]
overall = "HOLDS" if reads.count("HOLDS") >= 2 else "FAILS" if reads.count("FAILS") >= 2 else "MIXED"
print(json.dumps({"rule": "PREREG_UB2_PREDICTIONS.md", "ranges": rng, "rows": rows, "verdict": overall}, indent=1))
