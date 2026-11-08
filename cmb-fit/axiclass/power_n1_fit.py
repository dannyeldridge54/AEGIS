"""POWER_N n = 1 on AxiCLASS (run plan field_tests/rules/PREREG_POWER_N1_AXICLASS.md, carrying out the deferral in
cubemind/PREREGISTRATION_SPT3G_DEVIATIONS.md, 31 Oct 21:05 CT, of cubemind/PREREGISTRATION_POWER_N.md).
The stored ax_spa_edelock fit (early_late_spa.make, unchanged) with ONE change: n_axion = 1.
    python power_n1_fit.py            -> results/cmp_ax_spa_edelock_n1.json   (refuses to run before the lock)
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
AEGIS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
RULE = os.path.join(AEGIS, "field_tests", "rules", "PREREG_POWER_N1_AXICLASS.md")
NAME = "ax_spa_edelock_n1"


def make():
    import early_late_spa as E
    E._maybe_coupled("ax_spa_edelock")
    info = E.make("ax_spa_edelock")
    extra = info["theory"]["classytwist"]["extra_args"] if "classytwist" in info["theory"] else \
        next(iter(info["theory"].values()))["extra_args"]
    assert extra.get("n_axion") == 3, extra.get("n_axion")
    extra["n_axion"] = 1
    info["output"] = f"{E.OUT}/chains/cmp_{NAME}"
    return info, E


if __name__ == "__main__":
    assert os.path.exists(RULE + ".sha256"), "PREREG_POWER_N1_AXICLASS.md is not locked; no fit runs before the lock"
    from cobaya.run import run as crun
    t = time.time()
    info, E = make()
    crun(info)
    E.save(NAME, time.time() - t)
