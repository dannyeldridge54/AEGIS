"""KiDS-Legacy full-shear test (field_tests/rules/PREREG_KIDS_LEGACY_SHEAR.md), same equal-effort search as
field_tests/S8_WL/part2/run_part2.py. Cosmology fixed at each stored best fit; only KiDS nuisance parameters (baryon
feedback logT_AGN, mass-dependent intrinsic alignments, n(z) shifts) are minimised, with KiDS's own priors.
    KIDS_DIR=<unpacked release> KIDS_DEPS=<dir with 2pt_stats, CosmoPipe> CSL_DIR=... TWIST_RESULTS=... \
    python run_kids.py [pair ...]     -> ../results/part3_kids_legacy.json
chi2_KiDS = -2 ln(posterior) at the nuisance-only maximum (likelihood x KiDS nuisance priors), as Part 2."""
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
AEGIS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PK = os.path.join(HERE, "..", "results")
OUT = os.environ.get("KIDS_OUT", os.path.join(HERE, "..", "results"))
RES = os.environ.get("TWIST_RESULTS", os.path.join(AEGIS, "cmb-fit", "results"))
KIDS = os.environ["KIDS_DIR"]
DEPS = os.environ["KIDS_DEPS"]
CSL = os.environ["CSL_DIR"]
CONF = os.path.join(KIDS, "chains_and_config_files", "cosebis")
SN = (("Pantheon+", ""), ("DES-Dovekie", "_dovekie"), ("Union3", "_union3"))
sys.path.insert(0, os.path.join(AEGIS, "field_tests", "S8_WL", "part2"))


def _better_lcdm(suf):
    best, name = None, f"ax_spa_lcdm_halofit{suf}_s8y6"
    for n in (name, name + "_more"):
        p = os.path.join(RES, f"cmp_{n}.json")
        if os.path.exists(p):
            c = json.load(open(p))["minimum"]["chi2"]
            if best is None or c < best:
                best, name = c, n
    return name


PAIRS = {}
for sn, suf in SN:
    PAIRS[f"Spiral, {sn}"] = (("boost", f"ax_spa_spiraltwist{suf}_nlfix", f"ax_spa_spiraltwist{suf}_nlfix"),
                              ("boost", f"ax_spa_lcdm_halofit{suf}", f"ax_spa_lcdm_halofit{suf}"))
    PAIRS[f"S8-J joint Spiral, {sn}"] = (("boost", f"ax_spa_spiraltwist{suf}_nlfix_s8y6", f"ax_spa_spiraltwist{suf}_nlfix_s8y6"),
                                         ("boost", _better_lcdm(suf), _better_lcdm(suf)))
    PAIRS[f"S8-L light angle, {sn}"] = (("stored", f"spiralL{suf}_axhm", f"spiralL{suf}"),
                                        ("stored", f"ax_spa_lcdm_halofit{suf}_axhm", f"ax_spa_lcdm_halofit{suf}"))


def _cpl(fit):
    p = os.path.join(AEGIS, "theory", f"fpc_{fit}.json")
    if os.path.exists(p):
        d = json.load(open(p))
        if d.get("w0_cpl") is not None:
            return d["w0_cpl"], d["wa_cpl"]
    return -1.0, 0.0


def _values(fit, start, fix_logT):
    import numpy as np
    m = json.load(open(os.path.join(RES, f"cmp_{fit}.json")))["minimum"]
    txt = open(os.path.join(CONF, "KiDS_Legacy_values.ini")).read()
    cosmo = (f"[cosmological_parameters]\nomch2 = {m['omega_cdm']}\nombh2 = {m['omega_b']}\nh0 = {m['H0'] / 100}\n"
             f"n_s = {m['n_s']}\nomega_k = 0.0\nw = -1.0\nwa = 0.0\nmnu = 0.06\n\n")
    rest = txt.split("[halo_model_parameters]")[1]
    rest = "[halo_model_parameters]" + rest.replace("log_t_agn =", "logT_AGN =")
    if fix_logT:
        rest = re.sub(r"logT_AGN = .*", "logT_AGN = 8.0", rest)
    if start:
        src = re.sub(r"np\.float64\(([^)]*)\)", r"\1", open(start).read())
        secs = re.split(r"(?m)^(?=\[)", src)
        rest = "".join(x for x in secs if x.strip() and not x.startswith("[cosmological_parameters]"))
        if fix_logT:
            rest = re.sub(r"(?mi)^logt_agn = .*", "logT_AGN = 8.0", rest)
    return cosmo + rest


def run(nl, pkname, fit, start=None, tag_suffix=""):
    import numpy as np
    m = json.load(open(os.path.join(RES, f"cmp_{fit}.json")))["minimum"]
    tag = os.path.join(OUT, f"part3_{pkname}{tag_suffix}")
    vals = tag + "_values.ini"
    open(vals, "w").write(_values(fit, start, nl == "stored"))
    pk = os.path.join(PK, f"pk_{pkname}.npz")
    d = np.load(pk)
    omc_today = float(d["omega_m"]) * float(d["h0"]) ** 2 - m["omega_b"] - 0.06 / 93.14
    w0, wa = _cpl(fit)
    p = open(os.path.join(CONF, "KiDS_Legacy_cosebis_pipeline.ini")).read()
    for a, c in {"/MY/PATH/": OUT + "/", "%(MY_PATH)s/OUTPUT/FOLDER/": OUT + "/", "%(MY_PATH)s/CONFIG/FOLDER/": CONF + "/",
                 "%(MY_PATH)s/DATA/FOLDER/": os.path.join(KIDS, "data") + "/",
                 "%(MY_PATH)s/INSTALL/cosmosis-standard-library/": CSL + "/",
                 "%(MY_PATH)s/INSTALL/2pt_stats/": os.path.join(DEPS, "2pt_stats") + "/",
                 "%(MY_PATH)s/INSTALL/CosmoPowerCosmosis/": os.path.join(DEPS, "CosmoPowerCosmosis") + "/",
                 "%(MY_PATH)s/INSTALL/CosmoPipe/": os.path.join(DEPS, "CosmoPipe") + "/"}.items():
        p = p.replace(a, c)
    p = p.replace("modules = sample_S8 correlated_dz_priors load_nz_fits cosmopower camb ",
                  "modules = correlated_dz_priors load_nz_fits kids_pk ")
    p = p.replace("values = %(CONFIG_FOLDER)s/KiDS_Legacy_values.ini", f"values = {vals}")
    p = p.replace("sampler_name = nautilus", "sampler_name = " + os.environ.get("KIDS_SAMPLER", "maxlike"))
    p = p.replace("[DEFAULT]", f"[DEFAULT]\nWnLogPath = {OUT}/WnLog/", 1)
    p += (f"\n[kids_pk]\nfile = {os.path.join(HERE, 'kids_pk.py')}\npk_file = {pk}\nnonlinear = "
          f"{'stored' if nl == 'stored' else 'camb_boost'}\nomega_b = {m['omega_b']}\nomega_cdm = {omc_today}\n"
          f"n_s = {m['n_s']}\nw0 = {w0}\nwa = {wa}\ncache_file = {os.path.join(OUT, 'boost_' + pkname + '.npz')}\n"
          f"\n[maxlike]\nmethod = Nelder-Mead\ntolerance = 1e-3\nmaxiter = 6000\noutput_ini = {tag}_best.ini\n"
          f"max_posterior = T\n")
    p = re.sub(r"(?m)^filename = .*", f"filename = {tag}.txt", p, count=1)
    ini = tag + "_pipeline.ini"
    open(ini, "w").write(p)
    os.makedirs(os.path.join(OUT, "WnLog"), exist_ok=True)
    if os.path.exists(tag + ".txt"):
        os.remove(tag + ".txt")
    subprocess.run(["cosmosis", ini], cwd=OUT, check=True, stdout=open(tag + ".log", "w"), stderr=subprocess.STDOUT)
    head, row = None, None
    for line in open(tag + ".txt"):
        if head is None and line.startswith("#") and not line.startswith("##"):
            head = line.lstrip("#").split()
        elif not line.startswith("#") and line.strip():
            row = [float(x) for x in line.split()]
    dd = dict(zip(head, row))
    post = [v for k, v in dd.items() if k.endswith("post")][0]
    like = [v for k, v in dd.items() if k.lower().endswith("like")]
    return {"run": pkname, "fit": fit, "best_ini": tag + "_best.ini", "chi2_KiDS": round(-2 * post, 3),
            "data_chi2": round(-2 * like[0], 3) if like else None, "w0": w0, "wa": wa}


def minimise_pair(a, b):
    pool = ThreadPoolExecutor(int(os.environ.get("KIDS_WORKERS", "2")))
    fa, fb = pool.submit(run, *a), pool.submit(run, *b)
    tries = {a[1]: [fa.result()], b[1]: [fb.result()]}
    for rnd in range(1, 4):
        best = {k: min(v, key=lambda r: r["chi2_KiDS"]) for k, v in tries.items()}
        jobs = []
        for mod, other in ((a, b[1]), (b, a[1])):
            for src, lab in ((best[mod[1]], "own"), (best[other], "cross")):
                jobs.append((mod[1], pool.submit(run, *mod, src["best_ini"], f"_round{rnd}_{lab}")))
        improved = False
        for name, f in jobs:
            r = f.result()
            tries[name].append(r)
            improved |= r["chi2_KiDS"] < best[name]["chi2_KiDS"] - 0.05
        if not improved:
            break
    return {k: min(v, key=lambda r: r["chi2_KiDS"]) for k, v in tries.items()}, tries


def main():
    os.makedirs(OUT, exist_ok=True)
    want = sys.argv[1:] or list(PAIRS)
    path = os.path.join(OUT, "part3_kids_legacy.json")
    out = json.load(open(path)) if os.path.exists(path) else {
        "rule": "PREREG_KIDS_LEGACY_SHEAR.md", "data": "KiDS-Legacy COSEBIs (Wright et al. 2025), fiducial settings",
        "rows": {}}
    for lab in want:
        a, b = PAIRS[lab]
        best, tries = minimise_pair(a, b)
        x, y = best[a[1]], best[b[1]]
        d = x["chi2_KiDS"] - y["chi2_KiDS"]
        out["rows"][lab] = {"model": x, "LCDM": y, "Delta_KiDS": round(d, 2), "reading": "PASSES" if d <= 2 else "OVER",
                            "tries": {k: [t["chi2_KiDS"] for t in v] for k, v in tries.items()}}
        json.dump(out, open(path, "w"), indent=1)
    print(json.dumps({k: (v["Delta_KiDS"], v["reading"]) for k, v in out["rows"].items()}, indent=1))


if __name__ == "__main__":
    main()
