"""Command line: inflation-scorecard (score a model) and janus (predict the running)."""
from __future__ import annotations
import argparse, sys
from . import core, janus as J

def scorecard_main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="inflation-scorecard", description="Score an inflation model against current data.")
    ap.add_argument("--label", default="model"); ap.add_argument("--ns", type=float, nargs="+", required=True, help="n_s, or min max")
    ap.add_argument("--r", type=float, default=0.0); ap.add_argument("--alpha-s", type=float, default=0.0); ap.add_argument("--beta-s", type=float, default=0.0)
    ap.add_argument("--sum-mnu", type=float); ap.add_argument("--neff", type=float, default=3.044); ap.add_argument("--fnl", type=float)
    ap.add_argument("--janus-p", type=float, help="plateau exponent p (adds a Janus self-consistency row)"); ap.add_argument("--janus-kappa", type=float, help="kappa = q/p")
    ap.add_argument("--data", help="alternative constraints.yaml"); ap.add_argument("--camb", action="store_true", help="add Lyman-alpha and S8 (needs camb)")
    ap.add_argument("--out", help="write markdown here"); ap.add_argument("--figure", help="write the n_s-by-release figure here")
    a = ap.parse_args(argv)
    ns = (a.ns[0], a.ns[-1])
    m = core.Model(a.label, ns, a.r, a.alpha_s, a.beta_s, a.sum_mnu, a.neff, a.fnl, a.janus_p, a.janus_kappa)
    C = core.load_constraints(a.data); rows = core.score(m, C, a.camb); md = core.to_markdown(m, rows, C)
    if a.out: open(a.out, "w", encoding="utf-8").write(md)
    else: print(md)
    if a.figure: core.ns_figure(m, C, a.figure)
    return 0

def janus_main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="janus", description="Predict alpha_s and beta_s from (n_s, r) for V ~ 1 - A e^{-p phi} + delta e^{q phi}.")
    ap.add_argument("ns", type=float); ap.add_argument("r", type=float)
    ap.add_argument("--p", type=float, help="plateau exponent p"); ap.add_argument("--kappa", type=float, help="q/p")
    ap.add_argument("--class", dest="cls", choices=list(J.MODEL_CLASSES), help="use a built-in model class")
    ap.add_argument("--serapis-offset", action="store_true", help="use the offset-corrected SERAPIS tau=i form (D640)")
    a = ap.parse_args(argv)
    if a.serapis_offset:
        res = J.janus_offset_serapis(a.ns, a.r)
    else:
        p, k = (J.MODEL_CLASSES[a.cls][:2] if a.cls else (a.p, a.kappa))
        if p is None or k is None: ap.error("give --p and --kappa, or --class")
        res = J.janus(a.ns, a.r, p, k)
    print(f"x = {res.x:.4f}   alpha_s = {res.alpha_s:.4e}   beta_s = {res.beta_s:.4e}")
    return 0

if __name__ == "__main__":
    sys.exit(scorecard_main())
