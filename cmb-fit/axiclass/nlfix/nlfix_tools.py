# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Run names for the NR replication (CubeMind PREREGISTRATION_NLFIX_REPLICATION.md). All names end in "_nlfix".
    python nlfix_tools.py stage1     -> Late Twist grids (Pantheon+, DES Y5), edge points (both), HC points
    python nlfix_tools.py ld         -> LD points chosen by the LD rule on the stage 1 NR results (DES-Dovekie)
    python nlfix_tools.py coupled    -> 3x3 Coupled Twist grid around the best stage 1 Pantheon+ GRID point
    python nlfix_tools.py final      -> C5 and the beta profile at the best stage 3 point"""
import os as _os
_AXI = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_RESULTS = _os.environ.get("TWIST_RESULTS", _os.path.join(_os.path.dirname(_AXI), "results"))
_BUILDS = _os.environ.get("TWIST_BUILDS", _os.path.expanduser("~"))
import glob
import json
import os
import re
import sys

OUT = _RESULTS
LF = (-0.4, -0.2, 0.0, 0.2, 0.4, 0.5)
LM = (-0.3, 0.0, 0.2, 0.4)
EDGE = ("gF0m0.057", "gF0m0.102", "gF0.2m-0.143", "gF0.2m-0.098", "gF0.4m-0.343", "gF0.4m-0.298", "gF0.5m-0.443",
        "gF0.5m-0.398")
HC = ("gF-0.6m0.751", "gF-0.6m1.052", "gF-0.6m1.353", "gF-0.4m0.551", "gF-0.4m0.852", "gF-0.4m1.153", "gF-0.2m0.351",
      "gF-0.2m0.652", "gF-0.2m0.953")
f = lambda x: f"{x:g}"
GRID = [f"gF{f(a)}m{f(b)}" for a in LF for b in LM]


def chi2(n):
    p = f"{OUT}/cmp_{n}.json"
    return json.load(open(p))["minimum"]["chi2"] if os.path.exists(p) else None


def best(names):
    rows = [(chi2(n), n) for n in names if chi2(n) is not None]
    return min(rows) if rows else None


def tagof(n):
    g = re.search(r"_gF(-?[0-9.]+)m(-?[0-9.]+)", n)
    return float(g.group(1)), float(g.group(2))


what = sys.argv[1]
if what == "stage1":
    out = [f"ax_spa_latetwist_{t}_nlfix" for t in GRID] + [f"ax_spa_latetwist_{t}_desy5_nlfix" for t in GRID]
    out += [f"ax_spa_latetwist_{t}_desy5_nlfix" for t in EDGE] + [f"ax_spa_latetwist_{t}_nlfix" for t in EDGE]
    out += [f"ax_spa_latetwist_{t}_nlfix" for t in HC]
    print("\n".join(out))
elif what == "ld":
    d = best([f"ax_spa_latetwist_{t}_desy5_nlfix" for t in GRID + list(EDGE)])
    p = best([f"ax_spa_latetwist_{t}_nlfix" for t in GRID])
    pts = []
    for b in (d, p):
        if b:
            t = re.search(r"_(gF-?[0-9.]+m-?[0-9.]+)_", b[1] + "_").group(1)
            if f"ax_spa_latetwist_{t}_dovekie_nlfix" not in pts:
                pts.append(f"ax_spa_latetwist_{t}_dovekie_nlfix")
    print("\n".join(pts))
elif what == "coupled":
    _, n = best([f"ax_spa_latetwist_{t}_nlfix" for t in GRID])
    lf, lm = tagof(n)
    print("\n".join(f"ax_spa_coupledtwist_gF{f(round(lf + da, 2))}m{f(round(lm + db, 2))}_nlfix"
                    for da in (-0.2, 0, 0.2) for db in (-0.2, 0, 0.2)))
elif what == "final":
    _, n = best([os.path.basename(p)[4:-5] for p in glob.glob(f"{OUT}/cmp_ax_spa_coupledtwist_gF*_nlfix.json")])
    lf, lm = tagof(n)
    t = f"_gF{f(lf)}m{f(lm)}"
    print("\n".join([f"ax_spa_coupledtwist_beta0.816{t}_nlfix", f"ax_spa_coupledtwist_beta-0.816{t}_nlfix"]
                    + [f"ax_spa_coupledtwist_beta{b}{t}_nlfix" for b in ("-0.1", "-0.05", "0", "0.05", "0.1")]))
