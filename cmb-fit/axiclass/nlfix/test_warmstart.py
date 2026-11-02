"""Check the NR warm start: an _nlfix grid run's ref centres equal its original run's minimum."""
import os as _os
_AXI = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_RESULTS = _os.environ.get("TWIST_RESULTS", _os.path.join(_os.path.dirname(_AXI), "results"))
_BUILDS = _os.environ.get("TWIST_BUILDS", _os.path.expanduser("~"))
import json
import sys

sys.path.insert(0, _AXI)
import early_late_spa as E

for n in ("ax_spa_latetwist_gF0.5m-0.3_nlfix", "ax_spa_coupledtwist_gF0.3m-0.1_nlfix", "ax_spa_latetwist_gF-0.6m0.751_nlfix"):
    info = E.make(n)
    o = n.replace("_nlfix", "")
    try:
        m = json.load(open(f"{E.OUT}/cmp_{o}.json"))["minimum"]
        src = "original"
    except FileNotFoundError:
        m = json.load(open(f"{E.OUT}/cmp_ax_spa_lcdm_halofit.json"))["minimum"]
        src = "LCDM halofit (no original)"
    ok = all(abs(p["ref"]["loc"] - m[k]) < 1e-12 for k, p in info["params"].items()
             if isinstance(p, dict) and "ref" in p and k in m)
    print(f"{n}: centred on {src}: {'OK' if ok else 'MISMATCH'}; best_of {info['sampler']['minimize']['best_of']}")
