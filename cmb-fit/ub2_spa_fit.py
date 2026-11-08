"""UB-2 follow-up (declared in PREREG_UNIFY_DATA.md, runs ONLY once its own rule is locked): the same UB-2 runs on the
combined CMB of cmbfit_compare's "spa_" data (P-ACT: Planck cut + ACT DR6 + ACT x Planck lensing, plus SPT-3G D1 lite)
+ DESI DR2 + one SN set. Kept in its own file so the locked ub2_fit.py is untouched.
    python ub2_spa_fit.py ub2B_spa[_dovekie|_union3] | w0wa_spa[...] | lcdm_spa[...]"""
import os
import sys

import cmbfit_compare as CC
import ub2_fit as U

ORIG_MAKE = U.make
RULE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "field_tests", "rules", "PREREG_UNIFY_SPA.md.sha256")


def make(name):
    """'<run>_spa[_sn]' -> the UB-2 info for '<run>[_sn]' with the spa_ CMB likelihoods swapped in."""
    base = name.replace("_spa", "")
    core = base
    for suf in U.SN:
        if core.endswith(suf):
            core = core[:-len(suf)]
    if core == "lcdm":
        import cmbfit as C
        info = C.make_info("lcdm", sampler={"minimize": {"method": "bobyqa", "best_of": 4}})
        sn = base[len(core):]
        if sn:
            info["likelihood"].pop("sn.pantheonplus")
            info["likelihood"][U.SN[sn]] = None
        CC._start_near(info, CC.START_LCDM)
    else:
        info = ORIG_MAKE(base.replace("w0wa", "w0waP") if core == "w0wa" else base)
    if "ubcamb" in info["theory"]:
        info["theory"]["camb"] = info["theory"].pop("ubcamb")          # _spa edits theory['camb']
        CC._spa(info)
        info["theory"]["ubcamb"] = info["theory"].pop("camb")
    else:
        CC._spa(info)
    info["output"] = os.path.join(U.C.RESULTS, "chains", "cmp_" + name)
    return info


if __name__ == "__main__":
    if not os.path.exists(RULE):
        raise SystemExit("The ACT/SPT follow-up is not locked (field_tests/rules/PREREG_UNIFY_SPA.md.sha256 missing)")
    U.make = make
    for n in sys.argv[1:]:
        U.run(n)
