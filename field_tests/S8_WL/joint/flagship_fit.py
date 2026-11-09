"""FLAG-1 (field_tests/rules/PREREG_FLAGSHIP.md): the S8-J fit with kappa fixed at 1.
    python flagship_fit.py ax_spa_spiraltwist_kappa1[_dovekie|_union3]_nlfix_s8y6     (PC, WSL env "aegis")
Uses the S8-J wrapper unchanged (s8_joint_fit.add_s8); kappa is fixed by early_late_spa's "_kappa<x>" name rule."""
import os
import sys
import time

import s8_joint_fit as J

RULE = os.path.join(J.AEGIS, "field_tests", "rules", "PREREG_FLAGSHIP.md")
RUNS = ["ax_spa_spiraltwist_kappa1_nlfix", "ax_spa_spiraltwist_kappa1_dovekie_nlfix",
        "ax_spa_spiraltwist_kappa1_union3_nlfix"]


def run(name):
    assert name.endswith("_s8y6") and name[:-5] in RUNS, f"unknown run {name}"
    assert os.path.exists(RULE + ".sha256"), "PREREG_FLAGSHIP.md is not locked; no fit runs before the lock"
    import early_late_spa as E
    from cobaya.run import run as crun
    base = name[:-5]
    t = time.time()
    E._maybe_coupled(base)
    info = E.make(base)
    J.add_s8(info)
    info["output"] = f"{E.OUT}/chains/cmp_{name}"
    crun(info)
    E.save(name, time.time() - t)


if __name__ == "__main__":
    run(sys.argv[1])
