"""Filter step: rank every AxiCLASS model on the same data, and apply the A3, Late Twist (L1-L3) and robustness (R1, R2)
rules exactly as pre-registered. Reads AEGIS cmb-fit/results/cmp_<name>.json and writes MODEL_RANKING.md.
Missing runs are shown as "pending", so it can run at any time.

Rules: PREREGISTRATION_EARLY_LATE.md, PREREGISTRATION_LATE_TWIST.md (+ halofit deviation),
PREREGISTRATION_ROBUSTNESS.md. Post-hoc checks never change the official verdicts.
"""
import json
import math
import os

RES = r"C:\Users\Danny\.copilot\repos\AEGIS\cmb-fit\results"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MODEL_RANKING.md")
K = {"lcdm": 0, "w0wa": 2, "edelock": 2, "edelock_w0wa": 4, "latetwist": 2}
LABEL = {"lcdm": "ΛCDM", "w0wa": "Late w0–wa", "edelock": "Early (Locked Twist)", "edelock_w0wa": "Early + late",
         "latetwist": "Late Twist (n = 1 field)"}
PRIOR = {"log10_F": (-1.3, 0.5), "log10_m": (-0.5, 1.5)}


GRID_N = {}            # model name -> number of finished grid points (deviation 08:58: the fit is the lowest grid chi2)


GRID_LF, GRID_LM = (-0.4, -0.2, 0.0, 0.2, 0.4, 0.5), (-0.3, 0.0, 0.2, 0.4)   # the locked 08:58 grid


def is_edge(lf, lm):
    """Edge-scan points (PREREGISTRATION_EDGE_SCAN.md) lie off the 0.2 dex grid."""
    return not (any(abs(lf - g) < 1e-6 for g in GRID_LF) and any(abs(lm - g) < 1e-6 for g in GRID_LM))


def is_hc(lf, lm):
    """High-mass corner points (PREREGISTRATION_HIGH_MASS_CORNER.md): off the grid with m^2 F^2 >= 1.9."""
    return is_edge(lf, lm) and 10 ** (2 * (lf + lm)) >= 1.9


def grid_files(name):
    """Grid runs standing in for a free (F, m) fit: <base>_gF<x>m<y>[_desy5]. For the Late Twist with Pantheon+ the
    official fit uses grid points only (edge scan post-hoc there); for DES Y5 the edge points count (locked blind)."""
    import glob
    import re
    sfx = "_desy5" if name.endswith("_desy5") else ""
    base = name[:-len(sfx)] if sfx else name
    out = []
    for p in glob.glob(os.path.join(RES, f"cmp_{base}_gF*{sfx}.json")):
        n = os.path.basename(p)[4:-5]
        if not sfx and (n.endswith("_desy5") or n.endswith("_dovekie")):
            continue                                      # LD runs (PREREGISTRATION_LATE_DOVEKIE_LEE.md) are not grid points
        g = re.search(r"_gF(-?[0-9.]+)m(-?[0-9.]+)", n)
        if g:
            lf, lm = float(g.group(1)), float(g.group(2))
            if name == "ax_spa_latetwist" and is_edge(lf, lm):
                continue                                  # post-hoc for Pantheon+: reported separately
            out.append((n, lf, lm))
    return out


def load(name):
    if "_gF" not in name:
        rows = grid_files(name)
        if rows:
            GRID_N[name] = len(rows)
            ms = []
            for n, lf, lm in rows:
                m = json.load(open(os.path.join(RES, f"cmp_{n}.json")))["minimum"]
                ms.append((m["chi2"], n, {**m, "log10_F": lf, "log10_m": lm, "grid_run": n}))
            return min(ms, key=lambda t: t[0])[2]
    p = os.path.join(RES, f"cmp_{name}.json")
    return json.load(open(p))["minimum"] if os.path.exists(p) else None


def chi2(name):
    m = load(name)
    return None if m is None else m["chi2"]


def lee_and_ld():
    """PREREGISTRATION_LATE_DOVEKIE_LEE.md: LEE-G (Sidak over the distinct F values with a finite viable point, chi2 with
    2 dof, two-sided Z) and LD (Late Twist at the rule-chosen points on DES-Dovekie vs LCDM halofit Dovekie)."""
    from statistics import NormalDist
    L = []
    for name, ref, label in (("ax_spa_latetwist", "ax_spa_lcdm_halofit", "Pantheon+"),
                             ("ax_spa_latetwist_desy5", "ax_spa_lcdm_halofit_desy5", "DES Y5")):
        rows, best, r = grid_files(name), load(name), chi2(ref)
        if not rows or best is None or r is None:
            continue
        d = best["chi2"] - r
        n_eff = len({round(lf, 6) for n, lf, lm in rows})
        if d >= 0:
            L.append(f"- **LEE-G, {label}:** Δχ²_loc = {fmt(d)} → **NOT SIGNIFICANT**")
            continue
        p_loc = math.exp(d / 2)                           # P(chi2_2 >= -d)
        p_glob = 1 - (1 - p_loc) ** n_eff
        z = lambda p: NormalDist().inv_cdf(1 - p / 2) if p < 1 else 0.0
        zl, zg = z(p_loc), z(p_glob)
        v = "HOLDS" if zg >= 2 else "WEAK HINT" if zg >= 1 else "NOT SIGNIFICANT"
        L.append(f"- **LEE-G, {label}:** Δχ²_loc = {fmt(d)}, N_eff = {n_eff} F values; Z_loc {zl:.2f}σ → "
                 f"Z_glob {zg:.2f}σ → **{v}**" + ("  (grid incomplete)" if len(rows) < 24 else ""))
    ld_ref = chi2("ax_spa_lcdm_halofit_dovekie")
    import glob as _g
    pts = [(json.load(open(p))["minimum"]["chi2"], os.path.basename(p)[4:-5])
           for p in _g.glob(os.path.join(RES, "cmp_ax_spa_latetwist_gF*_dovekie.json"))]
    if pts and ld_ref is not None:
        c, n = min(pts)
        d = c - ld_ref
        v = "CONFIRMED" if d <= -4 else "WEAKENED" if d <= -1 else "NOT CONFIRMED"
        w = chi2("ax_spa_w0wa_halofit_dovekie")
        L.append(f"- **LD** (Late Twist on DES-Dovekie, {n}): Δ_D = {fmt(d)} → **{v}** (offset-corrected "
                 f"{fmt(d - 1.35)}, not used for the verdict)" + (f"; vs w0–wa {fmt(c - w)}" if w is not None else ""))
    else:
        L.append("- **LD** (Late Twist on DES-Dovekie): pending (runs after the edge scan)")
    return L


def best(*names):
    """Lowest chi2 found over runs of the same model (R1: original and best-of-4)."""
    vals = [c for c in (chi2(n) for n in names) if c is not None]
    return min(vals) if len(vals) == len(names) else None


def fmt(x, nd=2):
    return "pending" if x is None else f"{x:+.{nd}f}"


def a3_band(d):
    if d is None:
        return "pending"
    if d < -4 and d + 4 < 0:
        return "SURVIVES"
    return "NOT NEEDED" if d >= -1 else "MILD"


def l1(d):
    if d is None:
        return "pending"
    if d < -4 and d + 4 < 0:
        return "PASS"
    return "FAIL" if d >= 0 else "INCONCLUSIVE"


def l2(d):
    if d is None:
        return "pending"
    return "PREFERRED" if d < -2 else ("AS GOOD AS w0–wa" if d <= 2 else "WORSE")


def l3(m):
    if m is None:
        return "pending", ""
    lf, lm = m["log10_F"], m["log10_m"]
    F, mm = 10 ** lf, 10 ** lm
    if 0.1 <= F <= 3 and 0.5 <= mm <= 10:
        v = "CONSISTENT"
    elif F < 0.05 or F > 3 or mm < 0.3 or mm > 30:
        v = "INCONSISTENT"
    else:
        v = "BORDERLINE (between the rule's bands; reported, not judged)"
    edges = [f"{k} at its prior {'lower' if abs(x - PRIOR[k][0]) < 0.02 else 'upper'} edge"
             for k, x in (("log10_F", lf), ("log10_m", lm))
             if min(abs(x - PRIOR[k][0]), abs(x - PRIOR[k][1])) < 0.02]
    note = f"F = {F:.3g} M_Pl, m = {mm:.3g} H0" + (f"; **{', '.join(edges)}**" if edges else "")
    return v, note


def s8(m):
    return m["sigma8"] * math.sqrt(m["Omega_m"] / 0.3)


def family(suffix_main, suffix_lt):
    """Rows for one data set. Main models use HMcode; the Late Twist and its references use halofit."""
    rows = []
    ref = chi2("ax_spa_lcdm" + suffix_main)
    for mdl in ("lcdm", "w0wa", "edelock", "edelock_w0wa"):
        if mdl == "edelock" and suffix_main:          # early-only is not part of R2
            continue
        rows.append((mdl, "HMcode", "ax_spa_" + mdl + suffix_main, ref))
    ref_h = chi2("ax_spa_lcdm_halofit" + suffix_lt)
    for mdl, n in (("lcdm", "ax_spa_lcdm_halofit"), ("w0wa", "ax_spa_w0wa_halofit"), ("latetwist", "ax_spa_latetwist")):
        rows.append((mdl, "halofit", n + suffix_lt, ref_h))
    return rows


def table(title, rows):
    out = [f"### {title}", "", "| Model | Non-linear | χ² | Δχ² vs ΛCDM | ΔAIC | H₀ | S8 |", "|---|---|---|---|---|---|---|"]
    for mdl, nl, name, ref in rows:
        m = load(name)
        if m is None:
            out.append(f"| {LABEL[mdl]} | {nl} | pending | | | | |")
            continue
        d = None if ref is None else m["chi2"] - ref
        aic = None if d is None else d + 2 * K[mdl]
        out.append(f"| {LABEL[mdl]} | {nl} | {m['chi2']:.2f} | {fmt(d)} | {fmt(aic)} | {m['H0']:.2f} | {s8(m):.3f} |")
    return out + [""]


def diff(a, b):
    ca, cb = chi2(a), chi2(b)
    return None if ca is None or cb is None else ca - cb


def main():
    L = ["# Model ranking and pre-registered verdicts (AxiCLASS, one engine)", "",
         "Data: Planck low-ℓ + ACT DR6 + ACT×Planck lensing + SPT-3G D1 lite + DESI DR2 + SNe. Generated by "
         "`rank_models.py`; every number comes from AEGIS `cmb-fit/results/cmp_<name>.json`.", "",
         "## 1. Ranking", ""]
    L += table("Pantheon+ supernovae (main analysis)", family("", ""))
    L += table("DES Y5 supernovae (R2, post-hoc)", family("_desy5", "_desy5"))

    L += ["## 2. Official verdicts", ""]
    d_a3 = diff("ax_spa_edelock_w0wa", "ax_spa_w0wa")
    L.append(f"- **A3** (early alongside late): D = {fmt(d_a3)} → **{a3_band(d_a3)}**")
    d1 = diff("ax_spa_latetwist", "ax_spa_lcdm_halofit")
    d2 = diff("ax_spa_latetwist", "ax_spa_w0wa_halofit")
    v3, n3 = l3(load("ax_spa_latetwist"))
    L.append(f"- **L1** (Late Twist vs ΛCDM): Δχ² = {fmt(d1)}, ΔAIC = {fmt(None if d1 is None else d1 + 4)} → **{l1(d1)}**")
    L.append(f"- **L2** (Late Twist vs w0–wa): D = {fmt(d2)} → **{l2(d2)}**")
    L.append(f"- **L3** (natural range): **{v3}** {('(' + n3 + ')') if n3 else ''}")
    L.append("  - L3 is a weak test: its bands nearly coincide with the prior ranges (DEEP_REVIEW_2026-11-01.md, C).")
    F_EARLY = 0.1451                                  # PREREGISTRATION_SHARED_F.md (earlyF_ax_spa_edelock_w0wa.json)
    for tag, n in (("", "ax_spa_latetwist"), (" (DES Y5)", "ax_spa_latetwist_desy5")):
        m = load(n)
        if m is None:
            L.append(f"- **Shared F{tag}:** pending")
            continue
        R = m["log10_F"] - math.log10(F_EARLY)
        v = "SHARED" if abs(R) <= 0.30 else ("DIFFERENT" if abs(R) > 0.48 else "UNCLEAR")
        L.append(f"- **Shared F{tag}:** F_late/F_early = {10 ** R:.2f} (R = {R:+.2f}) → **{v}**")
    L.append("")

    L += ["## 3. Robustness (post-hoc; the official verdicts do not change)", ""]
    b_late = best("ax_spa_w0wa", "ax_spa_w0wa_b4")
    b_both = best("ax_spa_edelock_w0wa", "ax_spa_edelock_w0wa_b4")
    d_r1 = None if b_late is None or b_both is None else b_both - b_late
    r1 = "pending" if d_r1 is None else ("STABLE" if a3_band(d_r1) == a3_band(d_a3) else f"SHIFTED to {a3_band(d_r1)}")
    L.append(f"- **R1** (best of 4): D_best = {fmt(d_r1)} → band {a3_band(d_r1)} → **{r1}**")
    for a, b in (("ax_spa_w0wa", "ax_spa_w0wa_b4"), ("ax_spa_edelock_w0wa", "ax_spa_edelock_w0wa_b4")):
        L.append(f"  - restart scatter, {a}: b4 − original = {fmt(diff(b, a))}")
    d_y5 = diff("ax_spa_edelock_w0wa_desy5", "ax_spa_w0wa_desy5")
    late_y5 = diff("ax_spa_w0wa_desy5", "ax_spa_lcdm_desy5")
    same = lambda new, old: "pending" if "pending" in (new, old) else ("SAME" if new == old else f"CHANGES to {new}")
    L.append(f"- **R2, A3 with DES Y5:** D = {fmt(d_y5)} → {a3_band(d_y5)} → **{same(a3_band(d_y5), a3_band(d_a3))}**; "
             f"late gain {fmt(late_y5)} (Pantheon+: {fmt(diff('ax_spa_w0wa', 'ax_spa_lcdm'))})")
    d_dov = diff("ax_spa_edelock_w0wa_dovekie", "ax_spa_w0wa_dovekie")      # PREREGISTRATION_DOVEKIE.md
    late_dov = diff("ax_spa_w0wa_dovekie", "ax_spa_lcdm_dovekie")
    L.append(f"- **A3 with DES-Dovekie** (bracket, locked 09:56:48): D = {fmt(d_dov)} → **{a3_band(d_dov)}**; "
             f"late gain {fmt(late_dov)} (Pantheon+ {fmt(diff('ax_spa_w0wa', 'ax_spa_lcdm'))}, DES Y5 {fmt(late_y5)})")
    y1 = diff("ax_spa_latetwist_desy5", "ax_spa_lcdm_halofit_desy5")
    y2 = diff("ax_spa_latetwist_desy5", "ax_spa_w0wa_halofit_desy5")
    y3, yn3 = l3(load("ax_spa_latetwist_desy5"))
    L.append(f"- **R2, L1 with DES Y5:** Δχ² = {fmt(y1)} → {l1(y1)} → **{same(l1(y1), l1(d1))}**")
    L.append(f"- **R2, L2 with DES Y5:** D = {fmt(y2)} → {l2(y2)} → **{same(l2(y2), l2(d2))}**")
    L.append(f"- **R2, L3 with DES Y5:** {y3} {('(' + yn3 + ')') if yn3 else ''}")
    L.append("")
    # Coupled Twist (PREREGISTRATION_COUPLED_TWIST.md); C4 from weff_<name>.json written by coupled/coupled_weff.py
    L += ["## 3b. Coupled Twist (gates V1-V4 passed: COUPLED_TWIST_GATES.md)", ""]
    cfree = chi2("ax_spa_coupledtwist")
    lcdm_h, w0wa_h, lt = chi2("ax_spa_lcdm_halofit"), chi2("ax_spa_w0wa_halofit"), chi2("ax_spa_latetwist")
    c1 = None if cfree is None or lcdm_h is None else cfree - lcdm_h
    c1v = "pending" if c1 is None else ("PASS" if c1 < -6 else ("FAIL" if c1 >= 0 else "INCONCLUSIVE"))
    c2 = None if cfree is None or lt is None else cfree - lt
    c2v = "pending" if c2 is None else ("NEEDED" if c2 < -4 else ("NOT NEEDED" if c2 >= -1 else "MILD"))
    c3 = None if cfree is None or w0wa_h is None else cfree - w0wa_h + 2
    c3v = "pending" if c3 is None else ("PREFERRED" if c3 < -2 else ("AS GOOD AS" if abs(c3) <= 2 else "WORSE"))
    cm = load("ax_spa_coupledtwist") or {}
    wf = os.path.join(RES, f"weff_{cm.get('grid_run', 'ax_spa_coupledtwist')}.json")
    c4v = json.load(open(wf))["C4"] if os.path.exists(wf) else "pending"
    L.append(f"- **C1** (vs ΛCDM): Δχ² = {fmt(c1)} → **{c1v}**")
    L.append(f"- **C2** (coupling needed vs Late Twist rerun): D_c = {fmt(c2)} → **{c2v}**")
    L.append(f"- **C3** (vs w0–wa): ΔAIC = {fmt(c3)} → **{c3v}**")
    L.append(f"- **C4** (apparent phantom crossing, 0.3 < z < 2): **{c4v}**")
    c5 = [chi2(f"ax_spa_coupledtwist_beta{s}0.816") for s in ("", "-")]
    c5ok = [c for c in c5 if c is not None]
    if c5ok and lcdm_h is not None:
        d5 = min(c5ok) - lcdm_h
        L.append(f"- **C5** (|β| = 0.816 fixed): Δχ² = {fmt(d5)} → **{'SURVIVES' if d5 < 0 else 'EXCLUDED'}**")
    else:
        L.append("- **C5** (|β| = 0.816 fixed): pending, or EXCLUDED (code-limited) if both fits end with no finite point "
                 "(deviation log, 08:39)")
    prof = [(b, chi2(f"ax_spa_coupledtwist_beta{b}")) for b in ("-0.1", "-0.05", "0", "0.05", "0.1")]
    L.append("- β profile: " + ", ".join(f"β={b}: {('%.2f' % c) if c is not None else 'pending'}" for b, c in prof))
    L.append("")
    import glob as _g
    import re as _re
    edge, hc = [], []
    for p in _g.glob(os.path.join(RES, "cmp_ax_spa_latetwist_gF*.json")):
        n = os.path.basename(p)[4:-5]
        if n.endswith("_desy5") or n.endswith("_dovekie"):
            continue
        g = _re.search(r"_gF(-?[0-9.]+)m(-?[0-9.]+)", n)
        if g and is_edge(float(g.group(1)), float(g.group(2))):
            (hc if is_hc(float(g.group(1)), float(g.group(2))) else edge).append(
                (json.load(open(p))["minimum"]["chi2"], n))
    if edge:
        c, n = min(edge)
        ref = chi2("ax_spa_lcdm_halofit")
        L.append(f"- Edge scan, Pantheon+ (POST-HOC, not the official fit): best {n}, Δχ² vs ΛCDM {fmt(c - ref)}")
    gb = load("ax_spa_latetwist")
    if hc and gb is not None:
        c, n = min(hc)
        d = c - gb["chi2"]
        v = "BETTER CORNER" if d <= -1 else "SIMILAR" if d < 1 else "WORSE"
        ref = chi2("ax_spa_lcdm_halofit")
        L.append(f"- **HC** (high-mass corner, {len(hc)} of 9 finite): best {n}, Δ_HC = {fmt(d)} vs grid best → **{v}**; "
                 f"vs ΛCDM {fmt(c - ref)} (offset-corrected {fmt(c - ref - 1.35)})")
    else:
        L.append("- **HC** (high-mass corner): pending (runs after LD); no finite point at the end = NOT REACHABLE")
    nm = os.path.join(RES, "null_mirror_latetwist.json")
    if os.path.exists(nm):
        L.append("- **Null mirror:** the Late Twist code sits about +1.35 above ΛCDM in its frozen (Λ) limit "
                 "(LATE_TWIST_NULL_MIRROR.md; cause confirmed 13:06: halofit reads an Ω_m inflated by the field, and the "
                 "offset is +0.03 without halofit). Comparisons with Λ-based references carry this offset; the verdicts "
                 "above are as written.")
    L += lee_and_ld()
    L.append("")
    if GRID_N:
        L += ["## Grid status (deviation 08:58: lowest grid χ² is the fit; resolution 0.2 dex)", ""]
        for k, v in sorted(GRID_N.items()):
            m = load(k)
            L.append(f"- {k}: {v} grid point(s) finished; best = {m.get('grid_run')} (χ² {m['chi2']:.2f})"
                     + ("  ← verdicts are final only when the grid is complete" if ("latetwist" in k and v < 24)
                        or ("coupledtwist" in k and "_beta" not in k and v < 9) else ""))
        L.append("")
    L += ["## 4. Filter rule (how the headline is chosen)", "",
          "- A verdict is **solid** if R1 and R2 both report STABLE or SAME, and **fragile** otherwise.",
          "- The headline goes to the lowest-ΔAIC model whose verdict is solid. If the Late Twist is solid and at least "
          "AS GOOD AS w0–wa, it leads, and the shared-F test (PREREGISTRATION_SHARED_F.md) follows.", ""]
    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
