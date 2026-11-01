# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""CubeMind PREREGISTRATION_LATE_DOVEKIE_LEE.md: choose the LD points by rule and print the run names (one per line).
DES Y5 official best = lowest chi2 over grid + edge points; Pantheon+ official best = lowest chi2 over grid points only.
Grid points have m in {-0.3, 0, 0.2, 0.4}; edge points (PREREGISTRATION_EDGE_SCAN.md) carry 3-decimal m values."""
import glob
import json
import os
import re

OUT = "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results"
GRID_M = {"-0.3", "0", "0.2", "0.4"}


def points(suffix, with_edge):
    best = None
    for f in glob.glob(f"{OUT}/cmp_ax_spa_latetwist_gF*{suffix}.json"):
        tag = os.path.basename(f)[len("cmp_ax_spa_latetwist_"):-len(f"{suffix}.json")]
        g = re.fullmatch(r"gF(-?[0-9.]+)m(-?[0-9.]+)", tag)
        if not g or (g.group(2) not in GRID_M and not with_edge):
            continue
        chi2 = json.load(open(f))["minimum"].get("chi2")
        if chi2 is not None and chi2 == chi2 and (best is None or chi2 < best[0]):
            best = (chi2, tag)
    return best


names = ["ax_spa_lcdm_halofit_dovekie", "ax_spa_w0wa_halofit_dovekie"]
for suffix, with_edge in (("_desy5", True), ("", False)):
    b = points(suffix, with_edge)
    if b and f"ax_spa_latetwist_{b[1]}_dovekie" not in names:
        names.append(f"ax_spa_latetwist_{b[1]}_dovekie")
print("\n".join(names))
