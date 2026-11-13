"""NS-PURE (rule: field_tests/rules/PREREG_NS_PURE.md). Same data as V6; PURE-TWIST vs LCDM, n_s free.
    python ns_pure_fit.py gate PURE|LCDM
    python ns_pure_fit.py fit PURE|LCDM        (LCDM: reuses the V6 LCDM fit if present)
    python ns_pure_fit.py score               -> field_tests/results/ns_pure.json
PC, WSL env "aegis". AI-assisted."""
import json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import v6_pr4_fit as V
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_NS_PURE.md")
V.RULE = RULE
V.BASE = dict(V.BASE, PURE="ax_spa_spiraltwist_kappa0.8165_beta0_nlfix")


def _setup(which):
    """V6 setup; PURE has no stored fit-C minimum, so it starts from the LCDM one (only shared params are used)."""
    if which == "PURE":
        orig = V.BASE["PURE"]
        try:
            return V.setup("PURE")
        except FileNotFoundError:
            import early_late_spa as E, s8_joint_fit as J
            E._maybe_coupled(V.engine("PURE")); info = E.make(V.engine("PURE"))
            info["likelihood"].pop(V.OLD); info["likelihood"][V.NEW] = None; J.add_s8(info)
            m = json.load(open(f"{E.OUT}/cmp_{V.BASE['LCDM']}_cmbplanck_s8y6.json"))["minimum"]
            return E, info, m
    return V.setup(which)


V.setup = _setup


def score():
    res = os.environ.get("TWIST_RESULTS", os.path.join(AEG, "cmb-fit", "results"))
    f = {w: json.load(open(os.path.join(res, f"cmp_{V.name(w)}.json")))["minimum"] for w in ("PURE", "LCDM")}
    nsP, nsL = f["PURE"]["n_s"], f["LCDM"]["n_s"]; d = nsP - nsL
    gate = abs(nsL - 0.969) <= 0.005
    reading = ("NO VERDICT (gate failed)" if not gate else "SUPPORTED" if d <= -0.003 and nsP <= 0.9705
               else "NOT SUPPORTED" if d > -0.001 else "PARTIAL")
    keep = ("chi2", "n_s", "H0", "Omega_m", "sigma8")
    out = {"rule": "PREREG_NS_PURE.md", "n_s_PURE": nsP, "n_s_LCDM": nsL, "delta_n_s": round(d, 4),
           "delta_chi2": round(f["PURE"]["chi2"] - f["LCDM"]["chi2"], 3), "gate": gate, "reading": reading,
           "fits": {w: {k: v.get(k) for k in keep} | {"chi2_parts": {k: x for k, x in v.items() if k.startswith("chi2__")}}
                    for w, v in f.items()}}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "ns_pure.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"gate": lambda: V.gate(a[1]), "fit": lambda: V.fit(a[1]), "score": score}[a[0]]()
