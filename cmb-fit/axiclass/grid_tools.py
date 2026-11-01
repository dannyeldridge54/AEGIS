# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""(F, m) profile grid run names (deviation 08:58, CubeMind PREREGISTRATION_SPT3G_DEVIATIONS.md).
    python grid_tools.py latetwist [_desy5]   -> the 24 Late Twist grid run names
    python grid_tools.py coupled              -> 3x3 Coupled Twist grid around the best Late Twist (Pantheon+) point
    python grid_tools.py final                -> C5 (beta = +-0.816) and the 5-point beta profile at the best coupled point
    python grid_tools.py best <prefix>        -> best grid run for a prefix (name, chi2, log10F, log10m)
"""
import glob
import json
import os
import re
import sys

OUT = "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results"
LF = (-0.4, -0.2, 0.0, 0.2, 0.4, 0.5)
LM = (-0.3, 0.0, 0.2, 0.4)


def tag(lf, lm):
    f = lambda x: f"{x:g}"
    return f"_gF{f(lf)}m{f(lm)}"


def best(prefix, suffix=""):
    rows = []
    for p in glob.glob(f"{OUT}/cmp_{prefix}_gF*{suffix}.json"):
        n = os.path.basename(p)[4:-5]
        if suffix == "" and n.endswith("_desy5"):
            continue
        g = re.search(r"_gF(-?[0-9.]+)m(-?[0-9.]+)", n)
        rows.append((json.load(open(p))["minimum"]["chi2"], n, float(g.group(1)), float(g.group(2))))
    return min(rows) if rows else None


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "latetwist":
        sfx = sys.argv[2] if len(sys.argv) > 2 else ""
        print("\n".join(f"ax_spa_latetwist{tag(a, b)}{sfx}" for a in LF for b in LM))
    elif what == "coupled":
        _, _, lf, lm = best("ax_spa_latetwist")
        print("\n".join(f"ax_spa_coupledtwist{tag(round(lf + da, 2), round(lm + db, 2))}"
                        for da in (-0.2, 0, 0.2) for db in (-0.2, 0, 0.2)))
    elif what == "final":
        _, _, lf, lm = best("ax_spa_coupledtwist")
        t = tag(lf, lm)
        print("\n".join([f"ax_spa_coupledtwist_beta0.816{t}", f"ax_spa_coupledtwist_beta-0.816{t}"]
                        + [f"ax_spa_coupledtwist_beta{b}{t}" for b in ("-0.1", "-0.05", "0", "0.05", "0.1")]))
    elif what == "best":
        print(best(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ""))
