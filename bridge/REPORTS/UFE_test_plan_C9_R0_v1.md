# C9 search plan v1: R0 admission

The team intends to carry the derivation through testing under C7/C9. The
leader selects outward-first because A01 establishes only a conditional local
two-scalar minimum, not a coupled, data-eligible UFE. The checker performs
one R0 check and returns its result before the leader chooses the next node.
Nothing else in this plan authorizes another execution.

## Adaptive search rules

The candidate catalogue is: mandatory complex U anchor; S/tau (YFORK2);
Weave moduli; phi; dust; radiation; and alternative loop-metric, J-link,
product-link, flux and mediator bridges. A candidate has at most one
declared bridge, always conditional. Missing actions, model maps, inputs or
data remain UNCLEAR, never invented. `combine()` is metadata, not a complete
Hessian; `ufe_hessian2x2` is not the full-field Hessian. Count every free
coupling even if fixed for a check; also report parameters optimized.

View each candidate through at least geometry/metric, field-space masses,
and data/all applicable bounds; Loom layers are bookkeeping, not a physical
stability proof. An unresolved applicable view makes the overall conclusion
UNCLEAR. Local stability is not global stability. A single failure or
missing input cannot establish an ENDPOINT/CUT; only proof that no admissible
rescue exists over the declared remaining domain can do so. A node is
unchoosable only if all its paths are cut.

If a later conditional stable expanded candidate is established, examine
removal in forward and reverse addition order, retaining the U anchor and
disallowing the empty field. Keep a removal only if all views pass. A greedy
result is not a global minimum unless the declared finite graph has been
exhausted. Before any later case whose numerical inputs, source or rules are
not admitted here, publish a deviations record and a newly locked plan
before execution. No automatic loop, scan or tuning is authorized.

## R0: exact model and rule

Only SERAPIS-E U, two real scalar components; no extra sector or bridge.
At rho = (1/2, sqrt(3)/2), MPl=1, normalized V0=1, C=0, lam=1,
G=I/(2 y^2). E_paper is the full-lattice normalization implemented with
E_fourier's default s=2 and nmax=20 with `mp.mp.dps=30`. The
potential is z/(1+z), z=E_paper(U)-E_paper(rho). The analytic comparison
is each normalized eigenvalue = 2 E_paper(rho). These are conditional
assumptions, not a compactification derivation or an observational claim.

One process computes h=(1e-3, 3e-4, 1e-4), each central coordinate
gradient and `landscape.hessian_canonical(..., n=1)` eigenvalues. All
stencil coordinates must be finite with y>0, and all values/outputs finite.
For all six eigenvalues, margin = 1e-6 * max(1, max(abs(eigenvalues)));
max relative error to the positive reference and the maximum per-ordered-
eigenvalue spread across h divided by reference must each be <= 1e-3.
Maximum absolute coordinate-gradient component must be <=
1e-5 * max(1, abs(E_paper(rho))).

Local mass verdict: clearly negative eigenvalue below -margin is NOT STABLE
locally; otherwise all numerical checks and min eigenvalue > margin give
STABLE locally; all other cases are UNCLEAR. The comparison is to the
analytic local reference, not a data fit. The full-field and observational
views are uncomputed, making the overall verdict UNCLEAR. No input dataset,
covariance, measured likelihood, global cutoff or observational acceptance
is assumed. Baseline coupling budget is 2 (V0 and C), optimized parameters 0;
lam=1 is a fixed normalization convention.

## Identity and execution

Source AEGIS commit `35ee189df9bc94ce9e98d754405b6441cc8d6412`:
`tools/serapis_calc/landscape.py` SHA-256
`ad15823f52f24ed032eee8cc55b1b629bcb45c68c6950dc2da17021393156ee4`;
`tools/serapis_calc/eisenstein.py` SHA-256
`af6b252ef446d36f19439c370acc818e9dff3053c20be83532451965ba25c5b7`;
`tools/serapis_calc/__init__.py` SHA-256
`25af74d3c55ad628eaa4fd363065543100efe9dad895c498836b1f389abfc779`.
The isolated harness `r0.py` below has SHA-256
`0546b041c84b4a276c885987f0bd09f34893401ad4b933c3ad1bb8b04675e985`.
Use an isolated directory containing those files at their relative paths.
Do not overwrite historical outputs. The documented broad selftest was not
run; this limited R0 is not a substitute for complete engine validation.

Intended host: Windows 11 x64, Python 3.12.10, NumPy 2.5.4,
SciPy 1.18.1, mpmath 1.3.0; mpmath dps is set to 30 and recorded.
Package metadata was inspected, but loading native modules has not yet been
established. Refuse execution if the versions or pinned bytes differ.
With the isolated directory as working directory, exact command:

```powershell
python -I -B -u .\r0.py 1> .\r0-stdout-v1.txt 2> .\r0-stderr-v1.txt
```

The Python executable is the identified Python 3.12.10 interpreter; the
exclusive output is the previously nonexistent `r0-result-v1.json` in that
directory; stdout and stderr go to the previously nonexistent named files.
Capture exit code and elapsed runtime. The JSON
records all three h values, gradients, eigenvalues, numerical rules, versions,
views, fit count, errors and verdict. An import/runtime failure is reported
explicitly and remains UNCLEAR, with no bypass of Windows application
control, installation or rerun. R0 begins only after this plan and its
SHA-256 sidecar are pushed and both remote byte identities verified.

## Exact isolated harness

```python
import json
import math
import pathlib
import sys
import time
import traceback

root = pathlib.Path(__file__).resolve().parent
output = root / "r0-result-v1.json"
start = time.monotonic()
result = {"case": "R0", "overall": "UNCLEAR", "views": {}}
if output.exists():
    raise SystemExit("Refusing to overwrite r0-result-v1.json")

try:
    sys.path.insert(0, str(root))
    import numpy as np
    import scipy
    import mpmath as mp
    from tools.serapis_calc import landscape
    from tools.serapis_calc.eisenstein import E_paper

    mp.mp.dps = 30
    x, y = 0.5, math.sqrt(3) / 2
    ref = 2 * E_paper(x, y)
    er = ref / 2
    if not math.isfinite(ref) or ref <= 0:
        raise ValueError("Invalid reference E_paper(rho)")
    potential = lambda a, b: landscape.V_tau(a, b, C=0, lam=1, Er=er)
    rows = []
    for h in (1e-3, 3e-4, 1e-4):
        coords = [(x + a * h, y + b * h)
                  for a, b in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1),
                               (1, 1), (1, -1), (-1, 1), (-1, -1))]
        if not all(b > 0 and math.isfinite(a) and math.isfinite(b) for a, b in coords):
            raise ValueError("Invalid metric stencil")
        vals = [potential(a, b) for a, b in coords]
        if not all(math.isfinite(v) for v in vals):
            raise ValueError("Non-finite potential stencil")
        gradient = [(vals[1] - vals[2]) / (2 * h), (vals[3] - vals[4]) / (2 * h)]
        eigs = landscape.hessian_canonical(potential, x, y, h=h, n=1).tolist()
        if not all(math.isfinite(v) for v in gradient + eigs):
            raise ValueError("Non-finite gradient or eigenvalue")
        rows.append({"h": h, "gradient": gradient, "eigenvalues": eigs})

    eigs = [v for row in rows for v in row["eigenvalues"]]
    margin = 1e-6 * max(1.0, max(abs(v) for v in eigs))
    relerr = max(abs(v - ref) / ref for v in eigs)
    spread = max(max(row["eigenvalues"][i] for row in rows)
                 - min(row["eigenvalues"][i] for row in rows) for i in (0, 1)) / ref
    gradmax = max(abs(v) for row in rows for v in row["gradient"])
    gradlimit = 1e-5 * max(1.0, abs(er))
    numerical = relerr <= 1e-3 and spread <= 1e-3 and gradmax <= gradlimit
    mass = "NOT STABLE" if min(eigs) < -margin else (
        "STABLE locally" if numerical and min(eigs) > margin else "UNCLEAR")
    result.update({
        "reference_eigenvalue": ref, "E_paper_rho": er, "rows": rows,
        "mass_margin": margin, "relative_error_max": relerr,
        "inter_h_spread_relative": spread, "gradient_inf_max": gradmax,
        "gradient_limit": gradlimit, "numerical_admission": numerical,
        "versions": {"python": sys.version, "numpy": np.__version__,
                     "scipy": scipy.__version__, "mpmath": mp.__version__,
                     "mpmath_dps": mp.mp.dps},
        "views": {
            "geometry_metric": "rho and positive metric stencil; symmetry applicability conditional",
            "mass": mass,
            "data_bounds": "UNCLEAR: observational bounds and full action not established",
            "loom": "source bookkeeping only; no physical stability conclusion"
        },
        "overall": "UNCLEAR",
        "fit_budget": {"free_couplings": 2, "optimized_parameters": 0}
    })
    exit_code = 0
except Exception as exc:
    traceback.print_exc()
    result["error"] = {"type": type(exc).__name__, "message": str(exc)}
    exit_code = 1

result["runtime_seconds"] = time.monotonic() - start
result["exit_code"] = exit_code
with output.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, indent=2, allow_nan=False)
    f.write("\n")
print(json.dumps(result, allow_nan=False))
raise SystemExit(exit_code)
```
