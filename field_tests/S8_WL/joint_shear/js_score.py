"""JOINT-SHEAR scoring (field_tests/rules/PREREG_JOINT_SHEAR.md), cloud, after the 6 PC fits (cmp_<base>__jsfit.json)
are copied into cmb-fit/results.
    PYTHONPATH=<plain AxiCLASS build lib> TWIST_RESULTS=<scratch dir with links to cmb-fit/results> CSL_DIR=... python js_score.py
LCDM P(k) uses the plain AxiCLASS build (the one that made the stored LCDM files; checked bit-identical 10 Nov).
Per SN set: P(k) (axiclass_pk) -> axionHMcode (axhm_pk) -> the full DES Y3 shear chi2_WL with the LATE-BASE equal-effort
search (run_part2.minimise_pair), S8-A vs LCDM. Then
  total(model) = chi2(fit) - chi2__js_shear (the emulator term) + chi2_WL(full)
  Delta = total(S8-A) - total(LCDM): SURVIVES SHEAR <= -4; TIE if none <= -4 and none >= +2; else MIXED (2 of 3).
  NO VERDICT for a set where |q - full| > 1 for either model.  -> field_tests/results/js_score.json"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WL = os.path.dirname(HERE)
AEGIS = os.path.abspath(os.path.join(WL, "..", ".."))
RES = os.environ["TWIST_RESULTS"]
OUTR = os.path.join(WL, "results")
SETS = {"Pantheon+": "", "DES-Dovekie": "_dovekie", "Union3": "_union3"}


def pk(name):
    for script, d, f in (("axiclass_pk.py", "part2", f"pk_{name}.npz"), ("axhm_pk.py", "nonlinear", f"pk_{name}_axhm.npz")):
        if not os.path.exists(os.path.join(OUTR, f)):
            subprocess.run([sys.executable, script, name], cwd=os.path.join(WL, d), check=True)
    src = os.path.join(RES, f"cmp_{name}.json")
    dst = os.path.join(RES, f"cmp_{name}_axhm.json")
    if not os.path.exists(dst):
        os.symlink(src, dst)


def main():
    sys.path.insert(0, os.path.join(WL, "part2"))
    import run_part2 as P
    out = {"rule": "PREREG_JOINT_SHEAR.md", "rows": {}}
    reads = []
    for sn, suf in SETS.items():
        a, b = f"S8A{suf}__jsfit", f"ax_spa_lcdm_halofit{suf}__jsfit"
        fits = {n: json.load(open(os.path.join(RES, f"cmp_{n}.json")))["minimum"] for n in (a, b)}
        for n in (a, b):
            pk(n)
        best, tries = P.minimise_pair(("pk", f"{a}_axhm"), ("pk", f"{b}_axhm"))
        row = {}
        for n in (a, b):
            f, full = fits[n], best[f"{n}_axhm"]["chi2_WL"]
            qv = f["chi2__js_shear"]
            row[n] = {"chi2_fit": f["chi2"], "q": qv, "chi2_WL_full": full, "q_minus_full": round(qv - full, 3),
                      "total": round(f["chi2"] - qv + full, 3), "H0": f.get("H0"), "sigma8": f.get("sigma8"),
                      "beta_eff": f.get("beta_eff")}
        d = row[a]["total"] - row[b]["total"]
        ok = all(abs(row[n]["q_minus_full"]) <= 1 for n in (a, b))
        row["Delta"] = round(d, 2) if ok else None
        row["Delta_WL_only"] = round(row[a]["chi2_WL_full"] - row[b]["chi2_WL_full"], 2)
        row["tries"] = {k: [t["chi2_WL"] for t in v] for k, v in tries.items()}
        out["rows"][sn] = row
        reads.append(d if ok else None)
        json.dump(out, open(os.path.join(AEGIS, "field_tests", "results", "js_score.json"), "w"), indent=1)
    valid = [d for d in reads if d is not None]
    if len(valid) < 2:
        verdict = "NO VERDICT"
    elif sum(d <= -4 for d in valid) >= 2:
        verdict = "SURVIVES SHEAR"
    elif not any(d <= -4 for d in valid) and not any(d >= 2 for d in valid):
        verdict = "TIE"
    else:
        verdict = "MIXED"
    out["verdict"] = verdict
    json.dump(out, open(os.path.join(AEGIS, "field_tests", "results", "js_score.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
