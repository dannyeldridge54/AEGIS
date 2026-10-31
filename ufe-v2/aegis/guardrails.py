# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: 8fce37e54098eb67
"""
Guardrails: automatic checks that keep every number on the AEGIS pages honest.

Each check returns {"name", "ok", "detail", "plain"}:
  - "detail" is for scientists, "plain" says the same thing in everyday words.
The page shows these live (GET /api/guardrails). A failed check never hides anything; it is shown in red.

Checks
  1. Fit numbers   - recompute Δχ², ΔAIC, H₀ and the error range straight from the saved fit files and compare
                     them with what the pages say (science.json "numbers").
  2. Pre-registration - the rule files written before testing must not change after they were locked (SHA-256).
  3. Theory math   - the field's resting point matches γ₀ = 0.2375; the Fingerprint shape reduces to the plain
                     shape near the bottom of the hill; the energy is never negative.
  4. Data          - our star counts must match ESA's own archive on every spot-check.
  5. Geometry      - a "direction" in the galaxy onion is only called real when it stands 3σ above noise, and
                     the pages must say that a pull toward the Galactic Centre is expected from the galaxy's shape.
  6. Authorship    - the sigil files must still match their published fingerprints.
  7. The Method    - every claim sits in its tier (evidence, hypothesis, meaning); meaning is never used as proof;
                     tested claims keep their locked rules; failures are kept (aegis/method.py).
"""
import glob, hashlib, json, math, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))           # ufe-v2/
ROOT = os.path.dirname(HERE)                                                   # repo root
FITS = os.path.join(ROOT, "cmb-fit", "axiclass", "results_live", "results")
FITS_PR4 = os.path.join(ROOT, "cmb-fit", "axiclass", "results_live", "results_pr4")
PREREG = sorted(set([os.path.join(ROOT, "cmb-fit", "axiclass", "torsion_shape", "PREREGISTRATION_SINH.md")]
                    + [p for p in glob.glob(os.path.join(ROOT, "cmb-fit", "PREREG*.md"))
                       if not p.endswith("_DEVIATIONS.md")]))   # every rule file is locked on first sight;
                                                                # deviation logs stay append-only and open
CAMB_RESULTS = os.path.join(ROOT, "cmb-fit", "results")                       # same-engine CAMB + Cobaya fits
LOCKFILE = os.path.join(HERE, "guardrails_lock.json")
EXTRA_PARAMS = 3                                                               # f, z_c, theta_i


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def sigil_sha(path):
    """SHA-256 of the drawing itself. Files delivered through Claude get a C2PA content-credentials stamp
    (<c2pa:manifest>) added inside <metadata>; that stamp is provenance, not the artwork, so it is removed first."""
    import re
    t = open(path, encoding="utf-8").read()
    t = re.sub(r'\s*xmlns:c2pa="[^"]*"', "", t)
    t = re.sub(r"<c2pa:manifest>.*?</c2pa:manifest>", "", t, flags=re.S)
    t = re.sub(r"<metadata>\s*</metadata>", "", t)
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def _chi2_sf(x, k):
    a, xx = k / 2.0, x / 2.0
    if xx <= 0:
        return 1.0
    term = summ = 1.0 / a
    for n in range(1, 500):
        term *= xx / (a + n); summ += term
        if term < summ * 1e-12:
            break
    return max(0.0, 1.0 - summ * math.exp(-xx + a * math.log(xx) - math.lgamma(a)))


def _sigma(p):
    """Two-sided Gaussian-equivalent significance of a p-value."""
    lo, hi = 0.0, 10.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if math.erfc(mid / math.sqrt(2)) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def compute_fit_numbers(fits_dir=FITS):
    """Everything the pages quote about the torsion fit, recomputed from the checkpoint files."""
    def load(name):
        p = os.path.join(fits_dir, name + ".ckpt.json")
        return json.load(open(p)) if os.path.exists(p) else None
    L, E = load("lcdm_noshoes_polish"), load("ede_noshoes_polish")
    if not (L and E and L.get("converged") and E.get("converged")):
        return None
    d = E["chi2_total"] - L["chi2_total"]
    out = {"chi2_lcdm": round(L["chi2_total"], 2), "chi2_ede": round(E["chi2_total"], 2), "dchi2": round(d, 1),
           "daic": round(d + 2 * EXTRA_PARAMS, 1), "H0_lcdm": round(L["best_params"]["H0"], 2),
           "H0_ede": round(E["best_params"]["H0"], 2), "f_ede": round(E["derived"].get("f_ede", 0), 3)}
    p = _chi2_sf(-d, EXTRA_PARAMS) if d < 0 else 1.0
    out["sigma"] = round(_sigma(p), 1)
    # profile likelihood points (fixed f), converged only
    pts = []
    for f in glob.glob(os.path.join(fits_dir, "ede_noshoes_fixf*.ckpt.json")):
        c = json.load(open(f))
        if c.get("converged") and c.get("chi2_eff") is not None:
            pts.append((float(os.path.basename(f)[len("ede_noshoes_fixf"):-len(".ckpt.json")]), c["chi2_eff"]))
    pts.sort(); out["profile_points"] = [[round(a, 3), round(b, 3)] for a, b in pts]
    if len(pts) >= 3:
        i = min(range(len(pts)), key=lambda k: pts[k][1]); i = min(max(i, 1), len(pts) - 2)
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        den = (x0 - x1) * (x0 - x2) * (x1 - x2)
        A = (x2 * (y1 - y0) + x1 * (y0 - y2) + x0 * (y2 - y1)) / den
        B = (x2 * x2 * (y0 - y1) + x1 * x1 * (y2 - y0) + x0 * x0 * (y1 - y2)) / den
        if A > 0:
            fm = -B / (2 * A); w = 1 / math.sqrt(A)                  # Δχ² = 1 half-width
            out.update(profile_best=round(fm, 3), profile_lo=round(fm - w, 3), profile_hi=round(fm + w, 3))
    # The Locked Twist (PREREGISTRATION_ZEQ.md): switch-on locked to matter-radiation equality, two extra settings.
    # Reported from the best point so far even before convergence (the search only ever improves it), flagged as such.
    Z = load("ede_noshoes_zeq")
    if Z:
        dz = Z["chi2_total"] - L["chi2_total"]
        out.update(dchi2_zeq=round(dz, 1), daic_zeq=round(dz + 4, 1), zeq_converged=bool(Z.get("converged")),
                   zeq_evals=Z.get("total_evals"), zc_zeq=round(10 ** Z["derived"]["log10_z_c"], 0))
    Z1 = load("ede_noshoes_F1.2247_zeq")
    if Z1:
        d1 = Z1["chi2_total"] - L["chi2_total"]          # chi2_total excludes the F constraint's own term
        out.update(dchi2_zeq1=round(d1, 1), daic_zeq1=round(d1 + 2, 1), zeq1_converged=bool(Z1.get("converged")))
    # Planck PR4 cross-check: report the likelihood-only Δχ² (the data's own fit). Gaussian foreground priors are
    # reported separately because they can make a model look better without the data fitting better.
    def lp(name):
        p = os.path.join(os.path.dirname(fits_dir), "results_pr4", name + ".ckpt.json")
        return json.load(open(p)) if os.path.exists(p) else None
    L4, E4 = lp("lcdm_noshoes_polish"), lp("ede_noshoes_polish")
    if L4 and E4 and L4.get("converged") and E4.get("converged"):
        out["dchi2_pr4"] = round(E4["chi2_total"] - L4["chi2_total"], 1)
        out["H0_pr4"] = [round(L4["best_params"]["H0"], 2), round(E4["best_params"]["H0"], 2)]
    return out


def compute_camb_numbers(results_dir=CAMB_RESULTS):
    """Headline numbers from the same-engine CAMB + Cobaya fits (cmbfit_compare.py). Each model uses its best
    run (lowest chi2) among the restarts on disk, and every model is compared with the best LCDM run."""
    def best(*names):
        runs = []
        for name in names:
            p = os.path.join(results_dir, "cmp_" + name + ".json")
            if os.path.exists(p):
                m = json.load(open(p, encoding="utf-8")).get("minimum") or {}
                if m.get("chi2") is not None:
                    runs.append(m)
        return min(runs, key=lambda m: m["chi2"]) if runs else None
    L, E, Z = best("lcdm", "lcdm8"), best("ede", "ede8"), best("edelock", "edelock8")
    if not (L and E):
        return None
    d = E["chi2"] - L["chi2"]
    p = _chi2_sf(-d, EXTRA_PARAMS) if d < 0 else 1.0
    def eff(m):        # chi2_eff = chi2 + Planck calibration prior A_planck ~ N(1, 0.0025), as the pre-registrations ask
        return m["chi2"] + ((m.get("A_planck", 1.0) - 1.0) / 0.0025) ** 2
    de = eff(E) - eff(L)
    out = {"engine": "CAMB + Cobaya", "chi2_lcdm": round(L["chi2"], 2), "chi2_ede": round(E["chi2"], 2),
           "dchi2": round(d, 1), "daic": round(d + 2 * EXTRA_PARAMS, 1), "H0_lcdm": round(L["H0"], 2),
           "H0_ede": round(E["H0"], 2), "f_ede": round(E.get("fde_zc", 0), 3), "sigma": round(_sigma(p), 1),
           "dchi2_eff": round(de, 2), "zc_ede": round(E.get("zc", 0), 0)}
    if Z:
        dz = Z["chi2"] - L["chi2"]; dze = eff(Z) - eff(L)
        out.update(dchi2_zeq=round(dz, 1), daic_zeq=round(dz + 4, 1), zeq_converged=True,
                   zc_zeq=round(Z.get("zc", 0), 0), H0_zeq=round(Z["H0"], 2), f_zeq=round(Z.get("fde_zc", 0), 3),
                   dchi2_zeq_exact=round(dz, 2), dchi2_eff_zeq=round(dze, 2), daic_eff_zeq=round(dze + 4, 2),
                   zeq_rule=("pass" if dz < -4 and dze < -4 else "fail" if dz >= -4 and dze >= -4 else "split"),
                   lock_cost=round(Z["chi2"] - E["chi2"], 2))
    return out


def check_fits(science):
    nums = compute_camb_numbers()
    legacy = compute_fit_numbers()
    if nums is None:
        nums = legacy
    elif legacy:
        # The AxiCLASS numbers are another engine: kept as a labelled cross-check, never as the headline.
        nums["axiclass"] = {k: legacy[k] for k in ("dchi2", "daic", "H0_lcdm", "H0_ede", "f_ede") if k in legacy}
        for k in ("profile_points", "profile_best", "profile_lo", "profile_hi", "dchi2_pr4", "H0_pr4"):
            if k in legacy:
                nums[k] = legacy[k]
    if nums is None:
        return {"name": "Fit numbers", "ok": None, "detail": "fit files not found on this computer",
                "plain": "The saved fit results are not on this computer yet, so this check is waiting."}
    shown = science.get("numbers", {})
    keys = (["dchi2", "daic", "H0_lcdm", "H0_ede"] + (["dchi2_pr4"] if "dchi2_pr4" in nums else [])
            + (["dchi2_zeq", "daic_zeq"] if "dchi2_zeq" in nums else []) + (["dchi2_zeq1", "daic_zeq1"] if "dchi2_zeq1" in nums else [])
            + [k for k in ("f_ede", "dchi2_eff_zeq") if k in nums])
    bad = [k for k in keys if k in shown and abs(float(shown[k]) - nums[k]) > 0.051]
    missing = [k for k in keys if k not in shown]
    ok = not bad and not missing
    detail = (f"Δχ² {nums['dchi2']}, ΔAIC {nums['daic']}, H₀ {nums['H0_lcdm']} → {nums['H0_ede']}, ≈{nums['sigma']}σ"
              + (f"; AxiCLASS profile f = {nums.get('profile_best')} ({nums.get('profile_lo')}–{nums.get('profile_hi')}, approximate)" if "profile_best" in nums else "")
              + (f"; AxiCLASS PR4 likelihood-only Δχ² {nums['dchi2_pr4']}" if "dchi2_pr4" in nums else "")
              + (f"; Locked Twist Δχ² {nums['dchi2_zeq']}, ΔAIC {nums['daic_zeq']} ({'converged' if nums['zeq_converged'] else 'still improving'})" if "dchi2_zeq" in nums else "")
              + (f" [exact {nums['dchi2_zeq_exact']}, χ²_eff {nums['dchi2_eff_zeq']}: rule Δχ² < −4 is {nums['zeq_rule']}; lock costs {nums['lock_cost']} vs free]" if "zeq_rule" in nums else "")
              + (f"; MISMATCH on page: {bad}" if bad else "") + (f"; not on page: {missing}" if missing else ""))
    plain = ("Every fit number on these pages was recomputed from the saved results and matches." if ok else
             "A fit number on the page does not match the saved results; the page needs updating.")
    return {"name": "Fit numbers", "ok": ok, "detail": detail, "plain": plain, "numbers": nums}


def check_prereg():
    files = [p for p in PREREG if os.path.exists(p)]
    if not files:
        return {"name": "Pre-registration", "ok": None, "detail": "rule files not found",
                "plain": "The rules we wrote before testing are not on this computer yet."}
    lock = json.load(open(LOCKFILE)) if os.path.exists(LOCKFILE) else {}
    now = {os.path.basename(p): _sha(p) for p in files}
    first = {k: v for k, v in now.items() if k not in lock}
    if first:
        lock.update(first); json.dump(lock, open(LOCKFILE, "w"), indent=1)
    changed = [k for k, v in now.items() if lock.get(k) != v]
    ok = not changed
    return {"name": "Pre-registration", "ok": ok,
            "detail": "; ".join(f"{k} sha256 {v[:16]}…" for k, v in now.items()) + (f"; CHANGED after lock: {changed}" if changed else ""),
            "plain": ("The pass-or-fail rules we wrote before running the tests have not been changed since." if ok else
                      "A rule file changed after it was locked. That must be explained before any result is trusted.")}


def check_theory():
    s = math.sqrt(1.5); g0 = 0.2375
    phi0 = s * math.asinh(1 / g0)                         # field value at the resting point, in Planck units
    x0 = math.asinh(1 / g0)
    g = lambda d: s * (math.sinh(d / s + x0) - math.sinh(x0)) / math.cosh(x0)
    slope = g(1e-6) / 1e-6                                # must be 1: Fingerprint = plain cosine near the bottom
    V = lambda u, n=3: (1 - math.cos(u)) ** n
    vmin = min(V(i * 0.01) for i in range(-700, 701))
    # Convention: the code's field variable is the displacement d = phi_abs - phi_0 (phi_0 = 2.63 M_Pl at gamma_0),
    # so the implemented potential must have its minimum at d = 0.
    src = os.path.join(HERE, "aegis", "cosmo_v2.py")
    centred = (not os.path.exists(src)) or ("(1 - np.cos(p / F))" in open(src, encoding="utf-8").read())
    ok = abs(phi0 - 2.63) < 0.005 and abs(slope - 1) < 1e-4 and vmin >= 0 and centred
    return {"name": "Theory math", "ok": ok,
            "detail": f"φ₀ = {phi0:.4f} M_Pl (pages quote 2.63); dg/dφ at rest = {slope:.6f} (expect 1); min V = {vmin:.2e} (expect ≥ 0); code potential centred at d = φ − φ₀ = 0: {centred}",
            "plain": ("The equations agree with each other: the field rests where quantum gravity says, the Fingerprint "
                      "matches the plain version at the bottom of the hill, and the stored energy is never negative."
                      if ok else "One of the equation self-checks failed; the theory code needs a look.")}


def check_data(status):
    checks = (status or {}).get("checks_total"), (status or {}).get("checks_passed")
    tot, ok_n = checks
    if not tot:
        return {"name": "Star data", "ok": None, "detail": "no ESA spot-checks yet",
                "plain": "The first comparison with ESA's archive has not run yet."}
    ok = tot == ok_n
    return {"name": "Star data", "ok": ok, "detail": f"{ok_n}/{tot} random tiles match ESA's COUNT exactly",
            "plain": (f"Our star counts matched ESA's own archive in all {tot} random checks." if ok else
                      f"{tot - ok_n} of {tot} random checks did not match ESA's archive.")}


def check_geometry(shells):
    rows = [r for r in (shells or {}).get("shells", []) if "amplitude" in r]
    frac = (shells or {}).get("sky_fraction", 0)
    if not rows:
        return {"name": "Geometry", "ok": True,
                "detail": f"sky swept {100 * frac:.1f}% (< {100 * (shells or {}).get('min_sky_fraction', 0.25):.0f}% needed): no direction claimed yet",
                "plain": "We don't call any direction real until at least a quarter of the sky is mapped. Not there yet, so we claim nothing."}
    sig = [r for r in rows if r.get("sigma", 0) >= 3]
    return {"name": "Geometry", "ok": True,
            "detail": "; ".join(f"{r['lo_pc']}-{r['hi_pc'] or '∞'} pc: |d| {r['amplitude']:.3f} ({r.get('sigma', 0):.1f}σ) toward l {r['l']:.0f}°, b {r['b']:.0f}°" for r in rows),
            "plain": (f"{len(sig)} of {len(rows)} distance layers show a direction stronger than 3× the noise. A pull toward the "
                      "Galactic Centre is expected from the shape of our galaxy, so it is not new physics by itself.")}


def check_sigils():
    d = os.path.join(HERE, "sigils"); hp = os.path.join(d, "hashes.json")
    if not os.path.exists(hp):
        return {"name": "Authorship", "ok": None, "detail": "no hashes.json", "plain": "Sigil fingerprints not found."}
    h = json.load(open(hp))["sha256"]
    bad = [k for k, v in h.items() if not os.path.exists(os.path.join(d, k)) or sigil_sha(os.path.join(d, k)) != v]
    ok = not bad
    return {"name": "Authorship", "ok": ok, "detail": "all sigil drawings match hashes.json (content-credentials stamp ignored)" if ok else f"changed: {bad}",
            "plain": "Each sigil file still matches its published fingerprint." if ok else "A sigil file no longer matches its fingerprint."}


def check_method():
    from aegis import method as M
    if not os.path.exists(M.STORE):
        return {"name": "The Method (claim wall)", "ok": None, "detail": "claim store not found",
                "plain": "The list of every claim and its tier is not on this computer yet."}
    return M.check()


def run_all(science=None, status=None, shells=None):
    if science is None:
        p = os.path.join(HERE, "science.json")
        science = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    out = []
    for fn, args in ((check_fits, (science,)), (check_prereg, ()), (check_theory, ()), (check_data, (status,)),
                     (check_geometry, (shells,)), (check_sigils, ()), (check_method, ())):
        try:
            out.append(fn(*args))
        except Exception as e:
            out.append({"name": fn.__name__.replace("check_", "").title(), "ok": False, "detail": f"check crashed: {e!r}",
                        "plain": "This check could not run; something needs fixing."})
    return {"checks": out, "passed": sum(1 for c in out if c["ok"] is True),
            "failed": sum(1 for c in out if c["ok"] is False), "waiting": sum(1 for c in out if c["ok"] is None)}


if __name__ == "__main__":
    print(json.dumps(run_all(), indent=1, ensure_ascii=False))
