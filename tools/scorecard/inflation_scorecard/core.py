"""Scorecard core: pulls and verdicts. Only numpy + pyyaml needed; CAMB optional (Lyman-alpha, S8)."""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from importlib import resources
from typing import Optional
import yaml

@dataclass
class Model:
    label: str = "model"
    ns: tuple = (0.965, 0.965)          # band (min, max); a single value -> (v, v)
    r: float = 0.0
    alpha_s: float = 0.0
    beta_s: float = 0.0
    sum_mnu: Optional[float] = None     # eV
    neff: float = 3.044
    fnl: Optional[float] = None         # default: single-field (5/12)(1 - n_s)
    @property
    def ns_mid(self): return 0.5 * (self.ns[0] + self.ns[1])

@dataclass
class Row:
    group: str
    dataset: str
    detail: str
    pull: Optional[float]
    verdict: str
    ref: str = ""

def load_constraints(path=None) -> dict:
    if path:
        return yaml.safe_load(open(path, encoding="utf-8"))
    return yaml.safe_load(resources.files("inflation_scorecard").joinpath("data/constraints.yaml").read_text(encoding="utf-8"))

def verdict(p: Optional[float]) -> str:
    if p is None: return "-"
    a = abs(p)
    return "consistent" if a < 2 else ("tension" if a < 3 else "fail")

def band_distance(lo, hi, c, s):
    near = 0.0 if lo <= c <= hi else min(abs(c - lo), abs(c - hi)) / s
    far = max(abs(c - lo), abs(c - hi)) / s
    return near, far

def score(m: Model, C: dict, use_camb: bool = False) -> list[Row]:
    rows: list[Row] = []
    lo, hi = m.ns
    for d in C["ns_releases"]:
        near, far = band_distance(lo, hi, d["value"], d["sigma"])
        rows.append(Row("n_s by release", d["name"], f"{d['value']} ± {d['sigma']}: nearest edge {near:.2f}σ, far edge {far:.2f}σ", near, verdict(near), d["arxiv"]))
    for d in C["running"]:
        p = (m.alpha_s - d["value"]) / d["sigma"]
        rows.append(Row("running α_s", d["name"], f"{d['value']} ± {d['sigma']}", p, verdict(p), d["arxiv"]))
    for d in C["r_limits"]:
        ok = m.r < d["limit95"]
        rows.append(Row("tensor ratio r", d["name"], f"r = {m.r:.2e} vs < {d['limit95']} (95%)", None, "consistent" if ok else "excluded", d["arxiv"]))
    if m.sum_mnu is not None:
        for d in C["neutrino_mass_sum_eV"]:
            ok = m.sum_mnu < d["limit95"]
            rows.append(Row("Σm_ν", d["name"], f"{m.sum_mnu:.4f} vs < {d['limit95']} eV (margin {d['limit95'] - m.sum_mnu:+.4f})", None, "consistent" if ok else "excluded", d["arxiv"]))
    for d in C["neff"]:
        p = (m.neff - d["value"]) / d["sigma"]
        rows.append(Row("N_eff", d["name"], f"{m.neff} vs {d['value']} ± {d['sigma']}", p, verdict(p), d["arxiv"]))
    fnl = m.fnl if m.fnl is not None else 5 / 12 * (1 - m.ns_mid)
    for d in C["fnl_local"]:
        p = (fnl - d["value"]) / d["sigma"]
        rows.append(Row("f_NL local", d["name"], f"{fnl:.4f} vs {d['value']} ± {d['sigma']}", p, verdict(p), d["arxiv"]))
    if use_camb:
        rows += camb_rows(m, C)
    return rows

def camb_linear(ns, a, b, C):
    import numpy as np, camb
    cc = C["cosmology_for_camb"]
    p = camb.CAMBparams(); p.set_cosmology(H0=cc["H0"], ombh2=cc["ombh2"], omch2=cc["omch2"], mnu=cc["mnu"])
    p.InitPower.set_params(As=cc["As"], ns=ns, nrun=a, nrunrun=b, pivot_scalar=cc["pivot"])
    p.set_matter_power(redshifts=[3.0, 0.0], kmax=50); res = camb.get_results(p)
    kh, z, pk = res.get_matter_power_spectrum(minkh=1e-3, maxkh=40, npoints=600)
    h = cc["H0"] / 100; kp = 0.009 * res.hubble_parameter(3.0) / 4.0
    iz = list(z).index(3.0); k = kh * h; P = pk[iz] / h**3
    lnk = np.log(k); lnD = np.log(k**3 * P / (2 * np.pi**2))
    f = lambda x: np.interp(x, lnk, lnD)
    D2 = math.exp(f(math.log(kp))); nL = (f(math.log(kp) + 0.01) - f(math.log(kp) - 0.01)) / 0.02 - 3
    s8 = res.get_sigma8_0(); Om = (cc["ombh2"] + cc["omch2"] + cc["mnu"] / 93.14) / h**2
    return D2, nL, s8 * math.sqrt(Om / 0.3)

def camb_rows(m: Model, C: dict) -> list[Row]:
    rows = []
    D2, nL, S8 = camb_linear(m.ns_mid, m.alpha_s, m.beta_s, C)
    for d in C["lya_compressed"]:
        pa = (D2 - d["delta2"]) / d["delta2_sigma"]; pn = (nL - d["n"]) / d["n_sigma"]
        rows.append(Row("Lyman-α (z=3)", d["name"] + " amplitude", f"Δ²_L {D2:.4f} vs {d['delta2']} ± {d['delta2_sigma']}", pa, verdict(pa), d["arxiv"]))
        rows.append(Row("Lyman-α (z=3)", d["name"] + " slope", f"n_L {nL:.4f} vs {d['n']} ± {d['n_sigma']}", pn, verdict(pn), d["arxiv"]))
    for d in C["s8"]:
        p = (S8 - d["value"]) / d["sigma"]
        rows.append(Row("S8", d["name"], f"{S8:.4f} vs {d['value']} ± {d['sigma']} (A_s fixed)", p, verdict(p), d["arxiv"]))
    return rows

def to_markdown(m: Model, rows: list[Row], C: dict) -> str:
    out = [f"# Inflation Scorecard: {m.label}", "",
           f"Inputs: n_s {m.ns[0]}–{m.ns[1]}, r {m.r:g}, α_s {m.alpha_s:g}, β_s {m.beta_s:g}, Σm_ν {m.sum_mnu}, N_eff {m.neff}. Data file version {C['version']}.",
           "Verdict per dataset: |pull| < 2 consistent, 2–3 tension, > 3 fail (datasets are correlated; do not combine pulls).", "",
           "| Probe | Dataset | Comparison | Pull (σ) | Verdict | arXiv |", "|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r.group} | {r.dataset} | {r.detail} | {'' if r.pull is None else f'{r.pull:+.2f}'} | {r.verdict} | {r.ref} |")
    return "\n".join(out) + "\n"

def ns_figure(m: Model, C: dict, path: str):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=200)
    ax.axhspan(m.ns[0], m.ns[1], color="#c9a227", alpha=0.3, lw=0, label=f"{m.label} band")
    for d in C["ns_releases"]:
        ax.errorbar(d["year"], d["value"], yerr=d["sigma"], fmt="o", ms=4, color="#1f3b5c", capsize=2, lw=1)
    ax.set_xlabel("release year"); ax.set_ylabel(r"$n_s$"); ax.legend(fontsize=7, frameon=False, loc="lower right")
    fig.tight_layout(); fig.savefig(path)
