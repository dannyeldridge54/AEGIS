"""One workbook with everything relevant to the UFE / Twist question, gathered from this PC.

    python build_master_sheet.py      -> UFE_MASTER_SHEET.xlsx (rebuild any time; reads files only)

Tabs: Summary, CAMB fits, z_c profile, AxiCLASS fits, Live runs, Claims, Pre-registrations, Inventory.
Significance: p = chi2.sf(-dchi2, k extra settings), sigma = two-sided normal equivalent (same as the checklist).
"""
import datetime
import glob
import hashlib
import json
import math
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.abspath(__file__))
FIT = os.path.join(ROOT, "cmb-fit")
RES = os.path.join(FIT, "results")
UFE = os.path.join(ROOT, "ufe-v2")
CUBE = r"C:\Users\Danny\Desktop\CubeMind_side_project"
OUT = os.path.join(ROOT, "UFE_MASTER_SHEET.xlsx")
EXTRA = {"lcdm": 0, "wcdm": 1, "ede": 3, "edelock": 2}
SN_NAMES = {"_dovekie": "DES-Dovekie", "_desy5": "DES Y5", "_union3": "Union3", "_shoes": "Pantheon+ & SH0ES", "_s8A": "+S8(A)", "_s8B": "+S8(B)"}
HEAD = Font(bold=True, color="FFFFFF")
FILL = PatternFill("solid", fgColor="1F3A5F")
GOOD, BAD = PatternFill("solid", fgColor="D8F0D8"), PatternFill("solid", fgColor="F6D5D5")


# ---------------------------------------------------------------- statistics (no scipy needed)
def chi2_sf(x, k):
    if x <= 0:
        return 1.0
    if k == 1:
        return math.erfc(math.sqrt(x / 2))
    if k == 2:
        return math.exp(-x / 2)
    if k == 3:
        return math.erfc(math.sqrt(x / 2)) + math.sqrt(2 * x / math.pi) * math.exp(-x / 2)
    return float("nan")


def sigma(p):
    """Two-sided normal equivalent of p (bisection on erfc)."""
    if not 0 < p < 1:
        return 0.0
    lo, hi = 0.0, 40.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if math.erfc(mid / math.sqrt(2)) > p else (lo, mid)
    return lo


def strength(d, k):
    if d is None or k == 0 or d >= 0:
        return None, None
    p = chi2_sf(-d, k)
    return round(p, 4), round(sigma(p), 2)


# ---------------------------------------------------------------- readers
def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def classify(name):
    """(data set, model family, extra settings, profile log10 z_c or None)."""
    data, core = "Planck18+DESI2+Pantheon+", name
    if core.startswith("pact_"):
        data, core = "P-ACT+DESI2+Pantheon+ (blind)", core[5:]
    for suf, label in SN_NAMES.items():
        if core.endswith(suf):
            data, core = (data + " " + label) if suf in ("_s8A", "_s8B") else (data.replace("Pantheon+", label) if suf != "_shoes" else data + " +SH0ES"), core[:-len(suf)]
    if core.startswith("zc"):
        return data, "ede (z_c fixed)", 2, float(core[2:])
    if core.startswith("th"):
        return data, f"ede (theta_i fixed {core[2:]})", 2, None
    fam = next((f for f in ("edelock", "ede", "wcdm", "lcdm") if core.startswith(f)), core)
    return data, fam, EXTRA.get(fam, 0), None


def camb_rows():
    rows = []
    for p in sorted(glob.glob(os.path.join(RES, "cmp_*.json"))):
        d = load(p)
        if not d:
            continue
        m, name = d["minimum"], d["run"]
        data, fam, k, zc = classify(name)
        s8 = m["sigma8"] * math.sqrt(m["omegam"] / 0.3) if "sigma8" in m and "omegam" in m else None
        rows.append(dict(run=name, data=data, model=fam, k=k, zc_fixed=zc, chi2=m.get("chi2"), H0=m.get("H0"),
                         f_ede=m.get("fde_zc"), log10_zc=m.get("log10_zc"), theta_i=m.get("theta_i"),
                         omegam=m.get("omegam"), sigma8=m.get("sigma8"), S8=s8, rdrag=m.get("rdrag"),
                         chi2_cmb=m.get("chi2__CMB"), chi2_bao=m.get("chi2__BAO"), chi2_sn=m.get("chi2__SN"),
                         minutes=round(d.get("seconds", 0) / 60, 1),
                         finished=datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M")))
    refs = {}
    for r in rows:
        if r["model"] == "lcdm":
            refs[r["data"]] = min(refs.get(r["data"], 1e99), r["chi2"])
    for r in rows:
        ref = refs.get(r["data"])
        r["ref_lcdm_chi2"] = ref
        r["dchi2"] = round(r["chi2"] - ref, 2) if ref is not None else None
        r["dAIC"] = round(r["dchi2"] + 2 * r["k"], 2) if r["dchi2"] is not None else None
        r["p"], r["sigma"] = strength(r["dchi2"], r["k"])
    return rows


def axiclass_rows():
    out = []
    for p in sorted(glob.glob(os.path.join(FIT, "axiclass", "**", "*.ckpt.json"), recursive=True)):
        d = load(p) or {}
        b, dv = d.get("best_params", {}), d.get("derived", {})
        out.append(dict(file=os.path.relpath(p, FIT), model=d.get("model"), chi2=d.get("chi2_total"),
                        H0=b.get("H0"), f_ede=dv.get("f_ede"), log10_zc=dv.get("log10_z_c"),
                        theta_i=b.get("scf_param_1"), sigma8=dv.get("sigma8"), omegam=dv.get("Omega_m"),
                        rs_drag=dv.get("rs_drag"), converged=d.get("converged"), updated=d.get("updated")))
    return out


def prereg_rows():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "**", "PREREG*.md"), recursive=True)):
        if "venv" in p or "_stale" in p:
            continue
        with open(p, "rb") as f:
            raw = f.read()
        title = raw.decode("utf-8", "replace").splitlines()[0].lstrip("# ").strip()
        out.append(dict(file=os.path.relpath(p, ROOT), title=title,
                        modified=datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M"),
                        sha256=hashlib.sha256(raw).hexdigest()[:16]))
    return out


def size_of(path):
    if os.path.isfile(path):
        return os.path.getsize(path), 1
    total = n = 0
    for dp, _, fs in os.walk(path):
        for f in fs:
            try:
                total += os.path.getsize(os.path.join(dp, f)); n += 1
            except OSError:
                pass
    return total, n


INVENTORY = [
    ("Theory", os.path.join(ROOT, "papers", "torsion_born_ede.pdf"), "The torsion-born EDE paper (PDF + .tex)"),
    ("Theory", os.path.join(ROOT, "MODEL_v2.md"), "Current model in two tiers; open problems"),
    ("Theory", os.path.join(UFE, "UFE_MODEL.md"), "The UFE model: equations, fitted values, status"),
    ("Theory", os.path.join(UFE, "hypotheses", "HOLD_RELEASE.md"), "Hypothesis: hold and release (the missing parameter)"),
    ("Method", os.path.join(ROOT, "AEGIS_METHOD.md"), "Rules every agent follows (tiers, the wall)"),
    ("Method", os.path.join(UFE, "method", "claims.json"), "Claim ledger (see Claims tab)"),
    ("Fit code", os.path.join(FIT, "cmbfit.py"), "CAMB + Cobaya model / likelihood setup"),
    ("Fit code", os.path.join(FIT, "cmbfit_compare.py"), "Same-data comparisons, SN swaps, SH0ES, profile"),
    ("Fit code", os.path.join(FIT, "run_lanes.py"), "Parallel fit runner (7 lanes x 2 threads)"),
    ("Fit results", os.path.join(RES, "COMPARE.md"), "Comparison tables (rebuilt after every fit)"),
    ("Fit results", os.path.join(RES, "chains"), "Cobaya outputs (.minimum files)"),
    ("Fit results", os.path.join(FIT, "axiclass"), "Earlier AxiCLASS fits (cloud engine)"),
    ("Data", os.path.join(FIT, "packages", "data", "planck_2018_pliklite_native"), "Planck 2018 high-l TTTEEE lite"),
    ("Data", os.path.join(FIT, "packages", "data", "planck_2018_lowT_native"), "Planck 2018 low-l TT"),
    ("Data", os.path.join(FIT, "packages", "data", "planck_2018_lowE_native"), "Planck 2018 low-l EE"),
    ("Data", os.path.join(FIT, "packages", "data", "ACTDR6CMBonly"), "ACT DR6 CMB-only (blind test)"),
    ("Data", os.path.join(FIT, "packages", "data", "ACT_dr6_likelihood"), "ACT DR6 lensing"),
    ("Data", os.path.join(FIT, "packages", "data", "bao_data"), "DESI DR2 BAO and others"),
    ("Data", os.path.join(FIT, "packages", "data", "sn_data"), "Pantheon+, DES Y5, DES-Dovekie, Union3, JLA"),
    ("Data", os.path.join(UFE, "data"), "UFE v2 data (Pantheon+ binned full covariance)"),
    ("Data", os.path.join(UFE, "cosmos_map", "cosmos_map_stars.csv"), "Gaia star map (192M stars swept)"),
    ("Side tests", os.path.join(ROOT, "research"), "Exoplanet locks, impact rhythm"),
    ("Side tests", os.path.join(FIT, "metatron"), "Metatron ratio test (failed)"),
    ("Other repos", os.path.join(ROOT, "..", "torsion-lambda-toolkit"), "TorsionΛ pre-simulation toolkit (TypeScript)"),
    ("Other repos", os.path.join(ROOT, "..", "NEXUS"), "NEXUS parameter-exploration daemon"),
]


# ---------------------------------------------------------------- writing
def sheet(wb, title, header, rows, widths=None):
    ws = wb.create_sheet(title)
    ws.append(header)
    for c in ws[1]:
        c.font, c.fill = HEAD, FILL
    for r in rows:
        ws.append([round(v, 4) if isinstance(v, float) else v for v in r])
    ws.freeze_panes = "A2"
    for i, h in enumerate(header, 1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(h, max(10, min(40, len(str(h)) + 4)))
    return ws


def main():
    fits, axi, pre = camb_rows(), axiclass_rows(), prereg_rows()
    claims = (load(os.path.join(UFE, "method", "claims.json"), {}) or {}).get("claims", {})
    status = load(os.path.join(RES, "lanes", "status.json"), {}) or {}
    queue = load(os.path.join(RES, "lanes", "queue.json"), []) or []
    by = {r["run"]: r for r in fits}

    def get(run, key):
        v = by[run][key] if run in by and by[run].get(key) is not None else "not yet"
        return round(v, 4) if isinstance(v, float) else v

    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    ws.column_dimensions["A"].width, ws.column_dimensions["B"].width = 46, 90
    lines = [
        ("UFE / Twist master sheet", f"built {datetime.datetime.now():%Y-%m-%d %H:%M} from files on this PC (rebuild: python build_master_sheet.py)"),
        ("Question", "Is the Twist (torsion-born early dark energy) preferred over the standard model (ΛCDM)?"),
        ("", ""),
        ("Fair Planck test: Locked Twist (edelockP vs best ΛCDM)", f"Δχ² {get('edelockP', 'dchi2')}, ΔAIC {get('edelockP', 'dAIC')}, {get('edelockP', 'sigma')}σ  (fair only once lcdmP exists: {'yes' if 'lcdmP' in by else 'NOT YET'})"),
        ("Fair Planck test: free Twist (edeP vs best ΛCDM)", f"Δχ² {get('edeP', 'dchi2')}, ΔAIC {get('edeP', 'dAIC')}, {get('edeP', 'sigma')}σ"),
        ("BLIND test (P-ACT), rule: Δχ² < −4 (PREREGISTRATION_ZEQ.md)", f"Locked Twist Δχ² {get('pact_edelock', 'dchi2')}  (needs pact_lcdm: {'done' if 'pact_lcdm' in by else 'RUNNING'})"),
        ("Supernova robustness (Dovekie / DES Y5 / Union3)", ", ".join(f"{s}: {get('edelockP' + s, 'dchi2')}" for s in ("_dovekie", "_desy5", "_union3"))),
        ("With SH0ES (not independent evidence)", f"Locked Twist Δχ² {get('edelockP_shoes', 'dchi2')}, H0 {get('edelockP_shoes', 'H0')}"),
        ("S8 (weak-lensing check)", f"ΛCDM {get('lcdm8', 'S8')}  vs  Twist {get('ede8', 'S8')}, polished Twist {get('edeP', 'S8')} (compare with verified weak-lensing values; checklist Phase 4)"),
        ("", ""),
        ("Theory gap", "Torsion-only prediction F = 1.2247 M_Pl failed (Δχ² +13.8). Data want F ≈ 0.14 M_Pl (≈1/8.9). Until a new torsion-only prediction exists, fits cannot tell the Twist from generic EDE."),
        ("Verdict", "TIE (filed 2026-10-29 10:45 under PREREGISTRATION_VERDICT.md). Blind ACT test PASSED (Δχ² −7.23, 2.2σ); fair Planck −4.70; all 3 supernova sets pass; but S8 costs +2.41 vs DES Y3+KiDS-1000 (limit 2; +0.39 vs KiDS-Legacy). With that S8 in the fit the gain drops to −2.92. Favours early energy switching on at equality; does NOT show torsion is the cause."),
        ("Live runs", f"{sum(v['status'] == 'done' for v in status.values())} done, {sum(v['status'] == 'running' for v in status.values())} running, {sum(v['status'] == 'failed' for v in status.values())} failed, {len([q for q in queue if q['name'] not in status])} waiting"),
        ("How to read strength", "σ = how surprising the improvement would be if the extra settings did nothing. ~1–2σ = a hint; 3σ = evidence; 5σ = discovery."),
    ]
    for a, b in lines:
        ws.append([a, b])
    ws["A1"].font = Font(bold=True, size=14)
    for row in ws.iter_rows(min_row=2):
        row[0].font = Font(bold=True)
        row[1].alignment = Alignment(wrap_text=True, vertical="top")

    cols = ["run", "data", "model", "k", "chi2", "ref_lcdm_chi2", "dchi2", "dAIC", "p", "sigma", "H0", "f_ede",
            "log10_zc", "theta_i", "omegam", "sigma8", "S8", "rdrag", "chi2_cmb", "chi2_bao", "chi2_sn", "minutes", "finished"]
    w = sheet(wb, "CAMB fits", cols, [[r.get(c) for c in cols] for r in fits if r["zc_fixed"] is None],
              {"run": 18, "data": 34, "model": 14})
    for row in w.iter_rows(min_row=2):
        d = row[cols.index("dchi2")].value
        if isinstance(d, (int, float)) and row[cols.index("k")].value:
            row[cols.index("dchi2")].fill = GOOD if d < -4 else (BAD if d > 0 else PatternFill())

    prof = sorted((r for r in fits if r["zc_fixed"] is not None), key=lambda r: r["zc_fixed"])
    sheet(wb, "z_c profile", ["log10_zc", "z_c", "chi2", "dchi2 vs best ΛCDM", "f_ede", "H0", "theta_i", "S8", "finished"],
          [[r["zc_fixed"], round(10 ** r["zc_fixed"]), r["chi2"], r["dchi2"], r["f_ede"], r["H0"], r["theta_i"], r["S8"], r["finished"]] for r in prof])

    acols = ["file", "model", "chi2", "H0", "f_ede", "log10_zc", "theta_i", "sigma8", "omegam", "rs_drag", "converged", "updated"]
    sheet(wb, "AxiCLASS fits", acols, [[r.get(c) for c in acols] for r in axi], {"file": 55, "model": 26})

    lrows = []
    for q in queue:
        s = status.get(q["name"], {})
        lrows.append([q["name"], s.get("status", "waiting"), s.get("lane"), s.get("start"), s.get("end"), s.get("minutes"),
                      json.dumps(q.get("env", {})), s.get("note", "")])
    sheet(wb, "Live runs", ["job", "status", "lane", "start", "end", "minutes", "env", "note"], lrows, {"env": 50, "start": 20, "end": 20})

    ccols = ["id", "tier", "status", "statement", "result", "prereg", "updated"]
    w = sheet(wb, "Claims", ccols, [[c.get(k) if k != "id" else cid for k in ccols] for cid, c in claims.items()],
              {"statement": 70, "result": 70, "prereg": 30, "id": 22})
    for row in w.iter_rows(min_row=2):
        st = row[2].value
        row[2].fill = GOOD if st == "passed" else (BAD if st == "failed" else PatternFill())
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    sheet(wb, "Pre-registrations", ["file", "title", "modified", "sha256"], [[r[k] for k in ("file", "title", "modified", "sha256")] for r in pre],
          {"file": 50, "title": 80})

    inv = []
    for group, path, what in INVENTORY:
        if os.path.exists(path):
            b, n = size_of(path)
            inv.append([group, what, os.path.normpath(path), round(b / 1e6, 2), n,
                        datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")])
        else:
            inv.append([group, what, os.path.normpath(path), None, 0, "missing"])
    sheet(wb, "Inventory", ["group", "what", "path", "MB", "files", "modified"], inv, {"what": 50, "path": 80})

    wb.save(OUT)
    print(f"saved {OUT}: {len(fits)} CAMB fits, {len(prof)} profile points, {len(axi)} AxiCLASS fits, "
          f"{len(claims)} claims, {len(pre)} pre-registrations, {len(inv)} inventory rows")


if __name__ == "__main__":
    main()
