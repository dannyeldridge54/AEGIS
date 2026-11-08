"""UB-1 deviation D2 (field_tests/rules/UB1_DEVIATIONS.md): re-run a UB-1 script unchanged, except that json.dump can
write numpy booleans (the first runs crashed while writing the result after the verdict line). Usage:
    python run_ub1_d2.py unify_hyperbolic_bg       (locked code)
    python run_ub1_d2.py unify_hyperbolic_bg_v2    (D1)"""
import importlib
import json
import sys

mod = importlib.import_module(sys.argv[1])
_dump = json.dump
mod.json.dump = lambda obj, fp, **kw: _dump(obj, fp, default=lambda o: o.item() if hasattr(o, "item") else str(o), **kw)
mod.main()
